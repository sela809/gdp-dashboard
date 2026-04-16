import streamlit as st

# 1. إعداد الصفحة (لازم يكون أول حاجة)
st.set_page_config(page_title="منظومة الرقابة", layout="wide")

st.markdown("<h1 style='text-align: center; color: #40a9ff;'>📊 لوحة التحكم الشاملة</h1>", unsafe_allow_html=True)

# 2. تعريف التبويبات (عشان البرنامج يعرفهم)
tab1, tab2, tab3 = st.tabs(["🏠 الرئيسية", "📉 إدارة الهالك", "💸 إدارة الديون"])

# 3. محتوى كل تبويب
with tab1:
    st.info("مرحباً بك في لوحة دعم القرار - الإدارة العليا")
    
    # إضافة الأرقام الرئيسية اللي كانت ناقصة
    col1, col2 = st.columns(2)
    col1.metric("صافي الربح اليومي", "125,400 ج.م", "+8%")
    col2.metric("كفاءة الإنتاج", "96%", "+2%")
    
    st.write("---")
    st.subheader("📍 رادار المنشآت اللحظي")
    st.write("هنا تظهر خريطة الأداء العام للمصنع")

with tab2:
    st.header("📉 حساب الهالك اللحظي")
    price = st.number_input("سعر كيلو الخام (ج.م)", value=150)
    waste = st.number_input("كمية الهالك (كيلو)", value=1)
    if st.button("احسب الخسارة"):
        st.error(f"⚠️ المبلغ المهدر: {price * waste} ج.م")

with tab3:
    st.header("💸 نظام المديونيات")
    st.text_input("اسم العميل")
    st.number_input("المبلغ المطلوب", min_value=0)
    st.button("حفظ السجل")
