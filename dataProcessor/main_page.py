import streamlit as st
import pandas as pd
from io import StringIO

# Step 1: Column selection
def show_column_selection(df):
    st.markdown("Choose the columns you want to display in the data table.")
    available_columns = df.columns.tolist()
    mode = st.selectbox("Column selection mode", ["Show all", "Custom selection"], key="select_mode_param")

    if mode == "Show all":
        return available_columns
    return st.multiselect("Columns to include", options=available_columns, default=[], key="filter_columns_parameter")

def choice_column_filtered_parameter(df):
    with st.expander("Step 1: Select columns to display", expanded=True):
        selected_columns = show_column_selection(df)
        if not selected_columns:
            st.warning("Please select at least one column.")
            return None
        return df[selected_columns]

# Step 2: Column filtering
def choice_column_filtered_search(selected_columns):
    with st.expander("Step 2: Select columns to filter (optional)", expanded=True):
        if not selected_columns:
            st.info("No columns selected in the previous step.")
            return
        filter_columns = st.multiselect("Columns for filtering", options=selected_columns, default=[], key="filter")
        st.session_state.filter_columns = filter_columns

# CSV parsing
def try_read_csv(uploaded_file, delimiter, encoding):
    try:
        content = uploaded_file.getvalue().decode(encoding)
        df = pd.read_csv(StringIO(content), delimiter=delimiter, low_memory=False)
        if df.shape[1] > 1:
            return df
    except Exception:
        return None

def read_csv_file(uploaded_file):
    if uploaded_file is None:
        return None
    for delimiter in [',', ';']:
        for encoding in ['utf-8', 'latin1']:
            df = try_read_csv(uploaded_file, delimiter, encoding)
            if df is not None:
                return df
    return None

def load_and_prepare_data(uploaded_file):
    df = read_csv_file(uploaded_file)
    if df is None:
        return None
    return choice_column_filtered_parameter(df)

# Main page
def main_page():
    st.title("Data Viewer - Upload")

    # Check if a file is already stored
    if "uploaded_file" not in st.session_state:
        uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"File uploaded: {uploaded_file.name}")
    else:
        st.success(f"File already loaded: {st.session_state.uploaded_file.name}")
        if st.button("Change file"):
            del st.session_state.uploaded_file
            st.rerun()
        uploaded_file = st.session_state.uploaded_file

    if "uploaded_file" in st.session_state:
        filtered_df = load_and_prepare_data(uploaded_file)
        if filtered_df is not None:
            choice_column_filtered_search(filtered_df.columns.tolist())
            st.session_state.original_df = filtered_df
            st.session_state.current_df = filtered_df.copy()
            if st.button("View data"):
                st.session_state.page = "data_viewer"
                st.rerun()
        else:
            st.error("Failed to process the file.")
