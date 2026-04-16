import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. إعدادات الصفحة (يجب أن يكون أول سطر)
st.set_page_config(page_title="نظام Enterprise الذكي", layout="wide", page_icon="🔐")

# 2. بوابة تسجيل الدخول (Username: admin | PW: 123)
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🔐 دخول النظام المركزي</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user = st.text_input("اسم المستخدم")
            pw = st.text_input("كلمة المرور", type="password")
            if st.button("دخول للنظام"):
                if user == "admin" and pw == "123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")
        return False
    return True

# 3. محرك التوصيات الذكي للصيانة
def get_maintenance_advice(machine_name, last_fix_details):
    details = str(last_fix_details).lower()
    if "سير" in details or "ترس" in details or "بلي" in details:
        return "🛠️ التوصية المسبقة: فحص مستويات التشحيم، ضبط توتر السيور، والتأكد من عدم وجود ضجيج في كراسي التحميل."
    elif "زيت" in details or "فلتر" in details or "هيدروليك" in details:
        return "🛠️ التوصية المسبقة: فحص لزوجة الزيت، تنظيف الفلاتر، والتأكد من عدم وجود تسريب في الخراطيم."
    elif "كهرباء" in details or "حساس" in details or "سلك" in details:
        return "🛠️ التوصية المسبقة: تنظيف اللوحة الكهربائية بضغط الهواء، فحص جودة التوصيلات، ومعايرة الحساسات."
    else:
        return "🛠️ التوصية المسبقة: فحص هيكلي شامل، تنظيف الماكينة من الرايش، والتأكد من سلامة وسائل الأمان."

# 4. تشغيل النظام
if login():
    # الربط بجوجل شيتس
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # استبدل الرابط أدناه برابط ملفك الفعلي
        df = conn.read(spreadsheet="رابط_ملف_جوجل_شيتس_هنا", worksheet="Sheet1")
    except:
        st.error("فشل الاتصال بجوجل شيتس. تأكد من الرابط وصلاحيات الوصول.")
        df = pd.DataFrame(columns=["الماكينة", "تاريخ_آخر_صيانة", "الدورة_بالأيام", "تفاصيل"])

    # القائمة الجانبية
    st.sidebar.title("🏢 لوحة تحكم الشركة")
    sections = ["الرئيسية", "الصيانة التنبؤية", "الموارد البشرية", "إعدادات الأقسام"]
    choice = st.sidebar.radio("انتقل إلى:", sections)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # --- القسم: الرئيسية ---
    if choice == "الرئيسية":
        st.title("📊 مركز العمليات الرئيسي")
        c1, c2 = st.columns(2)
        c1.metric("إجمالي الماكينات", len(df))
        c2.metric("حالة النظام", "متصل ✅")
        st.write("---")
        st.subheader("📍 نظرة عامة على الأصول")
        st.dataframe(df, use_container_width=True)

    # --- القسم: الصيانة التنبؤية ---
    elif choice == "الصيانة التنبؤية":
        st.title("🔧 نظام التنبؤ بالأعطال الذكي")
        
        tab1, tab2 = st.tabs(["🔮 رادار التوقعات", "➕ إضافة سجل جديد"])
        
        with tab1:
            if df.empty:
                st.info("لا توجد بيانات مسجلة في جوجل شيتس.")
            else:
                m_cols = st.columns(3)
                for i, row in df.iterrows():
                    # حساب التاريخ
                    last_date = pd.to_datetime(row["تاريخ_آخر_صيانة"])
                    next_due = last_date + timedelta(days=int(row["الدورة_بالأيام"]))
                    days_left = (next_due - datetime.now()).days
                    
                    with m_cols[i % 3]:
                        st.markdown(f"### ⚙️ {row['الماكينة']}")
                        if days_left <= 5:
                            st.error(f"🛑 خطر عطل متوقع خلال {days_left} يوم!")
                            advice = get_maintenance_advice(row['الماكينة'], row['تفاصيل'])
                            st.warning(advice)
                        else:
                            st.success(f"✅ مستقرة (باقي {days_left} يوم)")
                        st.caption(f"آخر عمرة: {row['تفاصيل']}")
                        st.write("---")

        with tab2:
            st.subheader("📝 تسجيل صيانة جديدة في السحابة")
            with st.form("add_to_sheets"):
                name = st.text_input("اسم الماكينة")
                d_date = st.date_input("تاريخ الصيانة")
                cycle = st.number_input("دورة العطل (بالأيام)", value=30)
                details = st.text_area("ماذا تم في الصيانة؟ (سير، زيت، كهرباء...)")
                
                if st.form_submit_button("حفظ البيانات للأبد"):
                    new_row = pd.DataFrame([{
                        "الماكينة": name, 
                        "تاريخ_آخر_صيانة": d_date.strftime("%Y-%m-%d"), 
                        "الدورة_بالأيام": cycle, 
                        "تفاصيل": details
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet="رابط_ملف_جوجل_شيتس_هنا", data=updated_df)
                    st.success("تم التحديث بنجاح في جوجل شيتس! 🚀")
                    st.rerun()

    # --- باقي الأقسام ---
    else:
        st.title(f"📂 قسم {choice}")
        st.info("هذا القسم قيد البرمجة المخصصة حسب طلب العميل.")
                        
