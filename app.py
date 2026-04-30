import streamlit as st
import pandas as pd
import os

# Nom du fichier
NOM_FICHIER = "donnees_agro.csv"

st.set_page_config(page_title="AgroStat INF232", layout="centered")
st.title("AgroStat : Collecte et Analyse")

# --- PARTIE 1 : COLLECTE ---
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
            # On cree la ligne avec exactement 4 colonnes
            nouvelle_ligne = pd.DataFrame([[culture, prix, humidite, zone]], 
                                         columns=["Culture", "Prix", "Humidite", "Zone"])
            
            if not os.path.exists(NOM_FICHIER):
                nouvelle_ligne.to_csv(NOM_FICHIER, index=False)
            else:
                nouvelle_ligne.to_csv(NOM_FICHIER, mode='a', header=False, index=False)
            
            st.success("Donnee enregistree !")
            st.rerun()
        else:
            st.error("Remplissez tous les champs.")

st.markdown("---")

# --- PARTIE 2 : ANALYSE DESCRIPTIVE (CORRECTION DU BUG DE TOKENIZATION) ---
st.header("Analyse Descriptive")

if os.path.exists(NOM_FICHIER):
    try:
        # La correction est ici : on force la lecture en ignorant les lignes mal formees
        # on_bad_lines='skip' permet d'eviter le crash si une ligne a 3 colonnes au lieu de 4
        df_analyse = pd.read_csv(NOM_FICHIER, on_bad_lines='skip')
        
        # On s'assure que les colonnes sont bien nommees
        df_analyse.columns = ["Culture", "Prix", "Humidite", "Zone"]
        
        # Securite numerique
        df_analyse["Prix"] = pd.to_numeric(df_analyse["Prix"], errors='coerce')
        
        if not df_analyse.empty:
            col_a, col_b = st.columns(2)
            col_a.metric("Total Collectes", len(df_analyse))
            col_b.metric("Prix Moyen (FCFA)", f"{round(df_analyse['Prix'].mean(), 1)}")
            
            st.write("### Graphique des prix")
            st.bar_chart(df_analyse.groupby("Culture")["Prix"].mean())
            
            st.write("### Historique")
            st.dataframe(df_analyse, use_container_width=True)
            
            # Bouton de secours pour "nettoyer" si le bug persiste
            if st.button("Reinitialiser le fichier (Effacer tout)"):
                os.remove(NOM_FICHIER)
                st.rerun()
        else:
            st.info("Le fichier est vide.")
            
    except Exception as e:
        st.error(f"Erreur de lecture. Cliquez sur le bouton en bas pour reinitialiser.")
        if st.button("Nettoyer le fichier corrompu"):
            os.remove(NOM_FICHIER)
            st.rerun()
else:
    st.info("Aucune donnee detectee.")
