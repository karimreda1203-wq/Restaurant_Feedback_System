# استيراد المكتبات الأساسية الخاصة بالواجهة والبيانات
import streamlit as st
import pandas as pd
from datetime import date
import hmac
import os

# استيراد الدوال المسؤولة عن التعامل مع قاعدة البيانات
from database import (
    DATABASE,
    create_database,
    save_feedback,
    search_by_phone,
    update_feedback,
    delete_feedback,
    load_feedback,
    is_valid_phone,
)

# استيراد صفحة لوحة التحكم
from dashboard import show_dashboard

# ==========================
# الاختيارات المتاحة في النموذج
# ==========================
MEALS = ["Grilled Chicken", "Fried Chicken", "Shawarma"]
TEMPERATURES = ["Hot", "Warm", "Cold"]
WAITING_TIMES = ["Less than 10 min", "10-20 min", "More than 20 min"]
CLEANLINESS = ["Excellent", "Good", "Fair"]

PHONE_ERROR = "Please enter a valid phone number (11 digits starting with 010, 011, 012 or 015)"

# ==========================
# إعدادات الصفحة الرئيسية
# ==========================
st.set_page_config(
    page_title="Restaurant Feedback System",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# تحميل ملف التنسيق لتجميل الواجهة (إن وجد)
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# تجهيز قاعدة البيانات قبل تشغيل النظام
create_database()

# ==========================
# متغيرات الجلسة
# ==========================
# هل صاحب المطعم مسجل دخول؟
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# رقم إصدار يزيد بعد كل تعديل أو حذف حتى يتم تحديث نموذج التعديل
if "version" not in st.session_state:
    st.session_state.version = 0


# دالة لعرض رسالة بعد إعادة تحميل الصفحة
def flash(message):
    st.session_state.flash = message
    st.session_state.version += 1
    st.rerun()


# دالة لعرض رسالة العملية السابقة (إن وجدت)
def show_flash():
    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))


# دالة لمعرفة مكان القيمة الحالية داخل قائمة الاختيارات
def option_index(options, value):
    return options.index(value) if value in options else 0


# ====================================
# صفحة العميل: نموذج التقييم فقط
# ====================================
def customer_page():

    st.title("🍽 Share Your Feedback")
    st.write("We'd love to hear about your experience today!")
    st.markdown("---")

    # clear_on_submit يفرّغ الحقول بعد الإرسال حتى لا يتكرر نفس التقييم
    with st.form("new_feedback", clear_on_submit=True):

        left, right = st.columns(2)

        # بيانات العميل
        with left:
            st.subheader("👤 Your Information")
            full_name = st.text_input("Full Name", placeholder="Enter your name")
            phone = st.text_input("Phone Number", placeholder="01xxxxxxxxx", max_chars=11)

        # بيانات الوجبة والتقييم
        with right:
            st.subheader("🍗 Your Meal")
            meal = st.selectbox("Meal", MEALS)
            temperature = st.selectbox("Food Temperature", TEMPERATURES)
            rating = st.slider("Taste Rating", 1, 5, 5)
            waiting = st.selectbox("Waiting Time", WAITING_TIMES)
            cleanliness = st.selectbox("Cleanliness", CLEANLINESS)

        comment = st.text_area("Comment", placeholder="Write your feedback...", height=150)

        submitted = st.form_submit_button("✅ Submit Feedback", width="stretch")

    # حفظ التقييم بعد التحقق من صحة البيانات (التاريخ يتسجل تلقائيًا بتاريخ اليوم)
    if submitted:
        if full_name.strip() == "":
            st.error("Please enter your name")
        elif not is_valid_phone(phone):
            st.error(PHONE_ERROR)
        else:
            save_feedback(
                full_name,
                phone,
                str(date.today()),
                meal,
                temperature,
                rating,
                waiting,
                cleanliness,
                comment,
            )
            st.success("Thank you! Your feedback has been submitted 🙏")


# ====================================
# تسجيل دخول صاحب المطعم
# ====================================
def get_admin_password():
    # الباسورد محفوظ في ملف .streamlit/secrets.toml وليس داخل الكود
    try:
        return st.secrets["admin_password"]
    except Exception:
        return None


def login_page():

    st.title("🔒 Restaurant Admin")

    admin_password = get_admin_password()

    if not admin_password:
        st.error(
            "Admin password is not set. Create the file .streamlit/secrets.toml "
            'and add this line to it:  admin_password = "your-password"'
        )
        return

    with st.form("login"):
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login", width="stretch")

    if login:
        # compare_digest يقارن الباسورد بطريقة آمنة
        if hmac.compare_digest(password, str(admin_password)):
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Wrong password")


