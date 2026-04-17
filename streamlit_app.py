import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. إعداد الصفحة (يجب أن يكون أول سطر)
st.set_page_config(page_title="نظام Enterprise الذكي", layout="wide", page_icon="🏢")

# --- محرك التوصيات وتنبيهات قطع الغيار ---
def get_advanced_analysis(details):
    details = str(details).lower()
    analysis = {"advice": "", "part": ""}
    
    if "سير" in details or "ترس" in details:
        analysis["advice"] = "🛠️ فحص قوة الشد، التشحيم، والتأكد من عدم وجود تآكل جانبي."
        analysis["part"] = "سير محرك (V-Belt) أو طقم تروس بديل"
    elif "زيت" in details or "هيدروليك" in details:
        analysis["advice"] = "🛠️ فحص مستوى الضغط، درجة الحرارة، ولزوجة الزيت."
        analysis["part"] = "فلاتر زيت + زيت هيدروليك 46"
    elif "كهرباء" in details or "حساس" in details:
        analysis["advice"] = "🛠️ تنظيف الحساسات بالهواء، وفحص التوصيلات الكهربائية."
        analysis["part"] = "حساس تقارب (Sensor) أو فيوزات تحكم"
    else:
        analysis["advice"] = "🛠️ فحص ميكانيكي شامل وتنظيف الأجزاء المتحركة."
        analysis["part"] = "طقم صيانة دورية (General Kit)"
    return analysis

# 2. نظام الدخول الأمن
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 بوابة الدخول الموحدة</h1>", unsafe_allow_html=True)
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
else:
    # 3. البرنامج الرئيسي بعد الدخول
    st.sidebar.title("💎 Enterprise Pro")
    st.sidebar.markdown(f"المستخدم: **Admin**")
    
    # إدارة الأقسام
    if "sections" not in st.session_state:
        st.session_state.sections = ["الرئيسية", "الصيانة التنبؤية", "الموارد البشرية"]
    
    choice = st.sidebar.radio("انتقل إلى القسم:", st.session_state.sections)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # تهيئة قاعدة البيانات (مؤقتة لحين ربط الشيت)
    if "db" not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["الماكينة", "التاريخ", "الدورة", "التفاصيل"])

    # --- قسم الصيانة التنبؤية ---
    if choice == "الصيانة التنبؤية":
        st.title("🔧 نظام إدارة الأعطال وقطع الغيار")
        
        tab1, tab2 = st.tabs(["🔮 رادار التوقعات", "📝 إضافة سجل جديد"])
        
        with tab1:
            if st.session_state.db.empty:
                st.info("لا توجد ماكينات مسجلة حالياً.")
            else:
                m_cols = st.columns(3)
                for i, row in st.session_state.db.iterrows():
                    # حساب التاريخ والتوقعات
                    dt = pd.to_datetime(row["التاريخ"])
                    target_date = dt + timedelta(days=int(row["الدورة"]))
                    days_left = (target_date - datetime.now()).days
                    
                    analysis = get_advanced_analysis(row["التفاصيل"])
                    
                    with m_cols[i % 3]:
                        if days_left <= 5:
                            st.error(f"🚨 {row['الماكينة']}")
                            st.write(f"**عطل متوقع خلال:** {days_left} يوم")
                            st.warning(analysis["advice"])
                            st.info(f"📦 **تنبيه شراء:** يُنصح بتوفير {analysis['part']}")
                            if st.button(f"تجهيز طلب شراء {i}", help="نسخ نص الطلب"):
                                st.code(f"طلب شراء لـ {row['الماكينة']}: {analysis['part']}")
                        else:
                            st.success(f"✅ {row['الماكينة']}")
                            st.write(f"**الحالة:** مستقرة")
                            st.write(f"**باقي للفحص:** {days_left} يوم")
                        st.divider()

        with tab2:
            st.subheader("إضافة ماكينة لنظام الرقابة")
            with st.form("add_m"):
                name = st.text_input("اسم الماكينة")
                last_d = st.date_input("تاريخ آخر صيانة")
                cycle = st.number_input("دورة الصيانة المتوقعة (أيام)", value=30)
                desc = st.text_area("تفاصيل ما تم في الصيانة السابقة")
                if st.form_submit_button("حفظ الماكينة"):
                    new_data = pd.DataFrame([{"الماكينة": name, "التاريخ": last_d, "الدورة": cycle, "التفاصيل": desc}])
                    st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                    st.success("تم تسجيل الماكينة في نظام التنبؤ!")
                    st.rerun()

    # --- قسم الرئيسية ---
    elif choice == "الرئيسية":
        st.title("📊 لوحة تحكم الإدارة")
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الماكينات", len(st.session_state.db))
        c2.metric("الحالة الأمنية", "محمي ✅")
        c3.metric("تحديثات النظام", "2026")
        st.divider()
        st.subheader("سجل الأصول والماكينات")
        st.dataframe(st.session_state.db, use_container_width=True)

    # --- أي قسم آخر ---
    else:
        st.title(f"📂 {choice}")
        st.write("القسم مفتوح وجاهز لتلقي برمجتك المخصصة.")
        
