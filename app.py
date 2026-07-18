# استيراد المكتبات الأساسية الخاصة بالواجهة والبيانات
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# استيراد الدوال المسؤولة عن التعامل مع قاعدة البيانات
from database import (
    create_database,
    save_feedback,
    search_by_phone,
    update_feedback,
    delete_feedback,
    load_feedback,
)

# استيراد صفحة لوحة التحكم
from dashboard import show_dashboard

# ==========================
# إعدادات الصفحة الرئيسية
# ==========================
st.set_page_config(
    page_title="Restaurant Feedback System",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================
# تحميل ملف التنسيق لتجميل الواجهة
# ==========================
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================
# إنشاء ملف قاعدة البيانات إذا لم يكن موجودًا
# ==========================
# تجهيز قاعدة البيانات قبل تشغيل النظام
create_database()

# ==========================
# إعداد القائمة الجانبية للتنقل بين الصفحات
# ==========================
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
    width=120,
)

st.sidebar.title("🍽 Restaurant System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Customer Feedback",
        "Dashboard",
    ],
)

# ==========================
# في حالة اختيار لوحة التحكم يتم عرضها مباشرة
# ==========================
if page == "Dashboard":
            # عرض لوحة التحكم
    show_dashboard()
    st.stop()

# ==========================
# الصفحة الرئيسية الخاصة بإدخال تقييمات العملاء
# ==========================
st.title("🍽 Restaurant Customer Feedback System")
st.markdown("---")

left, right = st.columns(2)

# ==========================
# بيانات العميل
# ==========================
with left:

    st.subheader("👤 Customer Information")

    full_name = st.text_input(
        "Full Name",
        placeholder="Enter customer name",
    )

    phone = st.text_input(
        "Phone Number",
        placeholder="01xxxxxxxxx",
    )

    feedback_date = st.date_input(
        "Date",
        value=datetime.today(),
    )

# ==========================
# بيانات الوجبة والتقييم
# ==========================
with right:

    st.subheader("🍗 Meal Information")

    meal = st.selectbox(
        "Meal",
        [
            "Grilled Chicken",
            "Fried Chicken",
            "Shawarma",
        ],
    )

    temperature = st.selectbox(
        "Food Temperature",
        [
            "Hot",
            "Warm",
            "Cold",
        ],
    )

    rating = st.slider(
        "Taste Rating",
        1,
        5,
        5,
    )

    waiting = st.selectbox(
        "Waiting Time",
        [
            "Less than 10 min",
            "10-20 min",
            "More than 20 min",
        ],
    )

    cleanliness = st.selectbox(
        "Cleanliness",
        [
            "Excellent",
            "Good",
            "Fair",
        ],
    )

comment = st.text_area(
    "Comment",
    placeholder="Write your feedback...",
    height=150,
)

# ====================================
# أزرار تنفيذ العمليات
# ====================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

# -------------------------
# حفظ التقييم الجديد
# -------------------------
with col1:

    if st.button("✅ Submit Feedback", use_container_width=True):

        if full_name.strip() == "" or phone.strip() == "":

            st.error("Please enter Name and Phone Number")

        else:

            save_feedback(

                full_name,

                phone,

                str(feedback_date),

                meal,

                temperature,

                rating,

                waiting,

                cleanliness,

                comment,

            )

            st.success("Feedback Saved Successfully")

# -------------------------
# البحث عن عميل باستخدام رقم الهاتف
# -------------------------
with col2:

    if st.button("🔍 Search", use_container_width=True):

        result = search_by_phone(phone)

        if result is not None:

            st.success("Customer Found")

            st.dataframe(result)

        else:

            st.warning("Customer Not Found")



# -------------------------
# حذف بيانات عميل باستخدام رقم الهاتف
# -------------------------
with col3:

    if st.button("🗑 Delete", use_container_width=True):

        success = delete_feedback(phone)

        if success:

            st.success("Feedback Deleted Successfully")

        else:

            st.error("Phone Number Not Found")


# ====================================
# تصدير البيانات إلى ملف Excel
# ====================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    data = load_feedback()

    excel_file = "feedback.xlsx"

    with open(excel_file, "rb") as file:

        st.download_button(

            label="📥 Export to Excel",

            data=file,

            file_name="Restaurant_Feedback.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True,

        )



# ====================================
# عرض جميع التقييمات المسجلة
# ====================================

st.markdown("---")

st.subheader("📋 Customer Feedback Records")

data = load_feedback()

if len(data) > 0:

    st.dataframe(

        data,

        use_container_width=True,

        hide_index=True,

    )

else:

    st.info("No Feedback Available")

# ====================================
# إحصائيات سريعة عن البيانات الحالية
# ====================================

st.markdown("---")

st.subheader("📊 Quick Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Feedback",
        len(data)
    )

with col2:

    if len(data) > 0:

        st.metric(
            "Average Rating",
            round(data["Taste Rating"].mean(),2)
        )

    else:

        st.metric(
            "Average Rating",
            0
        )

with col3:

    if len(data) > 0:

        st.metric(
            "Most Ordered Meal",
            data["Meal"].mode()[0]
        )

    else:

        st.metric(
            "Most Ordered Meal",
            "-"
        )

with col4:

    if len(data) > 0:

        st.metric(
            "Excellent Cleanliness",
            len(
                data[
                    data["Cleanliness"]=="Excellent"
                ]
            )
        )

    else:

        st.metric(
            "Excellent Cleanliness",
            0
        )

st.markdown("---")

st.success("Restaurant Feedback System Ready ✅")