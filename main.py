import streamlit as st
from list_project import PROJECTS

# Configuration de la page
st.set_page_config(
    page_title="Avionic Project Portal",
    page_icon="\u2708",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_home():
    # En-tête
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #1a73e8;'> Portail des Outils Avioniques</h1>
            <p style='font-size: 1.1rem; color: #5f6368;'>
                Plateforme intégrée pour le traitement des données et configurations avioniques
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Modules Disponibles")
    st.markdown("Sélectionnez un outil dans la liste ci-dessous :")

    search_query = st.text_input(" Rechercher un outil...")


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
                if st.button("Ouvrir →", key=f"btn_{project_name}", use_container_width=True):
                    st.session_state.selected_project = project_name
                    st.rerun()

    # Pied de page
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; color: #5f6368; font-size: 0.9rem;'>
            © 2025 Département du centre d'essai avionique - Tous droits réservés
        </div>
    """, unsafe_allow_html=True)


def project_wrapper(func):
    col1, col2 = st.columns([0.85, 0.15])

    with col2:
        if st.button("Retour à l'accueil", use_container_width=True):
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

    # Contenu du projet
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