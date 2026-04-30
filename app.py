import streamlit as st
import pandas as pd
import sqlite3
import os

# --- LOGIQUE DE STOCKAGE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'agro_permanent.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS collectes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  culture TEXT, prix REAL, humidite INTEGER, zone TEXT)''')
    conn.commit()
    conn.close()

def ajouter_donnee(culture, prix, humidite, zone):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO collectes (culture, prix, humidite, zone) VALUES (?,?,?,?)',
              (culture, prix, humidite, zone))
    conn.commit()
    conn.close()

def charger_donnees():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM collectes", conn)
    conn.close()
    return df

# --- INTERFACE ---
st.set_page_config(page_title="AgroStat INF232", layout="centered")
init_db()

st.title("AgroStat : Collecte et Analyse")
st.write("TP INF 232 EC2 - Systeme de collecte robuste")

menu = ["Collecte", "Analyse Descriptive"]
choix = st.sidebar.selectbox("Menu", menu)

if choix == "Collecte":
    st.subheader("Formulaire de saisie")
    
    with st.form("form_simple", clear_on_submit=True):
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
                ajouter_donnee(culture, prix, humidite, zone)
                st.success("Donnees enregistrees avec succes")
            else:
                st.error("Erreur : Veuillez remplir la zone et le prix.")

elif choix == "Analyse Descriptive":
    st.subheader("Visualisation des donnees")
    df = charger_donnees()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Collectes", len(df))
        col2.metric("Prix Moyen", f"{round(df['prix'].mean(), 1)} FCFA")
        
        st.write("### Prix moyen par produit")
        # Calcul de la moyenne par produit avant affichage
        chart_data = df.groupby('culture')['prix'].mean()
        st.bar_chart(chart_data)
        
        st.write("### Historique complet")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune donnee enregistree dans la base.")
