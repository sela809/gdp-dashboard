import streamlit as st

with tab1:
    st.info("مرحباً بك في لوحة دعم القرار - الإدارة العليا")
    
    # إضافة الأرقام الرئيسية في وش الصفحة
    col1, col2 = st.columns(2)
    col1.metric("صافي الربح اليومي", "125,400 ج.م", "+8%")
    col2.metric("كفاءة الإنتاج", "96%", "+2%")
    
    st.write("---")
    st.subheader("📍 رادار المنشآت اللحظي")
    # هنا ممكن ترسم الجدول اللي كان بيظهر زمان

# إعداد الصفحة
st.set_page_config(page_title="منظومة الرقابة", layout="wide")

st.markdown("<h1 style='text-align: center; color: #40a9ff;'>📊 لوحة التحكم الشاملة</h1>", unsafe_allow_html=True)

# عمل "تبويبات" أو أزرار للتنقل في نفس الصفحة
tab1, tab2, tab3 = st.tabs(["🏠 الرئيسية", "📉 إدارة الهالك", "💸 إدارة الديون"])

with tab1:
    st.info("مرحباً بك في لوحة دعم القرار - الإدارة العليا")
    # هنا ممكن تحط الكود القديم بتاعك اللي فيه الأرقام الكبيرة

with tab2:
    st.header("📉 حساب الهالك اللحظي")
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("سعر كيلو الخام (ج.م)", value=150)
    with col2:
        waste = st.number_input("كمية الهالك المكتشفة (كيلو)", value=1)
    
    if st.button("احسب الخسارة اللحظية"):
        st.error(f"⚠️ إجمالي المبلغ المهدر: {price * waste} ج.م")

with tab3:
    st.header("💸 نظام ملاحقة المديونيات")
    name = st.text_input("اسم العميل أو المصنع")
    debt = st.number_input("المبلغ المطلوب تحصيله", min_value=0)
    if st.button("تسجيل المديونية"):
        st.success(f"تم تسجيل {debt} ج.م على {name} بنجاح")
        
