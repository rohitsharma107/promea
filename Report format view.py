import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

Patient_name="SALMAN KHAN"
Lab_no="1234"
Age="99"
Gender="Male"
Ref_Doctor="Dr.Rohit"
Hospital="Promea"
Registered_on="20-06-2026 10:47"
Collected_on="21-06-2026 11:30"
Authorized_on="21-06-2026 11:40"
Printed_on="21-06-2026 11:40"
Lis_number="8684683726823"

report_df =pd.DataFrame({
    "Parameters":["sodium","Potassium","Chloride"],
    "Value":[138.20,2.43,109.40],
    "Unit":["mmol/L","mmol/L","mmol/L"],
    "Biological_Reference_Range":["135-150","3.5-5.1","94-110"]
})
st.markdown("""
<style>
.report-box{
    border:2px solid black;
    padding:20px;
    background:white;
    color:black;
}
.header{
    text-align:center;
    font-size:24px;
    font-weight:bold;
    margin-bottom:20px;
            <br>
}

.info-table{
    width:100%;
    border-collapse:collapse;
}

.info-table td{
    padding:4px;
    font-size:15px;
}

.result-table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}

.result-table th,
.result-table td{
    border:1px solid black;
    padding:8px;
    text-align:center;
}
  .footer{
margin-top:50px;
text-align:right;
font-weight:bold;       
}
</style>
""", unsafe_allow_html=True)
html=f"""
<div class="Report-Box">
<div class="header">
Patient Test Report
</div>

<table class="info-table" style="margin-top: 20px; width: 100%;">

<tr>
<td><b>Patient Name</b></td>
<td>{Patient_name}</td>

<td><b>Registered On</b></td>
<td>{Registered_on}</td>
</tr>

<tr>
<td><b>Lab No</b></td>
<td>{Lab_no}</td>

<td><b>Collected On</b></td>
<td>{Collected_on}</td>
</tr>

<tr>
<td><b>Age/Gender</b></td>
<td>{Age}/{Gender}</td>

<td><b>Authorized On</b></td>
<td>{Authorized_on}</td>
</tr>

<td><b>Ref.Doctor</b></td>
<td>{Ref_Doctor}</td>

<td><b>Printed On</b></td>
<td>{Printed_on}</td>
</tr>

<td><b>Hospital</b></td>
<td>{Hospital}</td>

<td><b>LIS number</b></td>
<td>{Lis_number}</td>

</table>

<br>
<h3 style="text-align:center;">
ELECTROLYTE PANEL
</h3>

<table class="result-table">

<tr>
<th>Parameter</th>
<th>Value</th>
<th>Unit</th>
<th>iological Reference Range</th>
</tr>

<tr>
<td>Sodium</td>
<td>138</td>
<td>mmol/L</td>
<td>135-150</td>
</tr>

<tr>
<td>Potassium</td>
<td>2.43</td>
<td>mmol/L</td>
<td>3.5-5.1</td>
</tr>

<tr>
<td>Chloride</td>
<td>109.40</td>
<td>mmol/L</td>
<td>94-110</td>
</tr>
</table>

<div class="footer" style="display: flex; justify-content: center;  align-items: center; width: 100%; text-align: center;">
   End of Report
</div>

</div>
"""
st.markdown(html, unsafe_allow_html=True)