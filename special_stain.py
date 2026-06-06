import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
@st.dialog("🔔 แจ้งเตือนระบบ")
def show_success_popup():
    st.write("") # เว้นบรรทัดนิดนึง
    st.success("**กดส่งย้อมเรียบร้อยแล้ว**")
    
    if st.button("ตกลง", use_container_width=True):
        # 🧹 ล้างค่าในกล่องข้อความทั้งหมดกลับเป็นค่าว่าง
        st.session_state["input_hn"] = ""
        st.session_state["input_case"] = ""
        st.session_state["input_patient"] = ""
        st.session_state["input_notes"] = ""
        
        # 🧹 ล้างค่าตัวเลือกสีย้อม (Checkbox) ทั้งหมดกลับเป็น False
        for stain in ["AFB", "mAFB", "GMS", "PAS", "PAS-D", "Giemsa", "Gram stain", "Mucin", "Congo red", "Recut", "Deep cut"]:
            st.session_state[f"cb_{stain}"] = False
            
        st.rerun()


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

# 2. จำลองข้อมูลในระบบ
if "cases" not in st.session_state:
    st.session_state.cases = [
        {"case_no": "S25-1041", "hn_an": "HN00145678", "patient_name": "มานี ศรีสุข", "doctor": "VT", "date_time": "05/06/2026 - 09:00 น.", "month_year": "มิถุนายน 2026", "stains": ["GMS"], "status": "ย้อมเสร็จแล้ว", "completed_at": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), "notes": ""},
        {"case_no": "S25-2000", "hn_an": "HN00222222", "patient_name": "สมชาย รักดี", "doctor": "NK", "date_time": "05/06/2026 - 10:00 น.", "month_year": "มิถุนายน 2026", "stains": ["AFB"], "status": "รอรับคำสั่ง", "completed_at": None, "notes": ""},
        {"case_no": "S25-3000", "hn_an": "HN00333333", "patient_name": "ชูใจ ตั้งใจ", "doctor": "KK", "date_time": "05/06/2026 - 11:30 น.", "month_year": "มิถุนายน 2026", "stains": ["PAS"], "status": "กำลังย้อม", "completed_at": None, "notes": ""}
    ]

st.title("🔬 ระบบส่งย้อมพิเศษ (Special Stains)")
st.caption("Reading frontend design skill >")

tab_order, tab_track, tab_lab, tab_stats = st.tabs([
    "➕ สั่งย้อม", 
    "📋 ติดตามสถานะ (แพทย์)", 
    "🔬 สำหรับเจ้าหน้าที่ (Lab)", 
    "📊 สถิติการส่งย้อม"
])

steps = ["รอรับคำสั่ง", "กำลังย้อม", "ย้อมเสร็จแล้ว"]

# ==========================================
# แท็บ 1: สั่งย้อม (เวอร์ชันเพิ่ม key เพื่อรองรับระบบล้างข้อมูล)
# ==========================================
with tab_order:
    col1, col2 = st.columns(2)
    with col1:
        # ✨ เพิ่ม key="input_hn" และ key="input_case"
        hn_an = st.text_input("HN / AN", key="input_hn")
        case_no = st.text_input("Case No. / Biopsy No.", key="input_case", autocomplete="off")
    with col2:
        # ✨ เพิ่ม key="input_patient"
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
    # ✨ เพิ่ม key="input_notes"
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
            
            # 🚀 เรียก Pop-up แจ้งเตือน
            show_success_popup()
        else:
            st.error("กรุณากรอก Case No. และ ชื่อผู้ป่วย")
# ==========================================
# ==========================================
# แท็บ 2: ติดตามสถานะ (แพทย์)
# ==========================================
with tab_track:
    if not st.session_state.cases:
        st.info("ยังไม่มีเคสในระบบ")
    else:
        search_query = st.text_input("🔍 ค้นหาเคสของคุณหมอ (พิมพ์ HN, Case No. หรือ ชื่อผู้ป่วย)", autocomplete="off")
        
        # ✨ เพิ่มเงื่อนไข: ถ้ายังไม่ได้พิมพ์อะไรในช่องค้นหา ให้แสดงคำแนะนำสั้นๆ และไม่ต้องโชว์เคสเลยครับ
        if not search_query.strip():
            st.info("💡 กรุณากรอก HN, Case No. หรือชื่อผู้ป่วย เพื่อค้นหาและติดตามสถานะเคส")
        
        else:
            # 🔍 จะทำงานค้นหาก็ต่อเมื่อคุณหมอเริ่มพิมพ์ข้อความเท่านั้น
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
                            st.markdown("<div class='status-banner'>✓ งานเสร็จสมบูรณ์ สามารถอ่านผลได้เลยค๊าบ</div>", unsafe_allow_html=True)
                        
                        if c['status'] == "รอรับคำสั่ง":
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button(f"❌ ยกเลิกคำสั่งย้อมสำหรับเคส {c['case_no']}", type="primary", key=f"cancel_{c['case_no']}"):
                                st.session_state.cases.pop(original_db_index)
                                st.success("ยกเลิกคำสั่งย้อมเรียบร้อยแล้ว!")
                                st.rerun()
                    
                    st.write("")
