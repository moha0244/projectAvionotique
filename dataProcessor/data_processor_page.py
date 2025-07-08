import streamlit as st
from dataProcessor.viewer_page import data_viewer_page
from dataProcessor.main_page import main_page


# Routage
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "data_viewer":
        data_viewer_page()

if __name__ == "__main__":
    main()
