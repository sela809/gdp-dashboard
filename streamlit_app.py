import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات الأمان والخصوصية
st.set_page_config(page_title="Enterprise Pro System", layout="wide", page_icon="🔐")

# --- دالة تسجيل الدخول ---
def check_password():
    def password_entered():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # مسح الباسورد من الذاكرة للأمان
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h1 style='text-align: center;'>🔐 بوابة تسجيل الدخول</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.text_input("اسم المستخدم", key="username")
            st.text_input("كلمة المرور", type="password", key="password")
            st.button("دخول للنظام", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ بيانات الدخول غير صحيحة")
        return False
    else:
        return True

# 2. تشغيل بوابة الأمان
if check_password():
    
    # --- تهيئة الذاكرة (تحدث مرة واحدة بعد الدخول) ---
    if 'sections' not in st.session_state:
        st.session_state.sections = ["الرئيسية", "الصيانة", "الموارد البشرية (HR)", "الإنتاج"]
    
    if 'hr_db' not in st.session_state:
        st.session_state.hr_db = pd.DataFrame([{"الموظف": "أحمد علي", "الوظيفة": "فني", "الحالة": "نشط", "الأداء": 90}])

    if 'machines_db' not in st.session_state:
        st.session_state.machines_db = pd.DataFrame(columns=["الماكينة", "تاريخ_آخر_صيانة", "الدورة_بالأيام", "تفاصيل"])

    # 3. القائمة الجانبية (Sidebar)
    st.sidebar.title("💎 Enterprise Pro")
    st.sidebar.success("تم تسجيل الدخول بنجاح")
    choice = st.sidebar.radio("انتقل إلى القسم:", st.session_state.sections)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- محرك الأقسام الذكي ---
    if choice == "الرئيسية":
        st.title("🏛️ واجهة الإدارة العليا")
        st.info("مرحباً بك في نظام إدارة الأصول والكوادر البشرية.")
        c1, c2, c3 = st.columns(3)
        c1.metric("عدد الأقسام", len(st.session_state.sections))
        c2.metric("موظفين نشطين", len(st.session_state.hr_db))
        c3.metric("تنبيهات الصيانة", len(st.session_state.machines_db))

    elif choice == "الصيانة":
        st.title("🔧 نظام التنبؤ بالأعطال")
        t1, t2 = st.tabs(["🔮 رادار التوقعات", "⚙️ إدارة الماكينات"])
        with t1:
            if st.session_state.machines_db.empty:
                st.info("لا توجد ماكينات. أضف بيانات من التبويب المجاور.")
            else:
                cols = st.columns(3)
                for i, row in st.session_state.machines_db.iterrows():
                    last_date = datetime.strptime(row["تاريخ_آخر_صيانة"], "%Y-%m-%d")
                    next_due = last_date + timedelta(days=int(row["الدورة_بالأيام"]))
                    days_left = (next_due - datetime.now()).days
                    with cols[i % 3]:
                        if days_left <= 3: st.error(f"🚨 {row['الماكينة']}: خطر عطل خلال {days_left} يوم")
                        else: st.success(f"✅ {row['الماكينة']}: مستقرة ({days_left} يوم)")

        with t2:
            with st.form("m_form"):
                name = st.text_input("اسم الماكينة:")
                d_date = st.date_input("آخر صيانة:")
                cycle = st.number_input("دورة العطل المتوقعة (أيام):", value=30)
                details = st.text_area("تفاصيل العمرة الأخيرة:")
                if st.form_submit_button("حفظ"):
                    new_m = {"الماكينة": name, "تاريخ_آخر_صيانة": d_date.strftime("%Y-%m-%d"), "الدورة_بالأيام": cycle, "تفاصيل": details}
                    st.session_state.machines_db = pd.concat([st.session_state.machines_db, pd.DataFrame([new_m])], ignore_index=True)
                    st.rerun()

    elif choice == "الموارد البشرية (HR)":
        st.title("👥 إدارة الموظفين")
        tab_h1, tab_h2 = st.tabs(["📋 السجل", "➕ إضافة/حذف"])
        with tab_h1:
            st.dataframe(st.session_state.hr_db, use_container_width=True)
        with tab_h2:
            with st.form("hr_form"):
                e_name = st.text_input("الاسم:")
                e_job = st.text_input("الوظيفة:")
                if st.form_submit_button("إضافة موظف"):
                    st.session_state.hr_db = pd.concat([st.session_state.hr_db, pd.DataFrame([{"الموظف": e_name, "الوظيفة": e_job, "الحالة": "نشط", "الأداء": 100}])], ignore_index=True)
                    st.rerun()
    
