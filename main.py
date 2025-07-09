import streamlit as st
from list_project import PROJECTS

# Page configuration
st.set_page_config(
    page_title="Avionic Project Portal",
    page_icon="\u2708",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_home():
    # Header
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #1a73e8;'> Avionics Tools Portal</h1>
            <p style='font-size: 1.1rem; color: #5f6368;'>
                Integrated platform for avionics data processing and configuration
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Available Modules")
    st.markdown("Select a tool from the list below:")

    search_query = st.text_input(" Search for a tool...")

    filtered_projects = PROJECTS
    if search_query:
        query = search_query.lower()
        filtered_projects = {
            k: v for k, v in PROJECTS.items()
            if (query in k.lower() or
                query in v["description"].lower() or
                any(query in tag for tag in v["tags"]))
        }

    cols = st.columns(2)
    for idx, (project_name, project_data) in enumerate(filtered_projects.items()):
        with cols[idx % 2]:
            with st.container(border=True, height=180):
                st.markdown(f"#### {project_data['icon']} {project_name}")
                st.markdown(f"<small>{project_data['description']}</small>", unsafe_allow_html=True)
                if st.button("Open →", key=f"btn_{project_name}", use_container_width=True):
                    st.session_state.selected_project = project_name
                    st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; color: #5f6368; font-size: 0.9rem;'>
            © 2025 Avionics Test Center Department – All rights reserved
        </div>
    """, unsafe_allow_html=True)


def project_wrapper(func):
    col1, col2 = st.columns([0.85, 0.15])

    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.selected_project = None
            st.rerun()

    selected = st.session_state.selected_project
    st.markdown(f"""
    <style>
    .display {{
      text-align: center;
    }}
    </style>

    <div class="display">
      <h1>{selected}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Load the selected project module
    func()


def main():
    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None

    if st.session_state.selected_project:
        selected_project = PROJECTS[st.session_state.selected_project]
        project_wrapper(selected_project["module"].main)
    else:
        show_home()


main()
