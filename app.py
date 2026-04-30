import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION DU STOCKAGE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'agro_data_expert.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # On ajoute plus de colonnes pour la diversité des données
    c.execute('''CREATE TABLE IF NOT EXISTS collectes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  date TEXT, produit TEXT, categorie TEXT, prix REAL, 
                  quantite INTEGER, humidite INTEGER, meteo TEXT, 
                  sol TEXT, zone TEXT, transport TEXT)''')
    conn.commit()
    conn.close()

def sauvegarder(date, produit, cat, prix, qte, hum, meteo, sol, zone, transport):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO collectes (date, produit, categorie, prix, quantite, humidite, meteo, sol, zone, transport) 
                 VALUES (?,?,?,?,?,?,?,?,?,?)''', (date, produit, cat, prix, qte, hum, meteo, sol, zone, transport))
    conn.commit()
    conn.close()

# --- INTERFACE ---
st.set_page_config(page_title="AgroStat Pro", layout="wide")
init_db()

st.title("🚜 AgroStat Pro : Système Expert de Collecte")
st.sidebar.header("Navigation")
menu = ["Saisie Expert", "Analyse Descriptive", "Exploration des Données"]
choix = st.sidebar.radio("Menu", menu)

if choix == "Saisie Expert":
    st.subheader("📝 Formulaire de Collecte Multidimensionnel")
    
    with st.form("form_expert", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("### 🍉 Produit")
            categorie = st.selectbox("Catégorie", ["Céréales", "Tubercules", "Rentes (Export)", "Fruits & Légumes"])
            
            # Liste diversifiée selon la catégorie
            produits_dict = {
                "Céréales": ["Maïs", "Riz", "Sorgho", "Mil"],
                "Tubercules": ["Manioc", "Igname", "Macabo", "Patate douce"],
                "Rentes (Export)": ["Cacao", "Café", "Palmiste", "Coton"],
                "Fruits & Légumes": ["Banane-Plantain", "Ananas", "Avocat", "Tomate", "Piment"]
            }
            produit = st.selectbox("Produit spécifique", produits_dict[categorie])
            date = st.date_input("Date de collecte")

        with col2:
            st.write("### 💰 Économie & Quantité")
            prix = st.number_input("Prix unitaire (FCFA)", min_value=0.0)
            quantite = st.number_input("Quantité disponible (Kg/Sacs)", min_value=0)
            transport = st.select_slider("État des routes/transport", options=["Mauvais", "Moyen", "Bon", "Excellent"])

        with col3:
            st.write("### 🌍 Environnement")
            zone = st.text_input("Zone / Bassin de production", placeholder="Ex: Moungo, Sanaga...")
            meteo = st.selectbox("Conditions Météo", ["Ensoleillé", "Pluvieux", "Orageux", "Brouillard"])
            sol = st.selectbox("Type de Sol", ["Ferralitique (Rouge)", "Volcanique (Noir)", "Sablonneux", "Argileux"])
            humidite = st.slider("Humidité du sol (%)", 0, 100, 45)

        submit = st.form_submit_button("🚀 Enregistrer dans la base permanente")
        
        if submit:
            if zone and prix > 0:
                sauvegarder(str(date), produit, categorie, prix, quantite, humidite, meteo, sol, zone, transport)
                st.success(f"Données enregistrées pour : {produit} ({zone})")
            else:
                st.error("Veuillez remplir les champs obligatoires (Zone et Prix).")

elif choix == "Analyse Descriptive":
    st.subheader("📊 Dashboard d'Analyse Multivariée")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM collectes", conn)
    conn.close()

    if not df.empty:
        # KPI
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Collectes", len(df))
        c2.metric("Prix Moyen", f"{round(df['prix'].mean(), 0)} FCFA")
        c3.metric("Stock Total", f"{df['quantite'].sum()} unités")
        c4.metric("Humidité Moy.", f"{round(df['humidite'].mean(), 1)}%")

        st.markdown("---")
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.write("#### 🥧 Répartition par Catégorie")
            fig1, ax1 = plt.subplots()
            df['categorie'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, cmap='Set3')
            st.pyplot(fig1)

        with col_right:
            st.write("#### 🌡️ Humidité selon la Météo")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x='meteo', y='humidite', data=df, ax=ax2)
            st.pyplot(fig2)

        st.write("#### 📈 Évolution du Prix par Produit")
        st.line_chart(df.pivot_table(index='date', columns='produit', values='prix'))

    else:
        st.warning("Aucune donnée disponible.")

else:
    st.subheader("🗄️ Exploration de la Base de Données")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM collectes", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
