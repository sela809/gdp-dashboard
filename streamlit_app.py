import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة
st.set_page_config(page_title="Enterprise Pro", layout="wide")

# 2. نظام الدخول المعدل (يقبل admin أو Admin)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 بوابة الدخول</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            # التأكد من المسافات هنا (أهم خطوة)
            if user.lower() == "admin" and pw == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول خطأ!")
else:
    # 3. واجهة البرنامج الرئيسية (Dashboard)
    if "db" not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])
    
    st.sidebar.title("💎 Enterprise Pro")
    choice = st.sidebar.radio("القائمة:", ["الرئيسية", "الصيانة التنبؤية"])

    if choice == "الرئيسية":
        st.title("📊 لوحة تحكم الإدارة")
        # الإحصائيات
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الماكينات", len(st.session_state.db))
        c2.metric("الحالة", "متصل ✅")
        c3.metric("التنبيهات", "جاهز")
        st.divider()
        st.subheader("📋 سجل العمليات الجاري")
        st.table(st.session_state.db)

    elif choice == "الصيانة التنبؤية":
        st.title("🔧 إدارة الأعطال")
        # حط هنا كود الصيانة اللي فات مع التأكد من المسافات
        st.write("القسم جاهز لإضافة الماكينات.")

    if st.sidebar.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
        
