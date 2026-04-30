import streamlit as st
import pandas as pd
import os

# Nom du fichier immuable
NOM_FICHIER = "donnees_agro.csv"

st.set_page_config(page_title="momha AgroStat INF232", layout="centered")
st.title("AgroStat : Collecte et Analyse")

# --- PARTIE 1 : COLLECTE (SANS MODIFICATION) ---
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
            nouvelle_ligne = pd.DataFrame([[culture, prix, humidite, zone]], 
                                         columns=["Culture", "Prix", "Humidite", "Zone"])
            if not os.path.exists(NOM_FICHIER):
                nouvelle_ligne.to_csv(NOM_FICHIER, index=False)
            else:
                nouvelle_ligne.to_csv(NOM_FICHIER, mode='a', header=False, index=False)
            st.success("Donnee enregistree !")
            # Cette commande force Streamlit a relire tout le code pour mettre l'analyse a jour
            st.rerun()
        else:
            st.error("Remplissez tous les champs.")

st.markdown("---")

# --- PARTIE 2 : ANALYSE DESCRIPTIVE (CORRIGEE) ---
st.header("Analyse Descriptive")

if os.path.exists(NOM_FICHIER):
    try:
        # 1. Lecture forcee avec Pandas
        df_analyse = pd.read_csv(NOM_FICHIER)
        
        # 2. Nettoyage de securite pour l'analyse
        # On s'assure que 'Prix' est bien traite comme un nombre
        df_analyse["Prix"] = pd.to_numeric(df_analyse["Prix"], errors='coerce')
        
        if not df_analyse.empty:
            # Affichage des compteurs
            col_a, col_b = st.columns(2)
            nb_entrees = len(df_analyse)
            moyenne = round(df_analyse["Prix"].mean(), 1)
            
            col_a.metric("Total Collectes", nb_entrees)
            col_b.metric("Prix Moyen (FCFA)", f"{moyenne}")
            
            # 3. Graphique descriptif
            st.write("### Visualisation des prix moyens")
            # Agregation pour le graphique
            stats_produit = df_analyse.groupby("Culture")["Prix"].mean()
            st.bar_chart(stats_produit)
            
            # 4. Affichage du tableau historique
            st.write("### Historique complet du fichier CSV")
            st.dataframe(df_analyse, use_container_width=True)
            
        else:
            st.info("Le fichier est vide pour le moment.")
            
    except Exception as e:
        st.error(f"Erreur lors de la lecture de l'analyse : {e}")
else:
    st.info("En attente de la premiere collecte pour generer l'analyse.")
