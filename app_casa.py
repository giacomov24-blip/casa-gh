import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date
import streamlit.components.v1 as components
import os

# 1. CONFIGURAZIONE UNICA (MAI DOPPIA!)
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# URL del tuo Google Sheets (già inserito quello che hai postato)
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZOO1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"
# Connessione al Database Google
conn = st.connection("gsheets", type=GSheetsConnection)

def carica_spesa_google():
    try:
        return conn.read(spreadsheet=URL_FOGLIO, worksheet="spesa")
    except:
        return pd.DataFrame(columns=["Elemento", "Categoria"])

def salva_spesa_google(df):
    conn.update(spreadsheet=URL_FOGLIO, worksheet="spesa", data=df)
    st.cache_data.clear()

# --- STILE CSS DARK PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3, p { color: #FFFFFF !important; }
    .stButton>button {
        border-radius: 12px;
        background-color: #4e73df;
        color: white;
        transition: 0.3s;
        width: 100%;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1A1C24;
        padding: 10px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE LOGIN (UNICA) ---
PASSWORD_CORRETTA = "gh28"

if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown("<h1 style='text-align: center;'>🔒 G&H Dark Access</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Inserisci Password:", type="password")
        if st.form_submit_button("Entra nell'Hub"):
            if pwd == PASSWORD_CORRETTA:
                st.session_state.autenticato = True
                st.rerun()
            else:
                st.error("❌ Password errata!")
    st.stop()

# --- INTERFACCIA PRINCIPALE ---
st.markdown("<h1 style='text-align: center;'>🏠 G&H Family Hub</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #AAA;'>Ciao Giacomo ed Helen! ❤️ {datetime.now().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "🧹 Task", "💪 Gym", "💬 Note", "📅 Bollette", "✨ Wish", "💰 Risparmi"])

# --- TAB 0: METEO ---
with tabs[0]:
    st.header("🌡️ Meteo & Consigli")
    citta = "Rome" 
    html_code = f"""
    <a class="weatherwidget-io" href="https://forecast7.com/it/41p9012p50/{citta.lower()}/" data-label_1="{citta.upper()}" data-label_2="METEO" data-theme="dark" >{citta.upper()} METEO</a>
    <script>!function(d,s,id){{var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){{js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}}}(document,'script','weatherwidget-io-js');</script>
    """
    components.html(html_code, height=220)

# --- TAB 1: SPESA (COLLEGATA A GOOGLE) ---
with tabs[1]:
    st.header("🛒 Lista Spesa (Cloud)")
    df_spesa = carica_spesa_google()
    
    with st.form("add_spesa_google", clear_on_submit=True):
        nuovo_item = st.text_input("Aggiungi prodotto:")
        if st.form_submit_button("Aggiungi"):
            if nuovo_item:
                nuova_riga = pd.DataFrame({"Elemento": [nuovo_item], "Categoria": ["Altro"]})
                df_spesa = pd.concat([df_spesa, nuova_riga], ignore_index=True)
                salva_spesa_google(df_spesa)
                st.rerun()

    for i, row in df_spesa.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Elemento']}")
        if c2.button("🗑️", key=f"sp_{i}"):
            df_spesa = df_spesa.drop(i)
            salva_spesa_google(df_spesa)
            st.rerun()

# --- TAB 2: TASK ---
with tabs[2]:
    st.header("🧹 Compiti")
    # Nota: per ora i task rimangono in sessione temporanea, se vuoi salvare anche questi su Google dimmelo!
    st.info("Esegui i compiti della settimana")

# --- TAB 3: GYM ---
with tabs[3]:
    st.header("💪 Palestra")
    st.write("1. **Sopra**: Panca, Lat, Spalle")
    st.write("2. **Gambe**: Squat, Pressa, Core")

# --- TAB 4: NOTE ---
with tabs[4]:
    st.header("💬 Bacheca Note")
    st.write("Qui puoi lasciare messaggi veloci per Helen.")

# --- TAB 5: BOLLETTE ---
with tabs[5]:
    st.header("📅 Scadenze Bollette")
    st.info("Tieni d'occhio i pagamenti.")

# (Le altre sezioni rimangono come struttura per ora)

