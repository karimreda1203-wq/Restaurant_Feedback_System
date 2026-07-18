# استيراد مكتبة Streamlit لإنشاء واجهة التطبيق
import streamlit as st
# استيراد Pandas للتعامل مع البيانات والجداول
import pandas as pd
# استيراد Plotly Express لرسم الرسوم البيانية
import plotly.express as px

# استيراد دالة تحميل بيانات التقييمات من ملف قاعدة البيانات
from database import load_feedback


   
# =====================================
# Dashboard
# =====================================

# الدالة الرئيسية المسؤولة عن إنشاء وعرض لوحة التحكم بالكامل
def show_dashboard():
    
    # عرض عنوان لوحة التحكم أعلى الصفحة
    st.title("📊 Restaurant Dashboard")

    # تحميل بيانات العملاء من قاعدة البيانات
    df = load_feedback()

    # إذا لم توجد أي بيانات يتم إظهار رسالة وإيقاف تنفيذ الدالة
    if df.empty:

        st.warning("No Feedback Available")

        return

    # ==============================
    # KPIs
    # ==============================

    # حساب إجمالي عدد التقييمات
    total_feedback = len(df)

    # حساب متوسط تقييم الطعم وتقريبه إلى منزلتين عشريتين
    avg_rating = round(df["Taste Rating"].mean(), 2)

    # استخراج أكثر وجبة تم اختيارها
    favorite_meal = df["Meal"].mode()[0]

    # حساب عدد العملاء الذين قيموا النظافة بأنها ممتازة
    excellent_clean = len(
        df[df["Cleanliness"] == "Excellent"]
    )

    # تقسيم الصفحة إلى أربعة أعمدة لعرض المؤشرات الرئيسية
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Feedback",
        total_feedback,
    )

    c2.metric(
        "Average Rating",
        avg_rating,
    )

    c3.metric(
        "Top Meal",
        favorite_meal,
    )

    c4.metric(
        "Excellent",
        excellent_clean,
    )

    st.markdown("---")

    # ==============================
    # Charts
    # ==============================

    # تقسيم الصفحة إلى عمودين لعرض الرسوم البيانية
    left, right = st.columns(2)

    # ------------------------------
    # Meal Chart
    # ------------------------------

    with left:

        # إنشاء رسم بياني يوضح عدد مرات طلب كل وجبة
        meal_chart = px.bar(

            df["Meal"].value_counts().reset_index(),

            x="Meal",

            y="count",

            title="🍗 Meals Ordered",

        )

        st.plotly_chart(
            meal_chart,
            use_container_width=True,
        )

    # ------------------------------
    # Rating Chart
    # ------------------------------

    with right:

        # إنشاء رسم يوضح توزيع تقييمات الطعم
        rating_chart = px.histogram(

            df,

            x="Taste Rating",

            nbins=5,

            title="⭐ Rating Distribution",

        )

        st.plotly_chart(

            rating_chart,

            use_container_width=True,

        )

# ==============================
    # Cleanliness Pie Chart
    # ==============================

    # تقسيم الصفحة إلى عمودين لعرض الرسوم البيانية
    left, right = st.columns(2)

    with left:

        # تجهيز بيانات النظافة لاستخدامها في الرسم الدائري
        clean_data = (
            df["Cleanliness"]
            .value_counts()
            .reset_index()
        )

        clean_data.columns = [
            "Cleanliness",
            "Count",
        ]

        # إنشاء رسم دائري يوضح نسب تقييمات النظافة
        clean_chart = px.pie(

            clean_data,

            names="Cleanliness",

            values="Count",

            title="🧼 Cleanliness",

            hole=0.45,

        )

        st.plotly_chart(

            clean_chart,

            use_container_width=True,

        )

    # ==============================
    # Waiting Time
    # ==============================

    with right:

        # تجهيز بيانات وقت الانتظار
        wait_data = (

            df["Waiting Time"]

            .value_counts()

            .reset_index()

        )

        wait_data.columns = [

            "Waiting Time",

            "Count",

        ]

        # إنشاء رسم بياني يوضح توزيع أوقات الانتظار
        wait_chart = px.bar(

            wait_data,

            x="Waiting Time",

            y="Count",

            title="⏰ Waiting Time",

        )

        st.plotly_chart(

            wait_chart,

            use_container_width=True,

        )

    st.markdown("---")

    # ==============================
    # Feedback By Date
    # ==============================

    # تجميع عدد التقييمات حسب التاريخ
    feedback_date = (

        df.groupby("Date")

        .size()

        .reset_index(name="Feedback")

    )

    # إنشاء رسم خطي يوضح تغير عدد التقييمات مع الوقت
    line_chart = px.line(

        feedback_date,

        x="Date",

        y="Feedback",

        markers=True,

        title="📈 Feedback Over Time",

    )

    st.plotly_chart(

        line_chart,

        use_container_width=True,

    )

    st.markdown("---")

    # ==============================
    # Data Table
    # ==============================

    # عرض جدول يحتوي على جميع تقييمات العملاء
    st.subheader("📋 All Customer Feedback")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True,

    )

    # إظهار رسالة تؤكد تحميل لوحة التحكم بنجاح
    st.success("Dashboard Loaded Successfully ✅")