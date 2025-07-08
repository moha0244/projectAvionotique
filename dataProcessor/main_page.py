import streamlit as st
import pandas as pd
from io import StringIO

# Étape 1 : Sélection des colonnes à afficher
def show_column_selection(df):
    st.markdown("Choisissez les colonnes que vous souhaitez visualiser dans le tableau de données.")
    available_columns = df.columns.tolist()
    mode = st.selectbox("Mode de sélection des colonnes", ["Tout afficher", "Sélection personnalisée"], key="select_mode_param")

    if mode == "Tout afficher":
        return available_columns
    return st.multiselect("Colonnes à inclure", options=available_columns, default=[], key="filter_columns_parameter")

def choice_column_filtered_parameter(df):
    with st.expander("Étape 1 : Sélectionner les colonnes à afficher", expanded=True):
        selected_columns = show_column_selection(df)
        if not selected_columns:
            st.warning("Veuillez sélectionner au moins une colonne.")
            return None
        return df[selected_columns]

# Étape 2 : Sélection des colonnes à filtrer
def choice_column_filtered_search(selected_columns):
    with st.expander("Étape 2 : Sélectionner les colonnes à filtrer (facultatif)", expanded=True):
        if not selected_columns:
            st.info("Aucune colonne sélectionnée à l'étape précédente.")
            return
        filter_columns = st.multiselect("Colonnes pour les filtres", options=selected_columns, default=[], key="filter")
        st.session_state.filter_columns = filter_columns

# Chargement et lecture du fichier
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

# Page principale
def main_page():
    st.title("Analyseur de données - Téléversement")

    # Vérifier si un fichier est déjà stocké
    if "uploaded_file" not in st.session_state:
        uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=['csv'])
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"Fichier chargé : {uploaded_file.name}")
    else:
        st.success(f"Fichier déjà chargé : {st.session_state.uploaded_file.name}")
        if st.button(" Changer de fichier"):
            del st.session_state.uploaded_file
            st.rerun()
        uploaded_file = st.session_state.uploaded_file

    if "uploaded_file" in st.session_state:
        filtered_df = load_and_prepare_data(uploaded_file)
        if filtered_df is not None:
            choice_column_filtered_search(filtered_df.columns.tolist())
            st.session_state.original_df = filtered_df
            st.session_state.current_df = filtered_df.copy()
            if st.button("Afficher les données"):
                st.session_state.page = "data_viewer"
                st.rerun()
        else:
            st.error("Impossible de traiter le fichier.")
