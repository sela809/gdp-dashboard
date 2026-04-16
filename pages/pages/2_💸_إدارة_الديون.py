import streamlit as st
import pandas as pd

st.set_page_config(page_title="إدارة المديونيات", layout="wide")
st.markdown("<h2 style='text-align: right;'>💸 نظام ملاحقة المديونيات والتحصيل</h2>", unsafe_allow_html=True)

# إضافة مديونية
with st.expander("➕ تسجيل مديونية جديدة"):
    name = st.text_input("اسم العميل")
    amount = st.number_input("المبلغ (ج.م)", min_value=0)
    if st.button("حفظ"):
        st.success(f"تم تسجيل {amount} ج.م على {name}")

st.write("---")
st.subheader("📊 كشف الديون")
df = pd.DataFrame({
    "العميل": ["شركة الأمل", "مكتب النجاح"],
    "المبلغ": ["25,000", "45,000"],
    "الحالة": ["🔴 متأخر", "🔴 متأخر جداً"]
})
st.table(df)
