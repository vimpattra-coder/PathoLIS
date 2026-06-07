import streamlit as st
import pandas as pd
import datetime
st.set_page_config(layout="wide")
# ใช้เวลาปัจจุบัน
current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# 1. เตรียมฐานข้อมูล (เพิ่มคอลัมน์ จุดประสงค์การยืม)
if "df_borrow" not in st.session_state:
    data = {
        "Block_ID": ["S690001A", "S690001B", "S690002A", "S690003A", "S690005A"],
        "Surgical_No": ["S690001", "S690001", "S690002", "S690003", "S690005"],
        "ชื่อผู้ป่วย": ["นายสมชาย ใจดี", "นายสมชาย ใจดี", "นายสมชาย ดีใจ", "นางสมศรี มีสุข", "นายมานะ เก่งกาจ"],
        "Status": ["อยู่ที่กลุ่มงาน"] * 5,
        "ผู้ยืม": [None] * 5,
        "เวลาที่ยืม": [None] * 5,
        "จุดประสงค์การยืม": [None] * 5,
        
        # --- เพิ่มบรรทัดนี้ลงไปครับ ---
        "รายการที่ยืม": [None] * 5, 
        
        "ผู้คืน": [None] * 5,
        "เวลาที่คืน": [None] * 5
    }
    st.session_state.df_borrow = pd.DataFrame(data)

st.title("🏥 ระบบยืม-คืน บล็อกสไลด์")

# 2. ฟังก์ชันอัปเดตสถานะ
def update_status(idx, status, person_name=None, reason=None, items=None):
    if status == "ถูกยืม":
        # บันทึกรายการที่ยืมลงในคอลัมน์ (คุณอาจต้องเพิ่มคอลัมน์ 'รายการที่ยืม' ใน data ด้วยนะครับ)
        st.session_state.df_borrow.loc[idx, ["Status", "ผู้ยืม", "เวลาที่ยืม", "จุดประสงค์การยืม", "รายการที่ยืม"]] = ["ถูกยืม", person_name, current_time, reason, ", ".join(items)]
    else:
        # ... (ส่วนคืน)
        st.session_state.df_borrow.loc[idx, ["Status", "ผู้คืน", "เวลาที่คืน"]] = ["อยู่ที่กลุ่มงาน", person_name, current_time]
    st.rerun()

# 3. ส่วนสแกน
st.subheader("📍 สแกนหรือพิมพ์เลขบล็อก/สไลด์")
scan_input = st.text_input("เลขบล็อก (เช่น S690001A):", key="scanner")

if scan_input:
    match = st.session_state.df_borrow[st.session_state.df_borrow["Block_ID"].str.upper() == scan_input.upper()]
    if not match.empty:
        idx = match.index[0]
        row = match.iloc[0]
        st.write(f"**ผู้ป่วย:** {row['ชื่อผู้ป่วย']} | **สถานะ:** {row['Status']}")
        
        if row["Status"] == "อยู่ที่กลุ่มงาน":
            items_to_borrow = st.multiselect("เลือกรายการที่ต้องการยืม:", ["Block", "Slide"])
            borrower = st.text_input("ชื่อผู้ยืม:", key="b_name")
            reason = st.selectbox(
    "จุดประสงค์การยืม:", 
    ["เพื่อวินิจฉัย/Consult", "ส่งต่อการรักษา", "เพื่อการศึกษา/วิจัย", "อื่นๆ"], 
    key="b_reason"
)
            
            if st.button("ยืนยันการยืม") and borrower and items_to_borrow:
                # ปรับการส่งค่า items_to_borrow เข้าไปในฟังก์ชันด้วย
                update_status(idx, "ถูกยืม", borrower, reason, items_to_borrow)
        else:
            st.warning(f"ถูกยืมโดย: {row['ผู้ยืม']} | จุดประสงค์การยืม: {row['จุดประสงค์การยืม']}")
            returner = st.text_input("ชื่อผู้คืน:", key="r_name")
            if st.button("ยืนยันการคืน") and returner:
                update_status(idx, "อยู่ที่กลุ่มงาน", returner)
    else:
        st.error("ไม่พบเลขบล็อกนี้ในระบบ")

st.markdown("---")
st.subheader("📄 รายการทั้งหมด")
st.dataframe(st.session_state.df_borrow, use_container_width=True)