# ==========================================
# แท็บ 3: สำหรับเจ้าหน้าที่ (Lab) - เวอร์ชันปุ่มกดต่อเนื่อง (สีแดงตัวเอียง -> กดเมื่อย้อมเสร็จ) 🟢
# ==========================================
with tab_lab:
    st.markdown("### 📋 รายการคำสั่งส่งย้อมทั้งหมดในระบบ")
    st.caption("Sorting Logic: เรียงเคสที่ยังไม่เสร็จตามเวลาส่ง (เก่าสุดอยู่บน) และนำเคสที่ 'ย้อมเสร็จแล้ว' ไปไว้ท้ายสุด")
    
    if not st.session_state.cases:
        st.info("ไม่มีงานในระบบขณะนี้")
    else:
        now = datetime.now()
        
        # ส่วนผสมตรรกะการจัดเรียง (Sorting Logic Process)
        active_cases = []
        completed_cases = []
        
        for case in st.session_state.cases:
            if case['status'] == "ย้อมเสร็จแล้ว" and case.get('completed_at'):
                try:
                    completed_time = datetime.strptime(case['completed_at'], "%Y-%m-%d %H:%M")
                    if now - completed_time > timedelta(hours=48):
                        continue
                except:
                    pass
            
            if case['status'] == "ย้อมเสร็จแล้ว":
                completed_cases.append(case)
            else:
                active_cases.append(case)
        
        def get_timestamp(case_item):
            try:
                date_part = case_item['date_time'].split(" - ")[0]
                time_part = case_item['date_time'].split(" - ")[1].replace(" น.", "")
                return datetime.strptime(f"{date_part} {time_part}", "%d/%m/%Y %H:%M")
            except:
                return datetime.now()
        
        active_cases.sort(key=get_timestamp)
        completed_cases.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
        sorted_display_cases = active_cases + completed_cases
        
        # แสดงผลตารางคิวงาน
        for case in sorted_display_cases:
            original_db_index = st.session_state.cases.index(case)
            
            with st.container(border=True):
                col_info, col_status_control = st.columns([3, 2])
                
                with col_info:
                    st.markdown(f"🔬 **Case:** {case['case_no']} | **ผู้ป่วย:** {case['patient_name']} (HN: {case['hn_an']})")
                    st.markdown(f"**แพทย์:** {case['doctor']} | ⏰ {case['date_time']}")
                    st.markdown("".join([f"<span class='tag'>{s}</span>" for s in case['stains']]), unsafe_allow_html=True)
                    if case['notes']:
                        st.caption(f"📝 หมายเหตุ: {case['notes']}")
                    if case['status'] == "ย้อมเสร็จแล้ว" and case.get('completed_at'):
                        st.caption(f"✅ ย้อมเสร็จเมื่อ: {case['completed_at']}")
                
                # 🟢 ฝั่งจัดการสถานะแบบปุ่มกดต่อเนื่องตามเงื่อนไขใหม่
                with col_status_control:
                    st.write("การจัดการสถานะงาน:")
                    
                    # 🟢 เงื่อนไขที่ 1: สถานะ "รอรับคำสั่ง" -> ใช้ปุ่ม HTML ล้วน (ลบกล่องว่างใต้ปุ่มออกถาวร)
                    if case['status'] == "รอรับคำสั่ง":
                        # 1. เช็ก Event จากการกดปุ่ม HTML ผ่าน query_params หรือใช้เทคนิคจับชื่อปุ่ม
                        btn_id = f"click_recv_{case['case_no']}"
                        
                        # ตรวจสอบว่าถ้ามีการกดปุ่มนี้เข้ามาในระบบ ให้เปลี่ยนสเตตัสทันที
                        if st.query_params.get(btn_id) == "true":
                            st.session_state.cases[original_db_index]['status'] = "กำลังย้อม"
                            # เคลียร์ค่าเพื่อไม่ให้ค้างตอนโหลดรอบหน้า
                            st.query_params.pop(btn_id, None)
                            st.rerun()

                        # 2. สร้างปุ่ม HTML สวยๆ โดยเมื่อคลิกจะบังคับรีโหลดเว็บพร้อมส่งค่าบอกระบบว่ากดแล้ว
                        button_html = f"""
                        <a href="?{btn_id}=true" target="_self" style="text-decoration: none;">
                            <div style="width: 100%; background-color: #FFEB3B; color: #000000; 
                                        padding: 10px 0px; text-align: center; font-weight: bold; 
                                        border-radius: 20px; cursor: pointer; font-size: 14px;
                                        box-sizing: border-box; display: block;">
                                📥 รับคำสั่งย้อม ({case['case_no']})
                            </div>
                        </a>
                        """
                        st.markdown(button_html, unsafe_allow_html=True)
                            
                    # เงื่อนไขที่ 2: สถานะ "กำลังย้อม" -> ขึ้นตัวหนังสือเอียงแดง และปุ่มกดเมื่อย้อมเสร็จ
                    elif case['status'] == "กำลังย้อม":
                        # ใช้ columns ย่อยจัดให้ข้อความและปุ่มอยู่ระนาบเดียวกันสวยงาม
                        sub_col1, sub_col2 = st.columns([1, 1.2])
                        with sub_col1:
                            # แสดงตัวหนังสือสีแดง ตัวหนา และตัวเอียงด้วย HTML
                            st.markdown("<p style='color: #D32F2F; font-weight: bold; font-style: italic; margin-top: 6px;'>กำลังย้อม</p>", unsafe_allow_html=True)
                        with sub_col2:
                            if st.button("✅ กดเมื่อย้อมเสร็จ", key=f"lab_btn_done_{case['case_no']}", use_container_width=True, type="primary"):
                                st.session_state.cases[original_db_index]['status'] = "ย้อมเสร็จแล้ว"
                                st.session_state.cases[original_db_index]['completed_at'] = now.strftime("%Y-%m-%d %H:%M")
                                st.rerun()
                                
                    # เงื่อนไขที่ 3: สถานะ "ย้อมเสร็จแล้ว" -> แสดงสถานะพร้อมปุ่มเผื่อดึงสเตตัสกลับกรณีเจ้าหน้าที่กดพลาด
                    else:
                        st.success("🟢 ย้อมเสร็จเรียบร้อยแล้ว")
                        if st.button("🔄 ดึงกลับเป็นกำลังย้อม (แก้ไข)", key=f"lab_btn_undo_{case['case_no']}", use_container_width=True):
                            st.session_state.cases[original_db_index]['status'] = "กำลังย้อม"
                            st.session_state.cases[original_db_index]['completed_at'] = None
                            st.rerun()
                            
                st.markdown("---")


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
        
        # 🟢 1. แยกรายชื่อสีย้อมเดี่ยว และตัวที่ต้องการนำมารวมกัน
        base_stains = [
            "AFB", "mAFB", "GMS", "PAS", 
            "PAS-D", "Giemsa", "Gram stain", "Mucin", 
            "Congo red"
        ]
        merge_stains = ["Recut", "Deep cut"]
        all_system_stains = base_stains + merge_stains
        
        # 2. รวบรวมข้อมูลดิบ
        raw_data = []
        for c in monthly_cases:
            doc = c.get('doctor', 'ไม่ระบุ')
            for stain in c['stains']:
                raw_data.append({"แพทย์": doc, "stain": stain})
                
        if raw_data:
            df_raw = pd.DataFrame(raw_data)
            
            # 3. ทำ Pivot Table เพื่อนับจำนวนแยกตามปกติก่อน
            df_pivot = df_raw.pivot_table(
                index='แพทย์', 
                columns='stain', 
                aggfunc='size', 
                fill_value=0
            )
            
            # 4. บังคับให้ตารางมีคอลัมน์ครบทุกสีย้อมดั้งเดิมก่อนเพื่อป้องกัน Error (กรณีบางเดือนไม่มีคนสั่งเลย)
            df_pivot = df_pivot.reindex(columns=all_system_stains, fill_value=0)
            
            # 🟢 5. ตรรกะรวมคอลัมน์: เอาคอลัมน์ Recut บวกกับ Deep cut เป็นคอลัมน์ใหม่
            df_pivot['Recut/Deep cut'] = df_pivot['Recut'] + df_pivot['Deep cut']
            
            # 🟢 6. ลบคอลัมน์ Recut และ Deep cut แบบเดี่ยว ๆ ออกไปจากตาราง
            df_pivot = df_pivot.drop(columns=merge_stains)
            
            # 7. ดึง Index "แพทย์" ออกมาเป็นคอลัมน์แรกปกติ
            df_pivot = df_pivot.reset_index()
            
            # 🟢 8. กำหนดลำดับคอลัมน์สุดท้ายที่จะแสดงผล (เอาคอลัมน์ใหม่ไปต่อท้ายแทนที่เดิม)
            final_display_columns = base_stains + ["Recut/Deep cut"]
            
            # 9. คำนวณยอดรวมแนวนอนตามสีย้อมที่ปรับแต่งแล้ว
            df_pivot['รวมทั้งหมด'] = df_pivot[final_display_columns].sum(axis=1)
            
            # เรียงลำดับตามแพทย์ที่ส่งเยอะที่สุด
            df_pivot = df_pivot.sort_values(by='รวมทั้งหมด', ascending=False)
            
            # แสดงผลตาราง
            st.dataframe(df_pivot, use_container_width=True, hide_index=True)
            
        else:
            # กรณีมีเคสในเดือนนั้นแต่ไม่มีการติ๊กเลือกเลย (สร้างตารางเปล่าแบบมีหัวข้อใหม่รอไว้)
            unique_docs = list(set([c.get('doctor', 'ไม่ระบุ') for c in monthly_cases]))
            final_cols = base_stains + ["Recut/Deep cut"]
            df_empty = pd.DataFrame(0, index=unique_docs, columns=final_cols).reset_index().rename(columns={'index': 'แพทย์'})
            df_empty['รวมทั้งหมด'] = 0
            st.dataframe(df_empty, use_container_width=True, hide_index=True)