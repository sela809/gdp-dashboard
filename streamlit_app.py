import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة الإدارة الذكية", layout="wide", page_icon="🏭")

# 2. تهيئة الذاكرة الشاملة (Session State) - لازم تكون في الأول
if 'machines' not in st.session_state:
    st.session_state.machines = pd.DataFrame([
        {"الماكينة": "ماكينة طباعة 1", "الحالة": "✅ تعمل"},
        {"الماكينة": "مكبس تجميع", "الحالة": "✅ تعمل"}
    ])

if 'production_log' not in st.session_state:
    st.session_state.production_log = pd.DataFrame(columns=["التوقيت", "الماكينة", "الكمية المنتج", "الهالك"])

if 'maintenance_logs' not in st.session_state:
    st.session_state.maintenance_logs = pd.DataFrame(columns=["الماكينة", "نوع الصيانة", "التاريخ", "الفني المسؤول", "التكلفة"])

if 'machine_health' not in st.session_state:
    st.session_state.machine_health = {
        "ماكينة طباعة 1": {"آخر_صيانة": "2026-04-01", "عمر_القطعة_افتراضي": 30},
        "مكبس تجميع": {"آخر_صيانة": "2026-03-15", "عمر_القطعة_افتراضي": 60}
    }

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏭 نظام الإدارة المتكامل (النسخة المصححة)</h1>", unsafe_allow_html=True)

# 3. إنشاء التبويبات مرة واحدة فقط
tabs = st.tabs(["🏠 الرئيسية", "🏗️ مدير الإنتاج", "🔧 مدير الصيانة", "📦 مدير المخزن"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.subheader("📊 تقرير الأداء العام")
    col1, col2 = st.columns(2)
    col1.metric("إجمالي الماكينات", len(st.session_state.machines))
    col2.metric("إجمالي إنتاج اليوم", f"{st.session_state.production_log['الكمية المنتج'].sum()} قطعة")
    st.table(st.session_state.machines)

# --- التبويب 2: مدير الإنتاج ---
with tabs[1]:
    st.header("🏗️ تسجيل الإنتاج اليومي")
    selected_m = st.selectbox("اختر الماكينة:", st.session_state.machines['الماكينة'], key="prod_select")
    p_amount = st.number_input("الكمية المنتجة:", min_value=0, step=1)
    if st.button("➕ تسجيل الإنتاج"):
        new_entry = {"التوقيت": datetime.now().strftime("%H:%M:%S"), "الماكينة": selected_m, "الكمية المنتج": p_amount, "الهالك": 0}
        st.session_state.production_log = pd.concat([st.session_state.production_log, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("تم الحفظ!")

# --- التبويب 3: مدير الصيانة (الرادار + الإدارة) ---
with tabs[2]:
    st.header("🔧 مركز قيادة الصيانة")
    
    # رادار التوقعات
    st.subheader("🔮 توقعات الأعطال")
    m_cols = st.columns(len(st.session_state.machine_health))
    for i, (name, data) in enumerate(st.session_state.machine_health.items()):
        last = datetime.strptime(data["آخر_صيانة"], "%Y-%m-%d")
        next_m = last + timedelta(days=data["عمر_القطعة_افتراضي"])
        days_left = (next_m - datetime.now()).days
        with m_cols[i]:
            if days_left <= 5: st.error(f"⚠️ {name}: صيانة خلال {days_left} يوم")
            else: st.success(f"✅ {name}: مستقرة ({days_left} يوم)")

    # تسجيل صيانة
    with st.expander("📝 تسجيل عملية صيانة"):
        m_fix = st.selectbox("الماكينة:", list(st.session_state.machine_health.keys()), key="fix_select")
        cost = st.number_input("التكلفة:", min_value=0)
        if st.button("💾 حفظ الصيانة"):
            st.session_state.machine_health[m_fix]["آخر_صيانة"] = datetime.now().strftime("%Y-%m-%d")
            st.success("تم تحديث الرادار!")
            st.rerun()

    # إضافة/حذف ماكينات
    with st.expander("⚙️ إعدادات الماكينات (إضافة/تكهين)"):
        new_m = st.text_input("اسم ماكينة جديدة:")
        if st.button("حفظ"):
            # إضافة للجدول وللرادار
            st.session_state.machines = pd.concat([st.session_state.machines, pd.DataFrame([{"الماكينة": new_m, "الحالة": "✅ تعمل"}])], ignore_index=True)
            st.session_state.machine_health[new_m] = {"آخر_صيانة": datetime.now().strftime("%Y-%m-%d"), "عمر_القطعة_افتراضي": 30}
            st.rerun()

# --- التبويب 4: المخزن ---
with tabs[3]:
    st.header("📦 حركة المخازن")
    st.info("قيد التطوير - لربط الخامات بالإنتاج")
        
