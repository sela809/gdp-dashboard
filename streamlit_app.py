import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة
st.set_page_config(page_title="Enterprise Pro", layout="wide", page_icon="🏢")

# --- محركات البحث والتحليل ---
def get_advanced_analysis(details):
    details = str(details).lower()
    analysis = {"advice": "", "part": ""}
    if "سير" in details:
        analysis["advice"] = "🛠️ افحص قوة الشد والتشحيم."
        analysis["part"] = "سير محرك أصلي"
    elif "زيت" in details:
        analysis["advice"] = "🛠️ افحص اللزوجة ومستوى الضغط."
        analysis["part"] = "زيت هيدروليك + فلتر"
    else:
        analysis["advice"] = "🛠️ فحص دوري شامل."
        analysis["part"] = "طقم صيانة عامة"
    return analysis

# 2. نظام الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 بوابة الدخول</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("المستخدم")
        pw = st.text_input("الكلمة", type="password")
        if st.button("دخول"):
            if user == "admin" and pw == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات خطأ")
else:
    # تهيئة البيانات
    if "db" not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])
    
    # القائمة الجانبية
    st.sidebar.title("💎 Enterprise Pro")
    choice = st.sidebar.radio("القائمة:", ["الرئيسية", "الصيانة التنبؤية", "الموارد البشرية"])

    # --- قسم الرئيسية (الواجهة الجديدة) ---
    if choice == "الرئيسية":
        st.title("📊 لوحة تحكم الإدارة العليا")
        st.markdown(f"**مرحباً بك يا مدير.. إليك ملخص حالة المصنع اليوم {datetime.now().date()}**")
        st.divider()

        # صف الإحصائيات السريعة
        c1, c2, c3, c4 = st.columns(4)
        
        # حساب عدد التنبيهات الخطيرة
        danger_count = 0
        for i, row in st.session_state.db.iterrows():
            target = pd.to_datetime(row["التاريخ"]) + timedelta(days=int(row["الدورة"]))
            if (target - datetime.now()).days <= 5:
                danger_count += 1

        with c1:
            st.metric("إجمالي الماكينات", len(st.session_state.db))
        with c2:
            st.metric("تنبيهات حرجة", danger_count, delta_color="inverse", delta=f"{danger_count} عطل متوقع")
        with c3:
            st.metric("حالة الأقسام", "4 نشطة")
        with c4:
            st.metric("كفاءة التشغيل", "98%")

        st.divider()

        # عرض سريع للرادار في الرئيسية
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("📋 ملخص سجل الأصول")
            st.dataframe(st.session_state.db, use_container_width=True)
            
        with col_right:
            st.subheader("🔔 أهم التنبيهات")
            if danger_count > 0:
                st.warning(f"يوجد {danger_count} ماكينة تحتاج تدخل فوري وتوفير قطع غيار.")
            else:
                st.success("جميع الماكينات في حالة مستقرة حالياً.")

    # --- قسم الصيانة (نفس الكود القوي) ---
    elif choice == "الصيانة التنبؤية":
        st.title("🔧 نظام إدارة الأعطال")
        tab1, tab2 = st.tabs(["🔮 رادار التوقعات", "📝 إضافة سجل"])
        
        with tab1:
            if st.session_state.db.empty:
                st.info("لا توجد بيانات.")
            else:
                m_cols = st.columns(3)
                for i, row in st.session_state.db.iterrows():
                    dt = pd.to_datetime(row["التاريخ"])
                    rem = (dt + timedelta(days=int(row["الدورة"])) - datetime.now()).days
                    analysis = get_advanced_analysis(row["التفاصيل"])
                    with m_cols[i % 3]:
                        if rem <= 5:
                            st.error(f"🚨 {row['الماكينة']}")
                            st.info(f"📦 اطلب: {analysis['part']}")
                        else:
                            st.success(f"✅ {row['الماكينة']} (باقي {rem} يوم)")

        with tab2:
            with st.form("add"):
                n = st.text_input("اسم الماكينة")
                d = st.date_input("آخر صيانة")
                c = st.number_input("الدورة", value=30)
                t = st.text_area("التفاصيل")
                if st.form_submit_button("حفظ"):
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([{"الماكينة": n, "التاريخ": d, "الدورة": c, "التفاصيل": t}])], ignore_index=True)
                    st.rerun()

    if st.sidebar.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
                      
