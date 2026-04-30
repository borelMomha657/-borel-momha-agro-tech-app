import streamlit as st
import pandas as pd
import os

# Nom du fichier unique
NOM_FICHIER = "donnees_agro.csv"

# Configuration de la page
st.set_page_config(page_title="AgroStat INF232", layout="centered")

# --- TITRE ---
st.title("AgroStat : Collecte et Analyse")
st.write("TP INF 232 EC2 - MOMHA AGRO TECH")

# --- NAVIGATION ---
menu = ["Collecte des données", "Analyse Descriptive"]
choix = st.sidebar.selectbox("Menu", menu)

# --- LOGIQUE DE LECTURE (Sert aux deux onglets) ---
if os.path.exists(NOM_FICHIER):
    df = pd.read_csv(NOM_FICHIER)
else:
    # Si pas de fichier, on cree un tableau vide structure
    df = pd.DataFrame(columns=["Culture", "Prix", "Humidite", "Zone"])

# --- ONGLET 1 : COLLECTE ---
if choix == "Collecte":
    st.subheader("Formulaire de saisie")
    
    with st.form("form_csv", clear_on_submit=True):
        culture = st.selectbox("Produit Agricole", [
            "Mais", "Manioc", "Cacao", "Cafe", "Banane-Plantain", 
            "Ananas", "Avocat", "Tomate", "Piment", "Riz", "Arachide"
        ])
        prix = st.number_input("Prix au kg (FCFA)", min_value=0.0, step=10.0)
        humidite = st.slider("Taux humidite (%)", 0, 100, 50)
        zone = st.text_input("Localite / Zone de collecte")
        
        soumettre = st.form_submit_button("Enregistrer")
        
        if soumettre:
            if zone and prix > 0:
                # On ajoute la nouvelle ligne au DataFrame existant
                nouvelle_ligne = pd.DataFrame([[culture, prix, humidite, zone]], 
                                             columns=["Culture", "Prix", "Humidite", "Zone"])
                # On sauvegarde (Si le fichier n'existe pas, on met l'entete, sinon non)
                if not os.path.exists(NOM_FICHIER):
                    nouvelle_ligne.to_csv(NOM_FICHIER, index=False)
                else:
                    nouvelle_ligne.to_csv(NOM_FICHIER, mode='a', header=False, index=False)
                
                st.success("Donnees enregistrees ! Allez dans l'onglet Analyse pour voir le tableau.")
                # Force le rafraichissement pour l'analyse
                st.rerun()
            else:
                st.error("Veuillez remplir la zone et le prix.")

# --- ONGLET 2 : ANALYSE ---
elif choix == "Analyse Descriptive":
    st.subheader("Visualisation des donnees")
    
    if not df.empty:
        # 1. Statistiques Rapides
        col1, col2 = st.columns(2)
        col1.metric("Collectes", len(df))
        # Conversion forcee en numerique au cas ou il y aurait un bug de type
        df["Prix"] = pd.to_numeric(df["Prix"], errors='coerce')
        col2.metric("Prix Moyen", f"{round(df['Prix'].mean(), 1)} FCFA")
        
        # 2. Graphique
        st.write("### Prix moyen par produit")
        chart_data = df.groupby('Culture')['Prix'].mean()
        st.bar_chart(chart_data)
        
        # 3. Affichage du Tableau (Ce qui manquait peut-etre)
        st.write("### Historique des donnees (CSV)")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("Le fichier est vide. Veuillez d'abord saisir des donnees dans l'onglet Collecte.")
