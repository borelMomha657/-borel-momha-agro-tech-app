import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PERSISTENCE ---
# On définit le chemin de la base de données SQLite
DB_PATH = os.path.join(os.getcwd(), 'agro_data_tp.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS collectes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  culture TEXT, prix REAL, humidite INTEGER, zone TEXT)''')
    conn.commit()
    conn.close()

def sauvegarder_donnee(culture, prix, humidite, zone):
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

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="AgroStat - INF 232", layout="wide")
init_db()

# Barre latérale (Sidebar)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller vers :", ["Collecte de données", "Analyse Descriptive", "Aide / Programme"])

if page == "Collecte de données":
    st.title("📥 Collecte de données Agro-Tech")
    st.info("Les données saisies ici sont stockées de manière permanente dans la base SQLite.")
    
    with st.form("form_collecte", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            culture = st.selectbox("Culture", ["Maïs", "Manioc", "Cacao", "Café", "Banane", "Arachide"])
            prix = st.number_input("Prix au kg (FCFA)", min_value=0.0, step=50.0)
        with col2:
            humidite = st.slider("Taux d'humidité (%)", 0, 100, 50)
            zone = st.text_input("Localité / Zone de production")
        
        btn = st.form_submit_button("Enregistrer les données")
        
        if btn:
            if zone and prix > 0:
                sauvegarder_donnee(culture, prix, humidite, zone)
                st.success(f"✅ Données pour {culture} sauvegardées !")
            else:
                st.error("❌ Veuillez remplir tous les champs (Prix et Zone).")

elif page == "Analyse Descriptive":
    st.title("📊 Tableau de Bord d'Analyse")
    df = charger_donnees()
    
    if not df.empty:
        # 1. Indicateurs clés
        c1, c2, c3 = st.columns(3)
        c1.metric("Collectes totales", len(df))
        c2.metric("Prix Moyen", f"{round(df['prix'].mean(), 1)} FCFA")
        c3.metric("Humidité Moyenne", f"{round(df['humidite'].mean(), 1)} %")
        
        st.markdown("---")
        
        # 2. Graphiques
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("### Répartition des cultures")
            fig1, ax1 = plt.subplots()
            df['culture'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, cmap='viridis')
            st.pyplot(fig1)
            
        with col_b:
            st.write("### Prix moyen par culture")
            prix_moy = df.groupby('culture')['prix'].mean()
            st.bar_chart(prix_moy)

        # 3. Tableau de données
        st.write("### Historique des données enregistrées")
        st.dataframe(df, use_container_width=True)
        
        # Bouton export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger les données (CSV)", csv, "data_agro.csv", "text/csv")
    else:
        st.warning("La base de données est vide. Veuillez effectuer une collecte.")

else:
    st.title("📚 Programme INF 232 EC2")
    st.write("**Objectif du TP :** Collecte et analyse descriptive des données.")
    st.write("**Professeur :** Rollin Francis (rollinfrancis28@gmail.com)")
    st.markdown("""
    1. Régression linéaire simple
    2. Régression linéaire multiple
    3. Réduction de dimensionnalité
    4. Classification supervisée
    5. Classification non-supervisée
    """)
