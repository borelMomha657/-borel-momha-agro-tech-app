import streamlit as st
import pandas as pd
import os

# --- NOM DU FICHIER DE SAUVEGARDE ---
NOM_FICHIER = "donnees_agro.csv"

# --- FONCTION POUR CHARGER LES DONNEES ---
def charger_donnees():
    if os.path.exists(NOM_FICHIER):
        return pd.read_csv(NOM_FICHIER)
    else:
        # Si le fichier n'existe pas, on retourne un tableau vide avec les colonnes
        return pd.DataFrame(columns=["Culture", "Prix", "Humidite", "Zone"])

# --- FONCTION POUR SAUVEGARDER LES DONNEES ---
def sauvegarder_donnee(culture, prix, humidite, zone):
    nouvelle_ligne = pd.DataFrame([[culture, prix, humidite, zone]], 
                                 columns=["Culture", "Prix", "Humidite", "Zone"])
    
    if not os.path.exists(NOM_FICHIER):
        nouvelle_ligne.to_csv(NOM_FICHIER, index=False)
    else:
        # On ajoute la ligne a la fin du fichier existant (mode 'a' pour append)
        nouvelle_ligne.to_csv(NOM_FICHIER, mode='a', header=False, index=False)

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="AgroStat INF232", layout="centered")

st.title("AgroStat : Collecte et Analyse")
st.write("TP INF 232 EC2 - Stockage par fichier CSV")

menu = ["Collecte", "Analyse Descriptive"]
choix = st.sidebar.selectbox("Menu", menu)

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
                sauvegarder_donnee(culture, prix, humidite, zone)
                st.success("Donnees enregistrees dans le fichier CSV")
            else:
                st.error("Erreur : Veuillez remplir la zone et le prix.")

elif choix == "Analyse Descriptive":
    st.subheader("Visualisation des donnees")
    df = charger_donnees()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Collectes", len(df))
        col2.metric("Prix Moyen", f"{round(df['Prix'].mean(), 1)} FCFA")
        
        st.write("### Prix moyen par produit")
        chart_data = df.groupby('Culture')['Prix'].mean()
        st.bar_chart(chart_data)
        
        st.write("### Historique des donnees (Tableau CSV)")
        st.dataframe(df, use_container_width=True)
        
        # Bouton pour telecharger le fichier cree
        csv_file = df.to_csv(index=False).encode('utf-8')
        st.download_button("Telecharger le fichier CSV", csv_file, "donnees_agro.csv", "text/csv")
    else:
        st.info("Le fichier CSV est vide ou n'existe pas encore. Effectuez une collecte.")
