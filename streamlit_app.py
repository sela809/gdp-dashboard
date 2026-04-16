import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة الإدارة الذكية", layout="wide", page_icon="🏭")

# 2. تهيئة الذاكرة (Session State)
if 'machines' not in st.session_state:
    st.session_state.machines = pd.DataFrame([
        {"الماكينة": "ماكينة طباعة 1", "الحالة": "✅ تعمل"},
        {"الماكينة": "مكبس تجميع", "الحالة": "✅ تعمل"}
    ])

if 'production_log' not in st.session_state:
    st.session_state.production_log = pd.DataFrame(columns=["التوقيت", "الماكينة", "الكمية المنتج", "الهالك"])

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏭 نظام توزيع الأدوار والرقابة</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🏗️ مدير الإنتاج", "🔧 مدير الصيانة", "📦 مدير المخزن"])

# --- التبويب 1: الرئيسية (عرض شامل) ---
with tabs[0]:
    st.subheader("📊 تقرير الأداء العام")
    col1, col2 = st.columns(2)
    col1.metric("إجمالي الماكينات", len(st.session_state.machines))
    col2.metric("إجمالي إنتاج اليوم", f"{st.session_state.production_log['الكمية المنتج'].sum()} قطعة")
    
    st.write("---")
    st.write("📍 **حالة الماكينات الآن:**")
    st.table(st.session_state.machines)

# --- التبويب 2: مدير الإنتاج (زيادة الإنتاج فقط) ---
with tabs[1]:
    st.header("🏗️ تسجيل الإنتاج اليومي")
    # مدير الإنتاج بيختار من الماكينات اللي ضافها مدير الصيانة
    selected_m = st.selectbox("اختر الماكينة التي أنتجت:", st.session_state.machines['الماكينة'])
    p_amount = st.number_input("الكمية المنتجة (قطعة):", min_value=0, step=1)
    p_waste = st.number_input("كمية الهالك (قطعة):", min_value=0, step=1)
    
    if st.button("➕ تسجيل الإنتاج"):
        new_entry = {
            "التوقيت": pd.Timestamp.now().strftime("%H:%M:%S"),
            "الماكينة": selected_m,
            "الكمية المنتج": p_amount,
            "الهالك": p_waste
        }
        st.session_state.production_log = pd.concat([st.session_state.production_log, pd.DataFrame([new_entry])], ignore_index=True)
        st.success(f"تم تسجيل إنتاج {p_amount} قطعة من {selected_m}")

    st.write("---")
    st.subheader("📋 سجل الإنتاج الأخير")
    st.dataframe(st.session_state.production_log)

# --- التبويب 3: مدير الصيانة (إضافة/تكهين الماكينات) ---
with tabs[2]:
    st.header("🔧 إدارة الأصول (الماكينات)")
    
    with st.expander("➕ إضافة ماكينة جديدة للمصنع"):
        m_name = st.text_input("اسم الماكينة (مثلاً: ماكينة 5)")
        if st.button("حفظ الماكينة"):
            new_m = {"الماكينة": m_name, "الحالة": "✅ تعمل"}
            st.session_state.machines = pd.concat([st.session_state.machines, pd.DataFrame([new_m])], ignore_index=True)
            st.success(f"تمت إضافة {m_name} للنظام")
            st.rerun()

    st.write("---")
    with st.expander("🔴 بيع أو تكهين ماكينة"):
        m_to_del = st.selectbox("اختر ماكينة للإزالة:", st.session_state.machines['الماكينة'])
        if st.button("تأكيد الإزالة النهائية"):
            st.session_state.machines = st.session_state.machines[st.session_state.machines['الماكينة'] != m_to_del]
            st.warning(f"تم حذف {m_to_del} من النظام")
            st.rerun()

# --- التبويب 4: مدير المخزن ---
with tabs[3]:
    st.header("📦 حركة المخازن")
    st.info("هنا يتم ربط استهلاك الخامات بالإنتاج (قيد التطوير)")
