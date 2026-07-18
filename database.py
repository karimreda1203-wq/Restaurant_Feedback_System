# استيراد مكتبة Pandas للتعامل مع ملفات Excel والبيانات
import pandas as pd
# استيراد مكتبة os للتعامل مع الملفات والتحقق من وجودها
import os

# اسم ملف قاعدة البيانات الذي سيتم حفظ التقييمات بداخله
DATABASE = "feedback.xlsx"

# ===================================
# Create Database
# ===================================

# دالة إنشاء ملف Excel لأول مرة إذا لم يكن موجودًا
def create_database():

    # التحقق مما إذا كان ملف قاعدة البيانات غير موجود
    if not os.path.exists(DATABASE):

        # إنشاء جدول بالأعمدة الأساسية الخاصة بالتقييمات
        df = pd.DataFrame(columns=[

            "Full Name",

            "Phone Number",

            "Date",

            "Meal",

            "Food Temperature",

            "Taste Rating",

            "Waiting Time",

            "Cleanliness",

            "Comment",

        ])

        # حفظ الملف الفارغ على الجهاز
        df.to_excel(DATABASE, index=False)

# ===================================
# Load Data
# ===================================

# دالة تحميل جميع البيانات من ملف Excel
def load_feedback():

    # التأكد من وجود قاعدة البيانات قبل القراءة
    create_database()

    # قراءة البيانات وإرجاعها كـ DataFrame مع الحفاظ على أرقام الهاتف كنص
    return pd.read_excel(DATABASE,
                         dtype={"Phone Number": str})

# ===================================
# Save Feedback
# ===================================

# دالة حفظ تقييم جديد داخل قاعدة البيانات
def save_feedback(

    full_name,

    phone,

    date,

    meal,

    temperature,

    rating,

    waiting,

    cleanliness,

    comment,

):

    # تحميل البيانات الحالية من الملف
    df = load_feedback()

    phone = str(phone).strip()
    full_name = str(full_name).strip()
    # إنشاء سجل جديد يحتوي على بيانات المستخدم
    new_row = {

        "Full Name": full_name,

        "Phone Number": phone,

        "Date": date,

        "Meal": meal,

        "Food Temperature": temperature,

        "Taste Rating": rating,

        "Waiting Time": waiting,

        "Cleanliness": cleanliness,

        "Comment": comment,

    }

    # إنشاء سجل جديد يحتوي على بيانات المستخدم
    df.loc[len(df)] = new_row

        # حفظ الملف الفارغ على الجهاز
    # حفظ البيانات بعد الإضافة
    df.to_excel(DATABASE, index=False)

# ===================================
# Search By Phone
# ===================================

def search_by_phone(phone):

    # تحميل البيانات الحالية من الملف
    df = load_feedback()
    phone = str(phone).strip()
    result = df[df["Phone Number"].astype(str) == str(phone)]

    if result.empty:
        return None

    return result


# ===================================
# Update Feedback
# ===================================

def update_feedback(

    phone,

    full_name,

    date,

    meal,

    temperature,

    rating,

    waiting,

    cleanliness,

    comment,

):

    # تحميل البيانات الحالية من الملف
    df = load_feedback()
    phone = str(phone).strip()
    index = df[df["Phone Number"].astype(str) == str(phone)].index

    if len(index) == 0:
        return False

    i = index[0]

    df.loc[i, "Full Name"] = full_name
    df.loc[i, "Date"] = date
    df.loc[i, "Meal"] = meal
    df.loc[i, "Food Temperature"] = temperature
    df.loc[i, "Taste Rating"] = rating
    df.loc[i, "Waiting Time"] = waiting
    df.loc[i, "Cleanliness"] = cleanliness
    df.loc[i, "Comment"] = comment

        # حفظ الملف الفارغ على الجهاز
    # حفظ البيانات بعد الإضافة
    df.to_excel(DATABASE, index=False)

    return True


# ===================================
# Delete Feedback
# ===================================

def delete_feedback(phone):

    # تحميل البيانات الحالية من الملف
    df = load_feedback()
    phone = str(phone).strip()
    index = df[df["Phone Number"].astype(str) == str(phone)].index

    if len(index) == 0:
        return False

    df = df.drop(index)

    df.reset_index(drop=True, inplace=True)

        # حفظ الملف الفارغ على الجهاز
    # حفظ البيانات بعد الإضافة
    df.to_excel(DATABASE, index=False)

    return True


# ===================================
# Export Excel
# ===================================

def export_excel():

    return DATABASE