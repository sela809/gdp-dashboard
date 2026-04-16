import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة الإدارة الذكية", layout="wide", page_icon="🏭")

# 2. إنشاء "الذاكرة" للبرنامج (لحفظ الماكينات والأصناف المضافة)
if 'machines' not in st.session_state:
    st.session_state.machines = pd.DataFrame([
        {"الاسم": "ماكينة طباعة 1", "الحالة": "✅ تعمل", "القسم": "الإنتاج"},
        {"الاسم": "مكبس تجميع", "الحالة": "✅ تعمل", "القسم": "التجميع"}
    ])

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"الصنف": "خام بلاستيك", "الكمية": 500, "الوحدة": "كيلو"}
    ])

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏭 نظام الإدارة المتكامل (نسخة الحفظ الذكي)</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🏗️ مدير الإنتاج", "🔧 مدير الصيانة", "📦 مدير المخزن", "💸 الديون"])

# --- التبويب 1: الرئيسية (تعرض كل ما تم حفظه) ---
with tabs[0]:
    st.subheader("📊 ملخص الأصول والإنتاج")
    col1, col2 = st.columns(2)
    col1.metric("عدد الماكينات المسجلة", len(st.session_state.machines))
    col2.metric("أصناف المخزن", len(st.session_state.inventory))
    
    st.write("---")
    st.write("📍 **قائمة الماكينات الحالية في المصنع:**")
    st.table(st.session_state.machines)

# --- التبويب 2: مدير الإنتاج (إضافة ماكينات جديدة) ---
with tabs[1]:
    st.header("🏗️ إدارة خطوط الإنتاج")
    with st.expander("➕ إضافة ماكينة إنتاج جديدة"):
        new_m_name = st.text_input("اسم الماكينة الجديدة", key="m_prod")
        if st.button("حفظ الماكينة في النظام"):
            new_row = {"الاسم": new_m_name, "الحالة": "✅ تعمل", "القسم": "الإنتاج"}
            st.session_state.machines = pd.concat([st.session_state.machines, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"تم تسجيل {new_m_name} في خطوط الإنتاج")

# --- التبويب 3: مدير الصيانة (إضافة وصيانة) ---
with tabs[2]:
    st.header("🔧 قسم الصيانة")
    # ميزة التكهين (المسح بالبيع أو التخريد)
    st.subheader("⚙️ إدارة الماكينات الحالية")
    m_to_delete = st.selectbox("اختر ماكينة (للبيع أو التكهين):", st.session_state.machines['الاسم'])
    if st.button("🔴 إتمام عملية التكهين/البيع"):
        st.session_state.machines = st.session_state.machines[st.session_state.machines['الاسم'] != m_to_delete]
        st.warning(f"تم إخراج {m_to_delete} من النظام بنجاح")
        st.rerun()

# --- التبويب 4: مدير المخزن (زيادة الأصناف) ---
with tabs[3]:
    st.header("📦 إدارة المخازن")
    with st.expander("➕ إضافة صنف جديد للمخزن"):
        item_name = st.text_input("اسم الخامة")
        item_qty = st.number_input("الكمية المبدئية", min_value=0)
        if st.button("تسجيل صنف مخزني"):
            new_item = {"الصنف": item_name, "الكمية": item_qty, "الوحدة": "كيلو"}
            st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
            st.success(f"تمت إضافة {item_name} للمخزن")
    
    st.write("---")
    st.subheader("📦 الرصيد الحالي")
    st.table(st.session_state.inventory)