# ====================================
# صفحة المطعم: البحث والتعديل والحذف وعرض كل التقييمات
# ====================================
def manage_feedback_page():

    st.title("🗂 Manage Feedback")
    show_flash()
    st.markdown("---")

    st.subheader("🔍 Search, Edit or Delete Feedback")

    search_phone = st.text_input(
        "Customer Phone Number",
        placeholder="01xxxxxxxxx",
        max_chars=11,
        key="search_phone",
    )

    if search_phone.strip() != "":

        if not is_valid_phone(search_phone):
            st.error(PHONE_ERROR)

        else:
            result = search_by_phone(search_phone)

            if result is None:
                st.warning("Customer Not Found")

            else:
                st.success(f"Found {len(result)} feedback record(s)")
                st.dataframe(result, width="stretch", hide_index=True)

                # اختيار تقييم واحد محدد لتعديله أو حذفه
                row_index = st.selectbox(
                    "Choose a record to edit or delete",
                    result.index,
                    format_func=lambda i: (
                        f"{result.loc[i, 'Date']} - {result.loc[i, 'Meal']} - "
                        f"{result.loc[i, 'Taste Rating']}⭐"
                    ),
                    key=f"pick_{st.session_state.version}",
                )

                record = result.loc[row_index]

                # تحويل التاريخ المحفوظ كنص إلى تاريخ لعرضه في النموذج
                try:
                    record_date = pd.to_datetime(record["Date"]).date()
                except (ValueError, TypeError):
                    record_date = date.today()

                # مفتاح فريد لكل سجل حتى تتحدث القيم عند اختيار سجل آخر
                k = f"{st.session_state.version}_{row_index}"

                with st.form(f"edit_{k}"):

                    st.markdown("**✏️ Edit Selected Record**")

                    e_left, e_right = st.columns(2)

                    with e_left:
                        e_name = st.text_input("Full Name", value=record["Full Name"])
                        e_date = st.date_input("Date", value=record_date)
                        e_meal = st.selectbox(
                            "Meal", MEALS, index=option_index(MEALS, record["Meal"])
                        )
                        e_temperature = st.selectbox(
                            "Food Temperature",
                            TEMPERATURES,
                            index=option_index(TEMPERATURES, record["Food Temperature"]),
                        )

                    with e_right:
                        current_rating = record["Taste Rating"]
                        e_rating = st.slider(
                            "Taste Rating",
                            1,
                            5,
                            int(current_rating) if pd.notna(current_rating) else 5,
                        )
                        e_waiting = st.selectbox(
                            "Waiting Time",
                            WAITING_TIMES,
                            index=option_index(WAITING_TIMES, record["Waiting Time"]),
                        )
                        e_cleanliness = st.selectbox(
                            "Cleanliness",
                            CLEANLINESS,
                            index=option_index(CLEANLINESS, record["Cleanliness"]),
                        )

                    e_comment = st.text_area("Comment", value=record["Comment"])

                    confirm_delete = st.checkbox("I confirm I want to delete this record")

                    b1, b2 = st.columns(2)
                    save_clicked = b1.form_submit_button("💾 Save Changes", width="stretch")
                    delete_clicked = b2.form_submit_button("🗑 Delete Record", width="stretch")

                # حفظ التعديلات
                if save_clicked:
                    if e_name.strip() == "":
                        st.error("Please enter the customer name")
                    elif update_feedback(
                        row_index,
                        e_name,
                        str(e_date),
                        e_meal,
                        e_temperature,
                        e_rating,
                        e_waiting,
                        e_cleanliness,
                        e_comment,
                    ):
                        flash("Feedback Updated Successfully")
                    else:
                        st.error("Record not found, please search again")

                # حذف السجل المختار فقط بعد التأكيد
                if delete_clicked:
                    if not confirm_delete:
                        st.warning("Please tick the confirmation box before deleting")
                    elif delete_feedback(row_index):
                        flash("Feedback Deleted Successfully")
                    else:
                        st.error("Record not found, please search again")

    # عرض جميع التقييمات وتصديرها
    st.markdown("---")
    st.subheader("📋 All Customer Feedback")

    data = load_feedback()

    if len(data) > 0:
        st.dataframe(data, width="stretch", hide_index=True)
    else:
        st.info("No Feedback Available")

    with open(DATABASE, "rb") as file:
        st.download_button(
            label="📥 Export to Excel",
            data=file,
            file_name="Restaurant_Feedback.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ====================================
# القائمة الجانبية والتنقل بين الصفحات
# ====================================
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
    width=120,
)

st.sidebar.title("🍽 Restaurant System")

page = st.sidebar.radio(
    "Navigation",
    ["Customer Feedback", "Restaurant Admin"],
)

if page == "Customer Feedback":
    customer_page()

elif not st.session_state.is_admin:
    login_page()

else:
    # صفحات المطعم تظهر فقط بعد تسجيل الدخول
    admin_page = st.sidebar.radio(
        "Admin",
        ["Dashboard", "Manage Feedback"],
    )

    if st.sidebar.button("🚪 Logout", width="stretch"):
        st.session_state.is_admin = False
        st.rerun()

    if admin_page == "Dashboard":
        show_dashboard()
    else:
        manage_feedback_page()
