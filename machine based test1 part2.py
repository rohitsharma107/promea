import streamlit as st
import pandas as pd
import re

st.title("Promea Machine Data Collection App")

st.write("This app collects machine data and displays it systematically.")

uploaded_file = st.file_uploader(
    "Upload machine data file",
    type=["csv", "xlsx", "txt", "log"]
)

def read_log_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    rows = []

    for line in lines:
        line = line.replace("#", "").replace("@", "").strip()

        if "=" in line:
            field, value = line.split("=", 1)
            field = field.strip()
            value = value.strip()

            rows.append([field, value])

    return pd.DataFrame(rows, columns=["Field", "Value"])

if uploaded_file is not None:
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        data = pd.read_excel(uploaded_file)

    elif file_name.endswith(".txt"):
        data = pd.read_csv(uploaded_file, sep=",", engine="python")

    elif file_name.endswith(".log"):
        data = read_log_file(uploaded_file)

    st.subheader("Collected Data")
    st.dataframe(data, use_container_width=True)

    st.subheader("Report View")

    st.markdown("""
    <div style="border:2px solid black; padding:25px; width:700px; background-color:white;">
        <h2 style="text-align:center;">PROMEA THERAPEUTICS</h2>
        <h3 style="text-align:center;">Electrolyte Analyzer Report</h3>
        <hr>
    """, unsafe_allow_html=True)

    for index, row in data.iterrows():
        st.markdown(
            f"""
            <p style="font-size:18px;">
                <b>{row.iloc[0]}</b> : {row.iloc[1]}
            </p>
            """,
            unsafe_allow_html=True
        )

    st.markdown("""
        <hr>
        <p style="text-align:center;">This is a system generated report.</p>
    </div>
    """, unsafe_allow_html=True)

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Organized CSV",
        csv,
        "organized_machine_data.csv",
        "text/csv"
    )

else:
    st.info("Please upload CSV, Excel, TXT, or LOG file.")
    #