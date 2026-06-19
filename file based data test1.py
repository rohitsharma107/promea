import streamlit as st
import pandas as pd

st.title("Promea Data Collection App")

st.write("This app collects data files and displays them systematically.")

uploaded_file = st.file_uploader(
    "Upload a data file",
    type=["csv", "xlsx", "txt"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        data = pd.read_excel(uploaded_file)

    elif uploaded_file.name.endswith(".txt"):
        data = pd.read_csv(uploaded_file, sep=",")
    
    st.subheader("Collected Data")
    st.dataframe(data)

    st.subheader("Column Names Found")
    st.write(list(data.columns))

    st.subheader("Select Columns For Chart")

    text_column = st.selectbox("Select parameters/name column", data.columns)
    value_column = st.selectbox("Select value column", data.columns)

    st.subheader("Simple Chart")
    st.bar_chart(data.set_index(text_column)[value_column])

else:
    st.info("Please upload CSV, Excel, or TXT file.")