import streamlit as st
import pandas as pd
import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Set up page layout to mimic a wide clinical dashboard screen
st.set_page_config(page_title="Promea Data Collection", layout="wide")

st.title("Promea Machine Data Collection App")
st.markdown("---")

# --- INITIALIZE SESSION STATE FOR PATIENT DATA ---
if "patient_name" not in st.session_state: st.session_state.patient_name = "SALMAN KHAN"
if "lab_no" not in st.session_state: st.session_state.lab_no = "1234"
if "age" not in st.session_state: st.session_state.age = "99"
if "gender" not in st.session_state: st.session_state.gender = "Male"
if "ref_doctor" not in st.session_state: st.session_state.ref_doctor = "Dr.Rohit"
if "hospital" not in st.session_state: st.session_state.hospital = "Promea"
if "lis_number" not in st.session_state: st.session_state.lis_number = "8684683726823"
if "registered_on" not in st.session_state: st.session_state.registered_on = "20-06-2026 10:47"
if "collected_on" not in st.session_state: st.session_state.collected_on = "21-06-2026 11:30"
if "authorized_on" not in st.session_state: st.session_state.authorized_on = "21-06-2026 11:40"
if "printed_on" not in st.session_state: st.session_state.printed_on = "21-06-2026 11:40"

# --- SECTION 1: MANUAL PATIENT INFORMATION INPUT ---
st.subheader("1. Edit Patient & Report Information Manually")

col1, col2, col3 = st.columns(3)

with col1:
    p_name = st.text_input("Patient Name", value=st.session_state.patient_name)
    l_no = st.text_input("Lab No.", value=st.session_state.lab_no)
    p_age = st.text_input("Age", value=st.session_state.age)
    gender_options = ["Male", "Female", "Other"]
    g_idx = gender_options.index(st.session_state.gender) if st.session_state.gender in gender_options else 0
    p_gender = st.selectbox("Gender", gender_options, index=g_idx)

with col2:
    r_doc = st.text_input("Ref. Doctor", value=st.session_state.ref_doctor)
    hosp = st.text_input("Hospital", value=st.session_state.hospital)
    lis_num = st.text_input("LIS Number", value=st.session_state.lis_number)

with col3:
    reg_on = st.text_input("Registered On", value=st.session_state.registered_on)
    col_on = st.text_input("Collected On", value=st.session_state.collected_on)
    auth_on = st.text_input("Authorized On", value=st.session_state.authorized_on)
    prnt_on = st.text_input("Printed On", value=st.session_state.printed_on)

# Sync and update state session variables
st.session_state.patient_name = p_name
st.session_state.lab_no = l_no
st.session_state.age = p_age
st.session_state.gender = p_gender
st.session_state.ref_doctor = r_doc
st.session_state.hospital = hosp
st.session_state.lis_number = lis_num
st.session_state.registered_on = reg_on
st.session_state.collected_on = col_on
st.session_state.authorized_on = auth_on
st.session_state.printed_on = prnt_on

st.markdown("---")

