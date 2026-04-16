import streamlit as st

st.title("📉 لوحة تحكم الهالك")
st.write("---")

# خاصية حساب الهالك
price = st.number_input("سعر الكيلو خام", value=100)
waste = st.number_input("كمية الهالك (كيلو)", value=10)

if st.button("احسب الخسارة"):
    result = price * waste
    st.error(f"إجمالي المبلغ المهدر: {result} ج.م")
  
