import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة التنبؤ بالأعطال", layout="wide", page_icon="🔧")

# 2. تهيئة مخزن البيانات الذكي (Session State)
if 'machines_db' not in st.session_state:
    # قاعدة بيانات الماكينات (الاسم، تاريخ آخر صيانة، دورة الصيانة بالأيام، وصف ما تم عمله)
    st.session_state.machines_db = pd.DataFrame(columns=["الماكينة", "تاريخ_آخر_صيانة", "الدورة_بالأيام", "تفاصيل_آخر_عمرة"])

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #E64A19;'>🛠️ نظام التنبؤ بالأعطال الذكي</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🚀 رادار التوقعات", "➕ إضافة/تحديث ماكينة", "📊 سجل الصيانة العام"])

# --- التبويب الأول: رادار التوقعات (الذكاء الصناعي للمصنع) ---
with tabs[0]:
    st.subheader("🔮 التحليل الاستباقي للأعطال")
    if st.session_state.machines_db.empty:
        st.info("لا توجد ماكينات مسجلة حالياً. ابدأ بإضافة ماكينة من التبويب التالي.")
    else:
        m_cols = st.columns(3)
        for i, row in st.session_state.machines_db.iterrows():
            # حساب تاريخ الصيانة القادم
            last_date = datetime.strptime(row["تاريخ_آخر_صيانة"], "%Y-%m-%d")
            next_due = last_date + timedelta(days=int(row["الدورة_بالأيام"]))
            days_left = (next_due - datetime.now()).days
            
            with m_cols[i % 3]:
                with st.container():
                    st.markdown(f"### ⚙️ {row['الماكينة']}")
                    if days_left <= 3:
                        st.error(f"🚨 **حالة حرجة!**\n\nتوقع عطل خلال: {days_left} يوم")
                        st.markdown(f"**توصية:** يجب فحص السير والزيوت فوراً (بناءً على عمرة {row['تاريخ_آخر_صيانة']})")
                    elif days_left <= 7:
                        st.warning(f"⚠️ **انتباه!**\n\nموعد الصيانة يقترب: {days_left} يوم")
                    else:
                        st.success(f"✅ **مستقرة**\n\nباقي {days_left} يوم على الفحص الدوري")
                    
                    st.caption(f"آخر عملية: {row['تفاصيل_آخر_عمرة']}")

# --- التبويب الثاني: إضافة أو تحديث ماكينة (المدخلات) ---
with tabs[1]:
    st.header("📝 إدخال بيانات الأصول")
    with st.form("add_machine_form"):
        col1, col2 = st.columns(2)
        with col1:
            m_name = st.text_input("اسم الماكينة (مثلاً: ماكينة طباعة هيدروليك)")
            last_m_date = st.date_input("تاريخ آخر صيانة تمت بالفعل", datetime.now())
        with col2:
            m_cycle = st.number_input("دورة الصيانة المقترحة (كل كم يوم تعطل؟)", min_value=1, value=30)
            m_details = st.text_area("ماذا تم في آخر صيانة؟ (مثلاً: تغيير بلي، تشحيم، تغيير زيت)")
        
        submit = st.form_submit_button("💾 حفظ الماكينة في نظام التوقعات")
        
        if submit:
            new_data = {
                "الماكينة": m_name,
                "تاريخ_آخر_صيانة": last_m_date.strftime("%Y-%m-%d"),
                "الدورة_بالأيام": m_cycle,
                "تفاصيل_آخر_عمرة": m_details
            }
            # لو الماكينة موجودة نحدثها، لو مش موجودة نضيفها
            if m_name in st.session_state.machines_db["الماكينة"].values:
                st.session_state.machines_db = st.session_state.machines_db[st.session_state.machines_db["الماكينة"] != m_name]
            
            st.session_state.machines_db = pd.concat([st.session_state.machines_db, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"تم تسجيل {m_name}. النظام بدأ الآن بمراقبة حالتها!")

# --- التبويب الثالث: سجل الصيانة (الأرشيف) ---
with tabs[2]:
    st.subheader("📂 أرشيف الماكينات المسجلة")
    st.dataframe(st.session_state.machines_db, use_container_width=True)