# --- FUNCTION TO GENERATE MEDICAL-GRADE PDF ---
def generate_pdf(patient_info, df_results):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom Styles for Prescription Look
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=1, fontSize=24, textColor=colors.HexColor("#1a365d"), spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Heading3'], alignment=1, fontSize=14, textColor=colors.HexColor("#4a5568"), spaceAfter=25)
    normal_bold = ParagraphStyle('NormalBold', parent=styles['Normal'], fontSize=10, leading=14)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=11, textColor=colors.whitesmoke, fontName="Helvetica-Bold")
    table_cell_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=10, leading=14)
    table_cell_bold = ParagraphStyle('TableCellBold', parent=styles['Normal'], fontSize=10, fontName="Helvetica-Bold", leading=14)
    footer_style = ParagraphStyle('FooterStyle', parent=styles['Italic'], alignment=1, fontSize=9, textColor=colors.gray, spaceBefore=40)

    # Header Title
    story.append(Paragraph("PROMEA THERAPEUTICS", title_style))
    story.append(Paragraph("Electrolyte Analyzer Report", subtitle_style))
    
    # Patient Metadata Table Structure (Two Columns)
    patient_data = [
        [Paragraph(f"<b>Patient Name:</b> {patient_info['patient_name']}", normal_bold), Paragraph(f"<b>Registered On:</b> {patient_info['registered_on']}", table_cell_style)],
        [Paragraph(f"<b>Lab No:</b> {patient_info['lab_no']}", normal_bold), Paragraph(f"<b>Collected On:</b> {patient_info['collected_on']}", table_cell_style)],
        [Paragraph(f"<b>Age/Gender:</b> {patient_info['age']} Yrs / {patient_info['gender']}", normal_bold), Paragraph(f"<b>Authorized On:</b> {patient_info['authorized_on']}", table_cell_style)],
        [Paragraph(f"<b>Ref. Doctor:</b> {patient_info['ref_doctor']}", normal_bold), Paragraph(f"<b>Printed On:</b> {patient_info['printed_on']}", table_cell_style)],
        [Paragraph(f"<b>Hospital:</b> {patient_info['hospital']}", normal_bold), Paragraph(f"<b>LIS Number:</b> {patient_info['lis_number']}", table_cell_style)]
    ]
    
    meta_table = Table(patient_data, colWidths=[260, 260])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor("#cbd5e0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # Section Divider heading
    story.append(Paragraph("<b>ELECTROLYTE PANEL</b>", ParagraphStyle('PanelHeader', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor("#1a365d"), spaceAfter=12)))
    
    # Lab Panel Results Table
    results_data = [[
        Paragraph("Parameter", table_header_style), 
        Paragraph("Observed Value (Slope)", table_header_style), 
        Paragraph("Unit", table_header_style), 
        Paragraph("Biological Reference Range", table_header_style)
    ]]
    
    for _, row in df_results.iterrows():
        results_data.append([
            Paragraph(str(row['Parameter']), table_cell_bold),
            Paragraph(str(row['Value']), table_cell_style),
            Paragraph(str(row['Unit']), table_cell_style),
            Paragraph(str(row['Biological Reference Range']), table_cell_style)
        ])
        
    results_table = Table(results_data, colWidths=[130, 130, 110, 150])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1a365d")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f7fafc")]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('LINEBELOW', (0,0), (-1,0), 2, colors.HexColor("#1a365d"))
    ]))
    story.append(results_table)
    
    # End of Report text
    story.append(Spacer(1, 30))
    story.append(Paragraph("--- End of Report ---", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- SECTION 2: MACHINE DATA UPLOAD ---
st.subheader("2. Upload Analyzer Output File")
uploaded_file = st.file_uploader(
    "Upload machine data file (Accepts: CSV, Excel, TXT, or LOG format)",
    type=["csv", "xlsx", "txt", "log"]
)

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name.lower()

        # 1. Adaptively ingest raw data based on file extensions
        if file_name.endswith(".xlsx"):
            raw_data = pd.read_excel(uploaded_file)
        elif file_name.endswith(".txt") or file_name.endswith(".log"):
            bytes_data = uploaded_file.read()
            text_data = bytes_data.decode("utf-8", errors="ignore")
            lines = text_data.splitlines()
            
            # Identify if it is a comma-delimited structure with predefined text headers
            if lines and "," in lines[0] and "Parameter" in lines[0]:
                uploaded_file.seek(0)
                raw_data = pd.read_csv(uploaded_file)
            else:
                raw_data = pd.DataFrame({"Machine_Data": lines})
        else:
            raw_data = pd.read_csv(uploaded_file)

        # Standardize and trim whitespace from parsed columns
        raw_data.columns = [str(col).strip() for col in raw_data.columns]

        # --- SMART ADAPTIVE TRANSFORMATION LAYER ---
        # Checks if file matches unstructured string streams (e.g. rohit.csv containing raw string cells)
        if "Parameter" not in raw_data.columns or ("SLOPE" not in raw_data.columns and "Machine_Data" in raw_data.columns):
            parsed_rows = []
            cols_to_scan = ["Machine_Data"] if "Machine_Data" in raw_data.columns else raw_data.columns
            
            for col in cols_to_scan:
                for val in raw_data[col].dropna():
                    # Parse using regex matching pattern blocks containing key-value configurations like !Na=136.36#
                    match = re.search(r'!([^=]+)=([^#]+)#', str(val))
                    if match:
                        param_key = match.group(1).strip()
                        # Ignore system identifiers that are not physical measurement parameters
                        if "ID" not in param_key.upper():
                            parsed_rows.append({
                                "Parameter": param_key,
                                "SLOPE": match.group(2).strip()
                            })
            if parsed_rows:
                raw_data = pd.DataFrame(parsed_rows)

        # Sync and format column signatures
        raw_data.columns = [str(col).strip() for col in raw_data.columns]

        if "Parameter" in raw_data.columns and "SLOPE" in raw_data.columns:
            
            # --- MEDICAL DATA MAPS (UNITS & REFERENCE RANGES) ---
            reference_map = {
                "na": {"name": "Sodium", "unit": "mmol/L", "range": "130-145"},
                "sodium": {"name": "Sodium", "unit": "mmol/L", "range": "130-145"},
                "k": {"name": "Potassium", "unit": "mmol/L", "range": "3.44-4.55"},
                "potassium": {"name": "Potassium", "unit": "mmol/L", "range": "3.44-4.55"},
                "cl": {"name": "Chloride", "unit": "mmol/L", "range": "92-112"},
                "chloride": {"name": "Chloride", "unit": "mmol/L", "range": "92-112"},
                "ica": {"name": "Ionized Calcium", "unit": "mmol/L", "range": "1.00-1.35"},
                "calcium": {"name": "Ionized Calcium", "unit": "mmol/L", "range": "1.00-1.35"}
            }

            filtered_df = raw_data[["Parameter", "SLOPE"]].copy()
            filtered_df["norm_key"] = filtered_df["Parameter"].str.lower().str.strip()
            filtered_df = filtered_df[filtered_df["norm_key"].isin(reference_map.keys())]

            final_report_rows = []
            for _, row in filtered_df.iterrows():
                ref_info = reference_map[row["norm_key"]]
                final_report_rows.append({
                    "Parameter": ref_info["name"],
                    "Value": row["SLOPE"], 
                    "Unit": ref_info["unit"],
                    "Biological Reference Range": ref_info["range"]
                })
            
            report_df = pd.DataFrame(final_report_rows)

            # --- SECTION 3: DISPLAY DASHBOARD PREVIEW ---
            st.markdown("<h2 style='text-align: center; margin-top: 10px; font-weight: bold;'>Patient Test Report</h2>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"**Patient Name:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.patient_name}")
                st.markdown(f"**Lab No:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.lab_no}")
                st.markdown(f"**Age/Gender:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.age}/{st.session_state.gender}")
                st.markdown(f"**Ref.Doctor:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.ref_doctor}")
                st.markdown(f"**Hospital:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.hospital}")

            with info_col2:
                st.markdown(f"**Registered On:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.registered_on}")
                st.markdown(f"**Collected On:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.collected_on}")
                st.markdown(f"**Authorized On:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.authorized_on}")
                st.markdown(f"**Printed On:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.printed_on}")
                st.markdown(f"**LIS number:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.lis_number}")

            st.markdown("<br><h3 style='text-align: center; color: #1a365d; letter-spacing: 1px; font-weight: bold;'>ELECTROLYTE PANEL</h3>", unsafe_allow_html=True)
            st.dataframe(report_df, use_container_width=True, hide_index=True)
            
            st.markdown("<p style='text-align: center; color: gray; font-size: 14px; margin-top: 20px;'>End of Report</p>", unsafe_allow_html=True)
            st.markdown("---")

            # --- SECTION 4: NATIVE PDF DOWNLOAD BUTTON ---
            patient_meta = {
                "patient_name": st.session_state.patient_name, "lab_no": st.session_state.lab_no,
                "age": st.session_state.age, "gender": st.session_state.gender, "ref_doctor": st.session_state.ref_doctor,
                "hospital": st.session_state.hospital, "lis_number": st.session_state.lis_number,
                "registered_on": st.session_state.registered_on, "collected_on": st.session_state.collected_on,
                "authorized_on": st.session_state.authorized_on, "printed_on": st.session_state.printed_on
            }
            
            pdf_data = generate_pdf(patient_meta, report_df)

            st.download_button(
                label="📥 Download Doctor Prescription / PDF Report",
                data=pdf_data,
                file_name=f"Medical_Report_{st.session_state.lab_no}.pdf",
                mime="application/pdf"
            )
            
        else:
            st.error("Error parsing file structure: 'Parameter' or 'SLOPE' data format could not be processed from the file layout.")
    except Exception as e:
        st.error(f"Execution Error processing file: {e}")
else:
    st.info("Awaiting machine data file upload to display the complete report panel.")