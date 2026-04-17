import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة (أول سطر دائماً)
st.set_page_config(page_title="Enterprise Pro v3.5", layout="wide", page_icon="🏢")

# --- محرك التحليل الذكي وتوقعات قطع الغيار ---
def analyze_machine(details):
    details = str(details).lower()
    if "سير" in details or "ترس" in details:
        return "🛠️ فحص الشد والتشحيم.", "📦 اطلب: سير محرك / طقم تروس"
    elif "زيت" in details or "فلتر" in details:
        return "🛠️ فحص اللزوجة والضغط.", "📦 اطلب: زيت هيدروليك 46 + فلتر"
    elif "كهرباء" in details or "حساس" in details:
        return "🛠️ تنظيف الحساسات بالهواء.", "📦 اطلب: حساس تقارب جديد"
    return "🛠️ فحص ميكانيكي شامل.", "📦 اطلب: طقم عمرة دورية"

# 2. نظام الدخول الذكي
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
    # تهيئة قواعد البيانات (لو مش موجودة)
    if "db" not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])
    if "hr_db" not in st.session_state:
        st.session_state.hr_db = pd.DataFrame(columns=["الموظف", "القسم", "الحالة", "الراتب"])
    if "prod_db" not in st.session_state:
        st.session_state.prod_db = pd.DataFrame(columns=["اليوم", "المنتج", "الكمية", "الهالك"])

    # القائمة الجانبية
    st.sidebar.title("💎 Enterprise Pro")
    menu = st.sidebar.radio("القائمة الرئيسية:", ["📊 لوحة التحكم", "🔧 الصيانة التنبؤية", "👥 الموارد البشرية", "🏭 خط الإنتاج"])
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # --- القسم 1: لوحة التحكم (Dashboard) ---
    if menu == "📊 لوحة التحكم":
        st.title("📊 ملخص أداء الشركة")
        
        # حسابات سريعة
        danger_count = 0
        for i, row in st.session_state.db.iterrows():
            target = pd.to_datetime(row["التاريخ"]) + timedelta(days=int(row["الدورة"]))
            if (target - datetime.now()).days <= 5: danger_count += 1

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("إجمالي الماكينات", len(st.session_state.db))
        c2.metric("تنبيهات صيانة", danger_count, delta="- عاجل" if danger_count > 0 else "مستقر", delta_color="inverse")
        c3.metric("عدد الموظفين", len(st.session_state.hr_db))
        c4.metric("إنتاج اليوم", f"{st.session_state.prod_db['الكمية'].sum() if not st.session_state.prod_db.empty else 0} قطعة")

        st.divider()
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("📋 حالة الإنتاج الأخيرة")
            st.table(st.session_state.prod_db.tail(5))
        with col_right:
            st.subheader("🔔 تنبيهات الإدارة")
            if danger_count > 0: st.error(f"يوجد {danger_count} ماكينة تقترب من العطل!")
            else: st.success("جميع الأقسام تعمل بشكل طبيعي.")

    # --- القسم 2: الصيانة التنبؤية ---
    elif menu == "🔧 الصيانة التنبؤية":
        st.title("🔧 إدارة الأعطال")
        t1, t2 = st.tabs(["🔮 الرادار", "➕ إضافة"])
        with t1:
            if st.session_state.db.empty: st.info("لا توجد بيانات.")
            else:
                cols = st.columns(3)
                for i, row in st.session_state.db.iterrows():
                    dt = pd.to_datetime(row["التاريخ"])
                    days_left = (dt + timedelta(days=int(row["الدورة"])) - datetime.now()).days
                    advice, part = analyze_machine(row["التفاصيل"])
                    with cols[i % 3]:
                        if days_left <= 5:
                            st.error(f"🛑 {row['الماكينة']}")
                            st.warning(advice)
                            st.info(part)
                        else: st.success(f"✅ {row['الماكينة']} (باقي {days_left} يوم)")
        with t2:
            with st.form("add_m"):
                name = st.text_input("الماكينة")
                d = st.date_input("آخر صيانة")
                c = st.number_input("الدورة", value=30)
                desc = st.text_area("التفاصيل")
                if st.form_submit_button("حفظ"):
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([{"الماكينة": name, "التاريخ": d, "الدورة": c, "التفاصيل": desc}])], ignore_index=True)
                    st.rerun()

    # --- القسم 3: الموارد البشرية (HR) ---
    elif menu == "👥 الموارد البشرية":
        st.title("👥 إدارة شؤون العاملين")
        with st.form("add_hr"):
            col_h1, col_h2 = st.columns(2)
            name_hr = col_h1.text_input("اسم الموظف")
            dept_hr = col_h2.selectbox("القسم", ["الإنتاج", "الصيانة", "الإدارة", "المخازن"])
            salary_hr = col_h1.number_input("الراتب الأساسي", value=5000)
            status_hr = col_h2.radio("الحالة", ["على رأس العمل", "إجازة"])
            if st.form_submit_button("إضافة موظف"):
                st.session_state.hr_db = pd.concat([st.session_state.hr_db, pd.DataFrame([{"الموظف": name_hr, "القسم": dept_hr, "الحالة": status_hr, "الراتب": salary_hr}])], ignore_index=True)
                st.success("تم تسجيل الموظف")
        st.dataframe(st.session_state.hr_db, use_container_width=True)

    # --- القسم 4: الإنتاج ---
    elif menu == "🏭 خط الإنتاج":
        st.title("🏭 متابعة سجل الإنتاج")
        with st.form("add_prod"):
            p_date = st.date_input("اليوم")
            p_name = st.text_input("اسم المنتج")
            p_qty = st.number_input("الكمية المنتجة", value=100)
            p_waste = st.number_input("الهالك", value=0)
            if st.form_submit_button("تسجيل الإنتاج"):
                st.session_state.prod_db = pd.concat([st.session_state.prod_db, pd.DataFrame([{"اليوم": p_date, "المنتج": p_name, "الكمية": p_qty, "الهالك": p_waste}])], ignore_index=True)
                st.rerun()
        st.line_chart(st.session_state.prod_db.set_index("اليوم")["الكمية"])
