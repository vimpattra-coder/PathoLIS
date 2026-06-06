import streamlit as st

# ==========================================
# 1. ตั้งค่าหัวเว็บไซต์
# ==========================================
st.set_page_config(page_title="ระบบจัดการงานพยาธิวิทยา", layout="wide")

# ==========================================
# หัวข้อตรงกลางหน้าจอ
# ==========================================
st.markdown(
    """
    <h1 style='text-align: center; color: #1E3A8A; margin-bottom: 25px;'>
        🔬 ระบบการจัดการทางพยาธิวิทยา
    </h1>
    """, 
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# 2. สลับแท็บ: แท็บแรกเป็นย้อมสีพิเศษ แท็บสองเป็นทิ้งสิ่งส่งตรวจ 🔄
# ==========================================
tab1, tab2 = st.tabs(["🔬 ระบบส่งย้อมสีพิเศษ", "📦 ระบบทิ้งสิ่งส่งตรวจ"])

with tab1:
    # รันไฟล์ย้อมสีพิเศษเป็นแท็บแรก
    try:
        with open("special_stain.py", encoding="utf-8") as f:
            code = f.read()
            exec(code)
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ special_stain.py กรุณาเช็คชื่อไฟล์อีกครั้งครับ")

with tab2:
    # รันไฟล์ทิ้งสิ่งส่งตรวจเป็นแท็บที่สอง
    try:
        with open("dispos.py", encoding="utf-8") as f:
            code = f.read()
            exec(code)
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ dispos.py กรุณาเช็คชื่อไฟล์อีกครั้งครับ")