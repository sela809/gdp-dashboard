import streamlit as st
import pandas as pd

# إعداد الصفحة لتناسب شاشات المديرين
st.set_page_config(page_title="الرادار المركزي للشركات", page_icon="🏢", layout="wide")

# تصميم الهيدر (العنوان الفخم)
st.markdown("""
    <div style="background-color:#001529;padding:15px;border-radius:10px;border-right: 8px solid #1890ff">
    <h1 style="color:white;text-align:right;">🏢 منظومة الرقابة المركزية للمصانع</h1>
    <p style="color:#40a9ff;text-align:right;">لوحة دعم اتخاذ القرار - الإدارة العليا</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 1. عدادات الأداء اللحظية (تلمس نقاط الألم)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 صافي الربح اليومي", "125,400 ج.م", "+8%")
with col2:
    st.metric("📉 معدل الهالك (Waste)", "2.1%", "-0.5%", delta_color="normal")
with col3:
    st.metric("💸 تحصيل مديونيات", "42,000 ج.م", "تنبيه!", delta_color="inverse")
with col4:
    st.metric("⚙️ كفاءة الإنتاج", "96%", "+2%")

st.write("---")

# 2. عرض حالة الفروع والمصانع
st.subheader("📍 رادار المنشآت اللحظي")
col_l, col_r = st.columns([2, 1])

with col_l:
    # بيانات محاكاة للشركات
    data = {
        'المنشأة': ['مصنع أشمون (خط 1)', 'مصنع الباجور (خط 3)', 'المخزن الإقليمي', 'معرض المنتجات'],
        'الحالة': ['يعمل ✅', 'توقف مؤقت ⚠️', 'مستقر ✅', 'مزدحم 🔥'],
        'الإنتاجية': ['98%', '15%', '100%', '88%']
    }
    st.table(pd.DataFrame(data))

with col_r:
    st.warning("🚨 **تنبيه الإدارة:** يوجد تأخير في توريد الخامات لمصنع الباجور، مما أدى لانخفاض الإنتاجية لـ 15%.")
    if st.button("إرسال تقرير PDF للمدير العام 📩"):
        st.success("تم إرسال التقرير بنجاح لواتساب الإدارة.")

# القائمة الجانبية
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("مركز القيادة")
st.sidebar.info("استخدم القائمة الجانبية للتنقل بين تقارير المصانع التفصيلية.")
