import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="نظام الشركة المتكامل", layout="wide", page_icon="🏢")

# 2. تهيئة الذاكرة المركزية (قاعدة البيانات المؤقتة)
if 'sections' not in st.session_state:
    st.session_state.sections = ["الرئيسية", "الصيانة", "الإنتاج", "الموارد البشرية (HR)", "المخزن"]

if 'machines_db' not in st.session_state:
    st.session_state.machines_db = pd.DataFrame(columns=["الماكينة", "تاريخ_آخر_صيانة", "الدورة_بالأيام", "تفاصيل"])

# 3. القائمة الجانبية (Sidebar) - دي اللي بتتحكم في "استقلالية" الأقسام
st.sidebar.title("🏢 لوحة تحكم الشركة")
st.sidebar.info(f"مرحباً بك يا {st.session_state.get('user_name', 'المدير')}")

# ميزة إضافة قسم جديد من البرنامج
with st.sidebar.expander("➕ إضافة قسم جديد"):
    new_sec = st.text_input("اسم القسم:")
    if st.button("تفعيل القسم"):
        if new_sec and new_sec not in st.session_state.sections:
            st.session_state.sections.append(new_sec)
            st.success(f"تم إنشاء قسم {new_sec}")
            st.rerun()

# اختيار القسم المراد الدخول إليه
choice = st.sidebar.radio("انتقل إلى القسم:", st.session_state.sections)

# ------------------------------------------------------------------
# 4. محرك الأقسام (كل قسم برنامج مستقل بذاته)
# ------------------------------------------------------------------

# --- قسم الرئيسية ---
if choice == "الرئيسية":
    st.title("📊 مركز العمليات الرئيسي")
    st.write("ملخص أداء جميع أقسام الشركة")
    c1, c2, c3 = st.columns(3)
    c1.metric("الأقسام النشطة", len(st.session_state.sections))
    c2.metric("حالة الإنتاج", "94%", "ممتاز")
    c3.metric("تنبيهات الصيانة", len(st.session_state.machines_db), "-1")

# --- قسم الصيانة (بنفس النظام الذكي اللي طلبته) ---
elif choice == "الصيانة":
    st.title("🔧 نظام الصيانة التنبؤي")
    tab1, tab2 = st.tabs(["🔮 رادار التوقعات", "➕ إدارة الماكينات"])
    
    with tab1:
        if st.session_state.machines_db.empty:
            st.info("لا توجد بيانات. أضف ماكينة من التبويب التالي.")
        else:
            m_cols = st.columns(3)
            for i, row in st.session_state.machines_db.iterrows():
                last_date = datetime.strptime(row["تاريخ_آخر_صيانة"], "%Y-%m-%d")
                next_due = last_date + timedelta(days=int(row["الدورة_بالأيام"]))
                days_left = (next_due - datetime.now()).days
                with m_cols[i % 3]:
                    if days_left <= 3: st.error(f"🚨 {row['الماكينة']}: عطل متوقع خلال {days_left} يوم")
                    else: st.success(f"✅ {row['الماكينة']}: مستقرة ({days_left} يوم)")

    with tab2:
        with st.form("m_form"):
            name = st.text_input("اسم الماكينة:")
            d_date = st.date_input("آخر صيانة:")
            cycle = st.number_input("دورة العطل (أيام):", value=30)
            if st.form_submit_button("حفظ"):
                new_m = {"الماكينة": name, "تاريخ_آخر_صيانة": d_date.strftime("%Y-%m-%d"), "الدورة_بالأيام": cycle, "تفاصيل": "جديدة"}
                st.session_state.machines_db = pd.concat([st.session_state.machines_db, pd.DataFrame([new_m])], ignore_index=True)
                st.rerun()

# --- قسم الموارد البشرية (مثال لقسم آخر مستقل) ---
elif choice == "الموارد البشرية (HR)":
    st.title("👥 إدارة الموارد البشرية")
    st.subheader("سجل الموظفين والرواتب")
    st.table({"الموظف": ["أحمد", "سارة"], "الوظيفة": ["فني صيانة", "محاسب"], "الحالة": ["حاضر", "إجازة"]})

# --- التعامل مع الأقسام الجديدة التي يضيفها المستخدم ---
else:
    st.title(f"📂 قسم {choice}")
    st.info(f"هذا القسم تم إنشاؤه حديثاً. يمكنك الآن البدء في بناء أدواته الخاصة.")
    st.write("نظام القسم قيد التجهيز التلقائي...")
                
