import streamlit as st

# Valeurs uniques pour filtrage
def get_unique_column_values(df, column_name):
    try:
        return [str(val) for val in df[column_name].dropna().unique()]
    except Exception:
        return []

# Page de visualisation des données
def apply_filters(df, filter_columns):
    for col in filter_columns:
        if col not in df.columns:
            continue
        options = get_unique_column_values(df, col)
        user_input = st.text_input(col, '', key=f"filter_{col}_{st.session_state.filter_reset_counter}")
        if user_input:
            df = df[df[col].astype(str).str.contains(user_input, case=False, na=False)]
    return df



def data_viewer_page():
    st.title("Analyseur de données - Visualisation")
    if 'original_df' not in st.session_state:
        st.warning("Aucun fichier chargé.")
        if st.button("Retour au téléversement"):
            st.session_state.page = "main"
            st.rerun()
        return

    if 'filter_reset_counter' not in st.session_state:
        st.session_state.filter_reset_counter = 0

    with st.sidebar:
        st.header("Filtres dynamiques")
        filter_columns = st.session_state.get("filter_columns", [])
        df = st.session_state.original_df.copy()
        df = apply_filters(df, filter_columns)
        st.session_state.current_df = df

        if not filter_columns:
            st.info("Aucun filtre sélectionné.")
        elif st.button("Réinitialiser les filtres"):
            st.session_state.filter_reset_counter += 1
            st.rerun()

        if st.button("Retour au téléversement"):
            st.session_state.page = "main"
            st.rerun()

    st.subheader("Données filtrées")
    st.dataframe(st.session_state.current_df)

    csv = st.session_state.current_df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger au format CSV", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")


