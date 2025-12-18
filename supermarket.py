import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Business Dashboard",
    layout="wide"
)

# =====================
# LANGUAGE DICTIONARY
# =====================
LANG = {
    "id": {
        "title": "Dashboard Bisnis",
        "upload": "Unggah File Excel",
        "sheet": "Pilih Sheet",
        "summary": "Ringkasan Data",
        "chart1": "Distribusi Data Numerik",
        "chart2": "Total Nilai per Kategori",
        "chart3": "Perbandingan Top 10 Kategori",
        "chart4": "Proporsi Data",
        "chart5": "Hubungan Antar Variabel",
        "error": "File tidak valid atau kosong"
    },
    "en": {
        "title": "Business Dashboard",
        "upload": "Upload Excel File",
        "sheet": "Select Sheet",
        "summary": "Data Summary",
        "chart1": "Numeric Distribution",
        "chart2": "Total Value by Category",
        "chart3": "Top 10 Category Comparison",
        "chart4": "Data Proportion",
        "chart5": "Variable Relationship",
        "error": "Invalid or empty file"
    }
}

# =====================
# SIDEBAR
# =====================
language = st.sidebar.selectbox(
    "Language / Bahasa",
    ["Bahasa Indonesia", "English"]
)

lang = "id" if language == "Bahasa Indonesia" else "en"
text = LANG[lang]

# =====================
# TITLE
# =====================
st.title(text["title"])

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    text["upload"],
    type=["xlsx", "xls"]
)

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox(text["sheet"], xls.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

        if df.empty:
            st.error(text["error"])
            st.stop()

        # =====================
        # BASIC CLEANING
        # =====================
        df = df.dropna(how="all")

        numeric_cols = df.select_dtypes(include="number").columns
        categorical_cols = df.select_dtypes(exclude="number").columns

        st.subheader(text["summary"])
        st.write(df.head())
        st.write(df.describe())

        # =====================
        # CHART 1: HISTOGRAM
        # =====================
        st.subheader(text["chart1"])
        if len(numeric_cols) > 0:
            fig, ax = plt.subplots()
            df[numeric_cols[0]].hist(ax=ax)
            ax.set_title(numeric_cols[0])
            st.pyplot(fig)

        # =====================
        # CHART 2: BAR TOTAL
        # =====================
        st.subheader(text["chart2"])
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].sum()
            fig, ax = plt.subplots()
            grouped.plot(kind="bar", ax=ax)
            st.pyplot(fig)

        # =====================
        # CHART 3: TOP 10
        # =====================
        st.subheader(text["chart3"])
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            top10 = grouped.sort_values(ascending=False).head(10)
            fig, ax = plt.subplots()
            top10.plot(kind="barh", ax=ax)
            st.pyplot(fig)

        # =====================
        # CHART 4: PIE
        # =====================
        st.subheader(text["chart4"])
        if len(categorical_cols) > 0:
            pie_data = df[categorical_cols[0]].value_counts().head(5)
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
            st.pyplot(fig)

        # =====================
        # CHART 5: SCATTER
        # =====================
        st.subheader(text["chart5"])
        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots()
            ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            st.pyplot(fig)

    except Exception:
        st.error(text["error"])
