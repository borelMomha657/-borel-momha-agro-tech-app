import streamlit as st
import pandas as pd
import os

# Nom du fichier pour sauvegarder les donnees
NOM_FICHIER = "donnees_agro.csv"

# Configuration de la page
st.set_page_config(page_title="AgroStat INF232", layout="centered")

st.title("AgroStat : Collecte et Analyse")
st.write("TP INF 232 - borel momha agro tech")

# --- 1. FORMULAIRE DE COLLECTE (En haut de la page) ---
st.header("Saisie des donnees")
with st.form("form_unique", clear_on_submit=True):
    culture = st.selectbox("Produit Agricole", [
        "Mais", "Manioc", "Cacao", "Cafe", "Banane-Plantain", 
        "Ananas", "Avocat", "Tomate", "Piment", "Riz", "Arachide"
    ])
    prix = st.number_input("Prix au kg (FCFA)", min_value=0.0, step=10.0)
    humidite = st.slider("Taux humidite (%)", 0, 100, 50)
    zone = st.text_input("Localite / Zone de collecte")
    
    soumettre = st.form_submit_button("Enregistrer la donnee")
    
    if soumettre:
        if zone and prix > 0:
            # Creation de la ligne
            nouvelle_ligne = pd.DataFrame([[culture, prix, humidite, zone]], 
                                         columns=["Culture", "Prix", "Humidite", "Zone"])
            # Sauvegarde immediate
            if not os.path.exists(NOM_FICHIER):
                nouvelle_ligne.to_csv(NOM_FICHIER, index=False)
            else:
                nouvelle_ligne.to_csv(NOM_FICHIER, mode='a', header=False, index=False)
            st.success("Donnee enregistree avec succes !")
        else:
            st.error("Veuillez remplir le prix et la zone.")

st.markdown("---")

# --- 2. ANALYSE DESCRIPTIVE (Juste en dessous) ---
st.header("Analyse et Historique")

if os.path.exists(NOM_FICHIER):
    # Lecture du fichier
    df = pd.read_csv(NOM_FICHIER)
    
    if not df.empty:
        # Statistiques en colonnes
        c1, c2 = st.columns(2)
        c1.metric("Nombre de collectes", len(df))
        # Calcul de la moyenne
        prix_moyen = round(df["Prix"].mean(), 1)
        c2.metric("Prix Moyen Global", f"{prix_moyen} FCFA")
        
        # Graphique simple
        st.write("### Graphique des prix par produit")
        chart_data = df.groupby("Culture")["Prix"].mean()
        st.bar_chart(chart_data)
        
        # Affichage du tableau
        st.write("### Tableau des donnees enregistrees")
        st.dataframe(df, use_container_width=True)
        
        # Option de suppression (pour vider la base si besoin)
        if st.button("Vider la base de donnees"):
            os.remove(NOM_FICHIER)
            st.warning("Base de donnees supprimee. Rechargez la page.")
    else:
        st.info("Le fichier est vide. Enregistrez une donnee ci-dessus.")
else:
    st.info("Aucune donnee enregistree pour le moment.")

