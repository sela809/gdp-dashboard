import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. تهيئة بيانات الصيانة في الذاكرة
if 'maintenance_logs' not in st.session_state:
    st.session_state.maintenance_logs = pd.DataFrame(columns=["الماكينة", "نوع الصيانة", "التاريخ", "الفني المسؤول", "التكلفة"])

# 2. بيانات افتراضية لتوقعات الأعطال (تجريبي)
if 'machine_health' not in st.session_state:
    st.session_state.machine_health = {
        "ماكينة طباعة 1": {"آخر_صيانة": "2026-04-01", "عمر_القطعة_افتراضي": 30, "حالة_السير": 85},
        "مكبس تجميع": {"آخر_صيانة": "2026-03-15", "عمر_القطعة_افتراضي": 60, "حالة_السير": 40}
    }

# --- داخل تبويب مدير الصيانة ---
with tabs[2]:
    st.header("🔧 مركز قيادة الصيانة الذكي")
    
    # أولاً: رادار توقع الأعطال (Predictive Maintenance)
    st.subheader("🔮 رادار توقع الأعطال (تحليل ذكي)")
    cols = st.columns(len(st.session_state.machine_health))
    
    for i, (m_name, m_data) in enumerate(st.session_state.machine_health.items()):
        last_date = datetime.strptime(m_data["آخر_صيانة"], "%2026-%m-%d")
        next_date = last_date + timedelta(days=m_data["عمر_القطعة_افتراضي"])
        days_left = (next_date - datetime.now()).days
        
        with cols[i]:
            if days_left <= 5:
                st.error(f"⚠️ {m_name}\n\nخطر: صيانة مطلوبة خلال {days_left} أيام!")
            else:
                st.success(f"✅ {m_name}\n\nمستقرة: فاضل {days_left} يوم")

    st.write("---")

    # ثانياً: تسجيل صيانة جديدة
    st.subheader("📝 تسجيل عملية صيانة/تصليح")
    col_a, col_b = st.columns(2)
    with col_a:
        m_select = st.selectbox("الماكينة:", list(st.session_state.machine_health.keys()))
        m_type = st.radio("نوع العملية:", ["صيانة دورية", "إصلاح عطل طارئ", "تغيير قطع غيار"])
    with col_b:
        m_tech = st.text_input("الفني المسؤول:")
        m_cost = st.number_input("تكلفة قطع الغيار (ج.م):", min_value=0)

    if st.button("💾 حفظ في سجل الصيانة"):
        new_log = {
            "الماكينة": m_select,
            "نوع الصيانة": m_type,
            "التاريخ": datetime.now().strftime("%Y-%m-%d"),
            "الفني المسؤول": m_tech,
            "التكلفة": m_cost
        }
        st.session_state.maintenance_logs = pd.concat([st.session_state.maintenance_logs, pd.DataFrame([new_log])], ignore_index=True)
        # تحديث تاريخ آخر صيانة في الرادار
        st.session_state.machine_health[m_select]["آخر_صيانة"] = datetime.now().strftime("%Y-%m-%d")
        st.success(f"تم تحديث بيانات {m_select} بنجاح!")

    st.write("---")
    
    # ثالثاً: سجل الصيانة التاريخي
    st.subheader("📜 أرشيف الصيانة والتكاليف")
    st.dataframe(st.session_state.maintenance_logs, use_container_width=True)
    
    # رابعاً: إحصائية لمدير الصيانة
    total_m_cost = st.session_state.maintenance_logs["التكلفة"].sum()
    st.metric("إجمالي إنفاق الصيانة هذا الشهر", f"{total_m_cost} ج.م")
    
