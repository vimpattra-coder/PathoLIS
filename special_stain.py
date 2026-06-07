import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# 2. ส่วนที่ 2: ประกาศฟังก์ชันส่วนกลางทั้งหมดไว้ตรงนี้ (ย้ายฟังก์ชันมาไว้ตรงนี้เลย!)
def change_status(case_no, status):
    for c in st.session_state.cases:
        if c['case_no'] == case_no:
            c['status'] = status
            if status == "ย้อมเสร็จแล้ว":
                c['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                c['completed_at'] = None
            break
    st.rerun()
# ==========================================
# 0. ฟังก์ชันแจ้งเตือนระบบ (Dialog)
# ==========================================
@st.dialog("🔔 แจ้งเตือนระบบ")
def show_success_popup():
    st.write("") 
    st.success("**กดส่งย้อมเรียบร้อยแล้ว**")
    
    if st.button("ตกลง", use_container_width=True):
        st.session_state["input_hn"] = ""
        st.session_state["input_case"] = ""
        st.session_state["input_patient"] = ""
        st.session_state["input_notes"] = ""
        
        for stain in ["AFB", "mAFB", "GMS", "PAS", "PAS-D", "Giemsa", "Gram stain", "Mucin", "Congo red", "Recut", "Deep cut"]:
            st.session_state[f"cb_{stain}"] = False
        st.rerun()

# ==========================================
# 1. การตั้งค่าสไตล์ CSS และตัวแปรส่วนกลาง
# ==========================================
st.markdown("""
    <style>
    .stButton>button { border-radius: 20px; }
    .status-banner {
        background-color: #E8F5E9; color: #2E7D32; padding: 12px;
        border-radius: 8px; text-align: center; font-weight: bold; margin-top: 15px;
    }
    .tag {
        background-color: #EDE7F6; color: #5E35B1; padding: 4px 12px;
        border-radius: 16px; font-size: 14px; display: inline-block;
        margin-right: 5px; margin-bottom: 5px; font-weight: bold;
    }
    .step-active { color: #5E35B1; font-weight: bold; }
    .step-inactive { color: #BDBDBD; }
    </style>
""", unsafe_allow_html=True)

thai_months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

# ฟังก์ชันส่วนกลางสำหรับอัปเดตสถานะเคส
def update_case_status(case_no, new_status):
    for c in st.session_state.cases:
        if c['case_no'] == case_no:
            c['status'] = new_status
            if new_status == "ย้อมเสร็จแล้ว":
                c['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                c['completed_at'] = None
            break
    st.rerun()

# ==========================================
# 2. จำลองข้อมูลเริ่มต้นในระบบ (Session State)
# ==========================================
if "cases" not in st.session_state:
    st.session_state.cases = [
        {"case_no": "S25-1041", "hn_an": "HN00145678", "patient_name": "มานี ศรีสุข", "doctor": "VT", "date_time": "05/06/2026 - 09:00 น.", "month_year": "มิถุนายน 2026", "stains": ["GMS"], "status": "ย้อมเสร็จแล้ว", "completed_at": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), "notes": ""},
        {"case_no": "S25-2000", "hn_an": "HN00222222", "patient_name": "สมชาย รักดี", "doctor": "NK", "date_time": "05/06/2026 - 10:00 น.", "month_year": "มิถุนายน 2026", "stains": ["AFB"], "status": "รอรับคำสั่ง", "completed_at": None, "notes": ""},
        {"case_no": "S25-3000", "hn_an": "HN00333333", "patient_name": "ชูใจ ตั้งใจ", "doctor": "KK", "date_time": "05/06/2026 - 11:30 น.", "month_year": "มิถุนายน 2026", "stains": ["PAS"], "status": "กำลังย้อม", "completed_at": None, "notes": ""}
    ]

st.title("🔬 ระบบส่งย้อมพิเศษ (Special Stains)")
st.caption("Reading frontend design skill >")

# สร้างแท็บหลักทั้ง 4 แท็บ
tab_order, tab_track, tab_lab, tab_stats = st.tabs([
    "➕ สั่งย้อม", 
    "📋 ติดตามสถานะ (แพทย์)", 
    "🔬 สำหรับเจ้าหน้าที่ (Lab)", 
    "📊 สถิติการส่งย้อม"
])

steps = ["รอรับคำสั่ง", "กำลังย้อม", "ย้อมเสร็จแล้ว"]

# ==========================================
# แท็บ 1: ➕ สั่งย้อม
# ==========================================
with tab_order:
    col1, col2 = st.columns(2)
    with col1:
        hn_an = st.text_input("HN / AN", key="input_hn")
        case_no = st.text_input("Case No. / Biopsy No.", key="input_case", autocomplete="off")
    with col2:
        patient_name = st.text_input("ชื่อผู้ป่วย", key="input_patient", autocomplete="off")
        doctor = st.selectbox("แพทย์ผู้ส่ง", ["VT", "NK", "KK", "PS"])
        
    st.markdown("### เลือก SPECIAL STAINS")
    selected_stains = []
    
    col_stain1 = st.columns(4)
    stains_row1 = ["AFB", "mAFB", "GMS", "PAS"]
    for i, stain in enumerate(stains_row1):
        if col_stain1[i].checkbox(stain, key=f"cb_{stain}"): selected_stains.append(stain)
            
    col_stain2 = st.columns(4)
    stains_row2 = ["PAS-D", "Giemsa", "Gram stain", "Mucin"]
    for i, stain in enumerate(stains_row2):
        if col_stain2[i].checkbox(stain, key=f"cb_{stain}"): selected_stains.append(stain)
            
    col_stain3 = st.columns(3)
    stains_row3 = ["Congo red", "Recut", "Deep cut"]
    for i, stain in enumerate(stains_row3):
        if col_stain3[i].checkbox(stain, key=f"cb_{stain}"): selected_stains.append(stain)

    st.markdown("---")
    notes = st.text_area("หมายเหตุ", placeholder="ข้อมูลเพิ่มเติม...", key="input_notes")
    
    if st.button("✈️ ส่งคำสั่งย้อม", use_container_width=True):
        if case_no and patient_name:
            now = datetime.now()
            current_date_time = now.strftime("%d/%m/%Y - %H:%M น.")
            current_month_year = f"{thai_months[now.month - 1]} {now.year}"
            
            st.session_state.cases.append({
                "case_no": case_no, "hn_an": hn_an, "patient_name": patient_name, "doctor": doctor,
                "date_time": current_date_time, "month_year": current_month_year, "stains": selected_stains, 
                "status": "รอรับคำสั่ง", "completed_at": None, "notes": notes
            })
            
            # เรียก Pop-up แจ้งเตือนความสำเร็จ
            show_success_popup()
        else:
            st.error("กรุณากรอก Case No. และ ชื่อผู้ป่วย")

# ==========================================
# แท็บ 2: 📋 ติดตามสถานะ (แพทย์)
# ==========================================
with tab_track:
    if not st.session_state.cases:
        st.info("ยังไม่มีเคสในระบบ")
    else:
        search_query = st.text_input("🔍 ค้นหาเคสของคุณหมอ (พิมพ์ HN, Case No. หรือ ชื่อผู้ป่วย)", autocomplete="off")
        
        if not search_query.strip():
            st.info("💡 กรุณากรอก HN, Case No. หรือชื่อผู้ป่วย เพื่อค้นหาและติดตามสถานะเคส")
        else:
            filtered_cases = []
            for c in st.session_state.cases:
                if (search_query.lower() in c['hn_an'].lower() or 
                    search_query.lower() in c['case_no'].lower() or 
                    search_query.lower() in c['patient_name'].lower()):
                    filtered_cases.append(c)
            
            if not filtered_cases:
                st.warning("❌ ไม่พบข้อมูลที่ตรงกับคำค้นหาของคุณ")
            else:
                for c in filtered_cases:
                    original_db_index = st.session_state.cases.index(c)
                    
                    with st.container(border=True):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"### **{c['case_no']}**")
                            st.markdown(f"**ผู้ป่วย:** {c['patient_name']}  |  **HN:** {c['hn_an']}")
                            st.markdown(f"**แพทย์ผู้ส่ง:** {c['doctor']}  |  📅 **วัน-เวลาส่ง:** {c['date_time']}")
                            if c['notes']:
                                st.markdown(f"*หมายเหตุ:* {c['notes']}")
                        with col_b:
                            st.markdown("**Stains Requested:**")
                            st.markdown("".join([f"<span class='tag'>{s}</span>" for s in c['stains']]), unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        current_idx = steps.index(c['status'])
                        cols_step = st.columns(3)
                        for idx, step in enumerate(steps):
                            with cols_step[idx]:
                                st.markdown(f"🟢 **{step}**" if idx <= current_idx else f"⚪ <span class='step-inactive'>{step}</span>", unsafe_allow_html=True)
                        
                        if c['status'] == "ย้อมเสร็จแล้ว":
                            st.markdown("<div class='status-banner'>✓ งานย้อมเสร็จสมบูรณ์</div>", unsafe_allow_html=True)
                        
                        if c['status'] == "รอรับคำสั่ง":
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button(f"❌ ยกเลิกคำสั่งย้อมสำหรับเคส {c['case_no']}", type="primary", key=f"cancel_{c['case_no']}"):
                                st.session_state.cases.pop(original_db_index)
                                st.success("ยกเลิกคำสั่งย้อมเรียบร้อยแล้ว!")
                                st.rerun()
                    st.write("")

# ==========================================
# ==========================================
# แท็บ 3: 🔬 สำหรับเจ้าหน้าที่ (Lab) - เวอร์ชันเสร็จสมบูรณ์
# ==========================================
with tab_lab:
    # 🛡️ กรองข้อมูลที่เป็น Dictionary จริง ๆ ออกมา (ป้องกันเศษซากเก่าค้างใน Cache)
    valid_cases = [c for c in st.session_state.cases if isinstance(c, dict)]
    
    if not valid_cases:
        st.info("🔬 ยังไม่มีรายการคำสั่งส่งย้อมในระบบ")
    else:
        st.subheader("📋 รายการคำสั่งส่งย้อมทั้งหมดในระบบ")
        st.caption("Sorting Logic: เรียงเคสที่ยังไม่เสร็จตามเวลาส่ง (เก่าสุดอยู่บน) และนำเคสที่ 'ย้อมเสร็จแล้ว' ไปไว้ท้ายสุด")
        
        # 1. กำหนดคะแนนความสำคัญของสถานะ
        status_priority = {"รอรับคำสั่ง": 1, "กำลังย้อม": 2, "ย้อมเสร็จแล้ว": 3}
        
        # 2. ฟังก์ชันช่วยแปลงข้อความวันที่เพื่อใช้เรียงลำดับ
        def parse_case_date(date_str):
            if not date_str:
                return datetime.min
            try:
                clean_str = str(date_str).replace(" น.", "").strip()
                return datetime.strptime(clean_str, "%d/%m/%Y - %H:%M")
            except Exception:
                return datetime.min
                
        # 3. จัดเรียงเคสแบบปลอดภัย
        sorted_cases = sorted(
            valid_cases,
            key=lambda x: (status_priority.get(x.get('status', 'รอรับคำสั่ง'), 99), parse_case_date(x.get('date_time', '')))
        )
        
        # 4. วนลูปแสดงผลกล่องข้อมูลเคส
        for idx, case in enumerate(sorted_cases):
            case_no = case.get('case_no', 'ไม่ระบุหมายเลข')
            patient_name = case.get('patient_name', 'ไม่ระบุชื่อ')
            hn_an = case.get('hn_an', '-')
            doctor = case.get('doctor', '-')
            date_time = case.get('date_time', '-')
            stains = case.get('stains', [])
            notes = case.get('notes', '')
            status = case.get('status', 'รอรับคำสั่ง')
            completed_at = case.get('completed_at', '')
            
            with st.container(border=True):
                col_info, col_status_control = st.columns([3, 1.2])
                
                # 📄 ฝั่งซ้าย: แสดงรายละเอียดข้อมูล (Clean Spaces เรียบร้อย)
                with col_info:
                    st.markdown(f"### **{case_no}**")
                    st.markdown(f"**ผู้ป่วย:** {patient_name} | **HN:** {hn_an}")
                    st.markdown(f"**แพทย์ผู้ส่ง:** {doctor} | 📅 **วัน-เวลาส่ง:** {date_time}")
                    
                    if isinstance(stains, list):
                        st.markdown("**สีย้อมที่สั่ง:** " + "".join([f"<span class='tag'>{s}</span>" for s in stains]), unsafe_allow_html=True)
                    else:
                        st.markdown(f"**สีย้อมที่สั่ง:** {stains}")
                        
                    if notes:
                        st.markdown(f"*หมายเหตุเพิ่มเติม:* <span style='color: #757575;'>{notes}</span>", unsafe_allow_html=True)
                        
                    if status == "ย้อมเสร็จแล้ว" and completed_at:
                        st.markdown(f"⏱️ **เสร็จเมื่อ:** {completed_at}")

                # 🟢 ฝั่งขวา: จัดการสถานะงานตามปุ่มกด
                with col_status_control:
                    st.write("การจัดการสถานะงาน:")
                    
                    # กรณีที่ 1: รอรับคำสั่ง
                    if status == "รอรับคำสั่ง":
                        if st.button(f"📥 รับคำสั่งย้อม ({case_no})", key=f"recv_{case_no}_{idx}", use_container_width=True):
                            change_status(case_no, "กำลังย้อม")
                            st.rerun()

                    # กรณีที่ 2: กำลังย้อม
                    elif status == "กำลังย้อม":
                        st.warning("⚠️ กำลังย้อม...")
                        if st.button("✅ กดเมื่อย้อมเสร็จ", key=f"done_{case_no}_{idx}", use_container_width=True, type="primary"):
                            change_status(case_no, "ย้อมเสร็จแล้ว")
                            st.rerun()
                                
                    # กรณีที่ 3: ย้อมเสร็จเรียบร้อยแล้ว
                    else:
                        st.success("🟢 ย้อมเสร็จเรียบร้อย")
                        if st.button("🔄 ดึงกลับมาแก้ไข", key=f"undo_{case_no}_{idx}", use_container_width=True):
                            change_status(case_no, "กำลังย้อม")
                            st.rerun()
                            
            st.write("")
# ==========================================
# แท็บ 4: 📊 สถิติการส่งย้อม
# ==========================================
with tab_stats:
    st.subheader("📅 ค้นหาสถิติการส่งย้อมประจำเดือน")
    
    col_select1, col_select2 = st.columns(2)
    with col_select1:
        selected_month = st.selectbox("เลือกเดือน:", thai_months, index=datetime.now().month - 1)
    with col_select2:
        selected_year = st.selectbox("เลือกปี (ค.ศ.):", [2025, 2026, 2027, 2028], index=1)
        
    target_month_year = f"{selected_month} {selected_year}"
    
    monthly_cases = []
    for c in st.session_state.cases:
        case_month_year = c.get('month_year')
        if not case_month_year and 'date_time' in c:
            try:
                date_part = c['date_time'].split(" - ")[0]
                parsed_date = datetime.strptime(date_part, "%d/%m/%Y")
                case_month_year = f"{thai_months[parsed_date.month - 1]} {parsed_date.year}"
            except:
                pass
                
        if case_month_year == target_month_year:
            monthly_cases.append(c)
            
    st.markdown("---")
    
    if not monthly_cases:
        st.warning(f"📭 ไม่พบข้อมูลการส่งย้อมในเดือน {target_month_year}")
    else:
        st.markdown(f"### 📋 ตารางแจกแจงสถิติการสั่งย้อมสียอดรวมประจำเดือน {target_month_year}")
        
        base_stains = ["AFB", "mAFB", "GMS", "PAS", "PAS-D", "Giemsa", "Gram stain", "Mucin", "Congo red"]
        merge_stains = ["Recut", "Deep cut"]
        all_system_stains = base_stains + merge_stains
        
        raw_data = []
        for c in monthly_cases:
            doc = c.get('doctor', 'ไม่ระบุ')
            for stain in c['stains']:
                raw_data.append({"แพทย์": doc, "stain": stain})
                
        if raw_data:
            df_raw = pd.DataFrame(raw_data)
            df_pivot = df_raw.pivot_table(index='แพทย์', columns='stain', aggfunc='size', fill_value=0)
            df_pivot = df_pivot.reindex(columns=all_system_stains, fill_value=0)
            
            # รวมคอลัมน์ Recut และ Deep cut
            df_pivot['Recut/Deep cut'] = df_pivot['Recut'] + df_pivot['Deep cut']
            df_pivot = df_pivot.drop(columns=merge_stains).reset_index()
            
            final_display_columns = base_stains + ["Recut/Deep cut"]
            df_pivot['รวมทั้งหมด'] = df_pivot[final_display_columns].sum(axis=1)
            df_pivot = df_pivot.sort_values(by='รวมทั้งหมด', ascending=False)
            
            st.dataframe(df_pivot, use_container_width=True, hide_index=True)
            
        else:
            unique_docs = list(set([c.get('doctor', 'ไม่ระบุ') for c in monthly_cases]))
            final_cols = base_stains + ["Recut/Deep cut"]
            df_empty = pd.DataFrame(0, index=unique_docs, columns=final_cols).reset_index().rename(columns={'index': 'แพทย์'})
            df_empty['รวมทั้งหมด'] = 0
            st.dataframe(df_empty, use_container_width=True, hide_index=True)