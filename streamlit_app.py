import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات المتجر والشركة
st.set_page_config(page_title="نظام Enterprise الذكي", layout="wide", page_icon="💎")

# 2. تهيئة قواعد البيانات (الذاكرة الديناميكية)
if 'sections' not in st.session_state:
    st.session_state.sections = ["الرئيسية", "الصيانة", "الموارد البشرية (HR)", "الإنتاج"]

if 'hr_db' not in st.session_state:
    st.session_state.hr_db = pd.DataFrame([
        {"الموظف": "أحمد علي", "الوظيفة": "فني", "الحالة": "نشط", "الأداء": 90}
    ])

if 'machines_db' not in st.session_state:
    st.session_state.machines_db = pd.DataFrame(columns=["الماكينة", "تاريخ_آخر_صيانة", "الدورة_بالأيام", "الحالة"])

# 3. القائمة الجانبية (لوحة التحكم)
st.sidebar.title("💎 Enterprise Pro")
st.sidebar.markdown("---")
choice = st.sidebar.radio("انتقل إلى القسم:", st.session_state.sections)

# ميزة إضافة قسم جديد (التوسع التجاري)
with st.sidebar.expander("🛠️ إعدادات النظام"):
    new_sec = st.text_input("إضافة قسم جديد:")
    if st.button("تفعيل القسم"):
        if new_sec and new_sec not in st.session_state.sections:
            st.session_state.sections.append(new_sec)
            st.rerun()

# ---------------------------------------------------------
# 4. الأقسام التشغيلية
# ---------------------------------------------------------

# --- قسم الموارد البشرية (HR) ---
if choice == "الموارد البشرية (HR)":
    st.title("👥 إدارة رأس المال البشري")
    t1, t2 = st.tabs(["📋 سجل الموظفين", "⚙️ إدارة البيانات"])
    
    with t1:
        st.subheader("تحليل القوى العاملة")
        # حساب الركود الوظيفي (مثال: من أداؤه أقل من 50)
        low_perf = st.session_state.hr_db[st.session_state.hr_db['الأداء'] < 50]
        st.metric("عدد الموظفين", len(st.session_state.hr_db))
        st.dataframe(st.session_state.hr_db, use_container_width=True)
        if not low_perf.empty:
            st.warning(f"⚠️ تنبيه: يوجد {len(low_perf)} موظفين في حالة ركود وظيفي!")

    with t2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("➕ إضافة موظف")
            with st.form("hr_add"):
                name = st.text_input("اسم الموظف")
                job = st.text_input("المسمى الوظيفي")
                perf = st.slider("تقييم الأداء", 0, 100, 80)
                if st.form_submit_button("حفظ"):
                    new_emp = {"الموظف": name, "الوظيفة": job, "الحالة": "نشط", "الأداء": perf}
                    st.session_state.hr_db = pd.concat([st.session_state.hr_db, pd.DataFrame([new_emp])], ignore_index=True)
                    st.rerun()
        with col2:
            st.subheader("🗑️ حذف/تعديل")
            to_del = st.selectbox("اختر موظف:", st.session_state.hr_db['الموظف'])
            if st.button("حذف الموظف نهائياً"):
                st.session_state.hr_db = st.session_state.hr_db[st.session_state.hr_db['الموظف'] != to_del]
                st.rerun()

# --- قسم الصيانة (الرادار التنبؤي) ---
elif choice == "الصيانة":
    st.title("🔧 مركز الصيانة الذكي")
    # (هنا نضع كود الصيانة التنبؤي السابق مع إضافة أزرار الحذف والتعديل بنفس منطق الـ HR)
    st.info("النظام يراقب الأعطال الآن بناءً على مدخلاتك.")
    # ... كود الصيانة المطور ...

# --- قسم الرئيسية ---
else:
    st.title("🏛️ واجهة الإدارة العليا")
    st.write(f"أهلاً بك في نظام إدارة شركة **{choice}**")
    st.image("https://via.placeholder.com/800x200.png?text=Company+Overview+Dashboard")
                    
