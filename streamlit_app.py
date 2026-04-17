import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة (أول سطر دائماً)
st.set_page_config(page_title="Enterprise Pro v3", layout="wide", page_icon="🏢")

# --- محرك التحليل الذكي وتوقعات قطع الغيار ---
def analyze_machine(details):
    details = str(details).lower()
    if "سير" in details or "ترس" in details:
        return "🛠️ التوصية: فحص الشد والتشحيم.", "📦 اطلب: سير محرك / طقم تروس"
    elif "زيت" in details or "فلتر" in details:
        return "🛠️ التوصية: فحص اللزوجة والضغط.", "📦 اطلب: زيت هيدروليك 46 + فلتر"
    elif "كهرباء" in details or "حساس" in details:
        return "🛠️ التوصية: تنظيف الحساسات بالهواء.", "📦 اطلب: حساس تقارب جديد"
    return "🛠️ التوصية: فحص ميكانيكي شامل.", "📦 اطلب: طقم عمرة دورية"

# 2. نظام الدخول الذكي (يقبل Admin و admin)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 نظام الإدارة المركزية</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if u.lower() == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")
else:
    # تهيئة قاعدة البيانات
    if "db" not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])

    # القائمة الجانبية
    st.sidebar.title("💎 Enterprise Pro")
    menu = st.sidebar.radio("القائمة الرئيسية:", ["📊 لوحة التحكم", "🔧 الصيانة التنبؤية", "👥 الموارد البشرية"])
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # --- القسم 1: لوحة التحكم (الرئيسية القوية) ---
    if menu == "📊 لوحة التحكم":
        st.title("📊 حالة المصنع العامة")
        
        # حساب التنبيهات الخطيرة
        danger_list = []
        for i, row in st.session_state.db.iterrows():
            target = pd.to_datetime(row["التاريخ"]) + timedelta(days=int(row["الدورة"]))
            if (target - datetime.now()).days <= 5:
                danger_list.append(row["الماكينة"])

        # صف العدادات
        m1, m2, m3 = st.columns(3)
        m1.metric("إجمالي الماكينات", len(st.session_state.db))
        m2.metric("أعطال وشيكة", len(danger_list), delta="- تنبيه حرج" if danger_list else "مستقر", delta_color="inverse")
        m3.metric("تحديث النظام", "2026")

        st.divider()
        col_table, col_alert = st.columns([2, 1])
        with col_table:
            st.subheader("📋 سجل الأصول المسجلة")
            st.dataframe(st.session_state.db, use_container_width=True)
        with col_alert:
            st.subheader("🔔 الإشعارات الذكية")
            if danger_list:
                for m in danger_list:
                    st.error(f"⚠️ {m}: يحتاج صيانة فورية!")
            else:
                st.success("✅ جميع الأنظمة تعمل بكفاءة")

    # --- القسم 2: الصيانة التنبؤية (الرادار والذكاء) ---
    elif menu == "🔧 الصيانة التنبؤية":
        st.title("🔧 إدارة الأعطال وقطع الغيار")
        t1, t2 = st.tabs(["🔮 رادار التوقعات", "➕ إضافة ماكينة"])
        
        with t1:
            if st.session_state.db.empty:
                st.info("قم بإضافة ماكينة أولاً من التبويب المجاور.")
            else:
                cols = st.columns(3)
                for i, row in st.session_state.db.iterrows():
                    dt = pd.to_datetime(row["التاريخ"])
                    next_fix = dt + timedelta(days=int(row["الدورة"]))
                    days_left = (next_fix - datetime.now()).days
                    advice, part = analyze_machine(row["التفاصيل"])
                    
                    with cols[i % 3]:
                        if days_left <= 5:
                            st.error(f"🛑 {row['الماكينة']}")
                            st.write(f"باقي: {days_left} يوم")
                            st.warning(advice)
                            st.info(part)
                            if st.button(f"طلب شراء {i}"):
                                st.code(f"طلب شراء عاجل لـ {row['الماكينة']}: {part}")
                        else:
                            st.success(f"✅ {row['الماكينة']}")
                            st.write(f"باقي: {days_left} يوم")
                        st.divider()

        with t2:
            with st.form("add_form"):
                name = st.text_input("اسم الماكينة")
                d_date = st.date_input("تاريخ آخر صيانة")
                cycle = st.number_input("دورة الصيانة (أيام)", value=30)
                details = st.text_area("تفاصيل الصيانة السابقة")
                if st.form_submit_button("حفظ في النظام"):
                    new_row = pd.DataFrame([{"الماكينة": name, "التاريخ": d_date, "الدورة": cycle, "التفاصيل": details}])
                    st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
                    st.rerun()
            
