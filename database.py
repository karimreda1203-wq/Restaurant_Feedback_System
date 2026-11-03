# استيراد مكتبة Pandas للتعامل مع ملفات Excel والبيانات
import pandas as pd
# استيراد مكتبة os للتعامل مع الملفات والتحقق من وجودها
import os
# استيراد مكتبة re للتحقق من صيغة رقم الهاتف
import re

# اسم ملف قاعدة البيانات الذي سيتم حفظ التقييمات بداخله
DATABASE = "feedback.xlsx"

# أسماء الأعمدة الأساسية في قاعدة البيانات
COLUMNS = [
    "Full Name",
    "Phone Number",
    "Date",
    "Meal",
    "Food Temperature",
    "Taste Rating",
    "Waiting Time",
    "Cleanliness",
    "Comment",
]

# صيغة أرقام الموبايل المصرية: 11 رقم تبدأ بـ 010 أو 011 أو 012 أو 015
PHONE_PATTERN = re.compile(r"^01[0125]\d{8}$")


# ===================================
# Validation
# ===================================

# دالة التحقق من صحة رقم الهاتف
def is_valid_phone(phone):
    return bool(PHONE_PATTERN.match(str(phone).strip()))


# ===================================
# Create Database
# ===================================

# دالة إنشاء ملف Excel لأول مرة إذا لم يكن موجودًا
def create_database():
    if not os.path.exists(DATABASE):
        # إنشاء جدول فارغ بالأعمدة الأساسية وحفظه على الجهاز
        pd.DataFrame(columns=COLUMNS).to_excel(DATABASE, index=False)


# ===================================
# Load Data
# ===================================

# دالة تحميل جميع البيانات من ملف Excel
def load_feedback():
    # التأكد من وجود قاعدة البيانات قبل القراءة
    create_database()

    # قراءة البيانات مع الحفاظ على أرقام الهاتف والتاريخ كنص
    df = pd.read_excel(
        DATABASE,
        dtype={"Phone Number": str, "Date": str},
    )

    # تحويل التقييم إلى رقم حتى تعمل العمليات الحسابية بشكل صحيح
    df["Taste Rating"] = pd.to_numeric(df["Taste Rating"], errors="coerce")

    # تحويل التعليقات الفارغة إلى نص فارغ بدل NaN
    df["Comment"] = df["Comment"].fillna("").astype(str)

    return df


# دالة حفظ البيانات في ملف Excel
def _save(df):
    df.to_excel(DATABASE, index=False)


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
    df = load_feedback()

    # إضافة سجل جديد في آخر الجدول
    df.loc[len(df)] = {
        "Full Name": str(full_name).strip(),
        "Phone Number": str(phone).strip(),
        "Date": str(date),
        "Meal": meal,
        "Food Temperature": temperature,
        "Taste Rating": rating,
        "Waiting Time": waiting,
        "Cleanliness": cleanliness,
        "Comment": comment,
    }

    _save(df)


# ===================================
# Search By Phone
# ===================================

# دالة البحث عن كل تقييمات عميل باستخدام رقم الهاتف
# ترجع النتائج مع رقم الصف الأصلي (index) لاستخدامه في التعديل والحذف
def search_by_phone(phone):
    df = load_feedback()
    phone = str(phone).strip()
    result = df[df["Phone Number"].astype(str) == phone]

    if result.empty:
        return None

    return result


# ===================================
# Update Feedback
# ===================================

# دالة تعديل تقييم واحد محدد باستخدام رقم الصف
def update_feedback(
    row_index,
    full_name,
    date,
    meal,
    temperature,
    rating,
    waiting,
    cleanliness,
    comment,
):
    df = load_feedback()

    if row_index not in df.index:
        return False

    df.loc[row_index, "Full Name"] = str(full_name).strip()
    df.loc[row_index, "Date"] = str(date)
    df.loc[row_index, "Meal"] = meal
    df.loc[row_index, "Food Temperature"] = temperature
    df.loc[row_index, "Taste Rating"] = rating
    df.loc[row_index, "Waiting Time"] = waiting
    df.loc[row_index, "Cleanliness"] = cleanliness
    df.loc[row_index, "Comment"] = comment

    _save(df)

    return True


# ===================================
# Delete Feedback
# ===================================

# دالة حذف تقييم واحد محدد باستخدام رقم الصف (وليس كل تقييمات العميل)
def delete_feedback(row_index):
    df = load_feedback()

    if row_index not in df.index:
        return False

    df = df.drop(row_index).reset_index(drop=True)

    _save(df)

    return True
