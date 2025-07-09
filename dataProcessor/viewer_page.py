import streamlit as st

# Get unique values for filtering
def get_unique_column_values(df, column_name):
    try:
        return [str(val) for val in df[column_name].dropna().unique()]
    except Exception:
        return []

# Filtering logic
def apply_filters(df, filter_columns):
    for col in filter_columns:
        if col not in df.columns:
            continue
        user_input = st.text_input(f"{col}", '', key=f"filter_{col}_{st.session_state.filter_reset_counter}")
        if user_input:
            df = df[df[col].astype(str).str.contains(user_input, case=False, na=False)]
    return df

# Page to view and filter data
def data_viewer_page():
    st.title("Data Viewer")

    if 'original_df' not in st.session_state:
        st.warning("No file uploaded.")
        if st.button("Back to Upload"):
            st.session_state.page = "main"
            st.rerun()
        return

    if 'filter_reset_counter' not in st.session_state:
        st.session_state.filter_reset_counter = 0

    with st.sidebar:
        st.header("Dynamic Filters")
        filter_columns = st.session_state.get("filter_columns", [])
        df = st.session_state.original_df.copy()
        df = apply_filters(df, filter_columns)
        st.session_state.current_df = df

        if not filter_columns:
            st.info("No filters selected.")
        elif st.button("Reset Filters"):
            st.session_state.filter_reset_counter += 1
            st.rerun()

        if st.button("Back to Upload"):
            st.session_state.page = "main"
            st.rerun()

    st.subheader("Filtered Data")
    st.dataframe(st.session_state.current_df)

    csv = st.session_state.current_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")
