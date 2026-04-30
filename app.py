import streamlit as st
import pandas as pd
import os

# --- FICHIER DE STOCKAGE ---
# Ce fichier sera créé automatiquement à la racine de ton projet
FILE_NAME = "donnees_agro.csv"

def sauvegarder_csv(df_nouvelle_ligne):
    # Si le fichier existe déjà, on ajoute la ligne, sinon on le crée
    if not os.path.isfile(FILE_NAME):
        df_nouvelle_ligne.to_csv(FILE_NAME, index=False)
    else:
        df_nouvelle_ligne.to_csv(FILE_NAME, mode='a', header=False, index=False)

# --- INTERFACE ---
st.title("🚜 AgroStat (Version CSV)")

# Formulaire de collecte
with st.form("form"):
    culture = st.selectbox("Culture", ["Maïs", "Manioc", "Cacao"])
    prix = st.number_input("Prix (FCFA)", min_value=0)
    zone = st.text_input("Zone")
    valider = st.form_submit_button("Enregistrer")
    
    if valider:
        # Création d'un petit tableau avec la nouvelle donnée
        nouvelle_donnee = pd.DataFrame([[culture, prix, zone]], columns=['Culture', 'Prix', 'Zone'])
        sauvegarder_csv(nouvelle_donnee)
        st.success("Donnée enregistrée dans le fichier CSV !")

# Analyse Descriptive
st.header("📊 Analyse des données")
if os.path.isfile(FILE_NAME):
    df_global = pd.read_csv(FILE_NAME)
    
    col1, col2 = st.columns(2)
    col1.metric("Nombre d'entrées", len(df_global))
    col2.metric("Prix Moyen", f"{round(df_global['Prix'].mean(), 1)} FCFA")
    
    st.bar_chart(df_global.groupby('Culture')['Prix'].mean())
    st.write("### Historique", df_global)
else:
    st.info("Aucune donnée pour le moment.")

