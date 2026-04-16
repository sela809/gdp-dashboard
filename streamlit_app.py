import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة - لازم أول سطر
st.set_page_config(page_title="Enterprise Pro", layout="wide")

# 2. التأكد من وجود المكتبة لتجنب الـ Error
try:
    from streamlit_gsheets import GSheetsConnection
    HAS_GSHEETS = True
except ImportError:
    HAS_GSHEETS = False

# 3. نظام الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول")
    col1, col2 = st.columns([2,1])
    with col1:
        user = st.text_input("اسم المستخدم (admin)")
        pw = st.text_input("كلمة المرور (123)", type="password")
        if st.button("دخول للنظام"):
            if user == "admin" and pw == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات خطأ!")
else:
    # 4. البرنامج الرئيسي
    st.sidebar.success("تم الاتصال")
    page = st.sidebar.radio("القسم", ["الرئيسية", "الصيانة التنبؤية"])

    # محرك التوصيات
    def get_advice(details):
        details = str(details).lower()
        if "زيت" in details: return "💡 افحص اللزوجة والفلتر."
        if "سير" in details: return "💡 افحص الشد والتاكل."
        return "💡 فحص دوري شامل."

    if page == "الصيانة التنبؤية":
        st.header("🔧 رادار الأعطال الذكي")
        
        # إذا كانت المكتبة لسه مش شغالة، نستخدم ذاكرة مؤقتة عشان "نلحق" الشغل
        if "temp_db" not in st.session_state:
            st.session_state.temp_db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])

        with st.expander("➕ إضافة سجل صيانة"):
            with st.form("add_form"):
                n = st.text_input("اسم الماكينة")
                d = st.date_input("تاريخ آخر صيانة")
                c = st.number_input("الدورة بالأيام", value=30)
                t = st.text_area("تفاصيل (زيت، سير، إلخ)")
                if st.form_submit_button("حفظ"):
                    new_r = pd.DataFrame([{"الماكينة": n, "التاريخ": d, "الدورة": c, "التفاصيل": t}])
                    st.session_state.temp_db = pd.concat([st.session_state.temp_db, new_r], ignore_index=True)
                    st.success("تم الحفظ مؤقتاً لحين ربط الشيت!")
                    st.rerun()

        # عرض التوقعات
        cols = st.columns(3)
        for i, row in st.session_state.temp_db.iterrows():
            dt = pd.to_datetime(row["التاريخ"])
            target = dt + timedelta(days=int(row["الدورة"]))
            rem = (target - datetime.now()).days
            
            with cols[i % 3]:
                if rem <= 5:
                    st.error(f"🛑 {row['الماكينة']}: عطل خلال {rem} يوم")
                    st.info(get_advice(row['التفاصيل']))
                else:
                    st.success(f"✅ {row['الماكينة']}: مستقرة ({rem} يوم)")

    elif page == "الرئيسية":
        st.title("📊 حالة أصول الشركة")
        st.write("البيانات ستظهر هنا من واقع السجل.")
