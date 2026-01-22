import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import streamlit.components.v1 as components

# CONFIGURAZIONE UNICA
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# URL del tuo foglio (Usa quello che hai già messo nell'immagine)
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def carica_spesa_google():
    try:
        return conn.read(spreadsheet=URL_FOGLIO, worksheet="spesa")
    except:
        return pd.DataFrame(columns=["Elemento", "Categoria"])

def salva_spesa_google(df):
    conn.update(spreadsheet=URL_FOGLIO, worksheet="spesa", data=df)
    st.cache_data.clear()

# --- GESTIONE LOGIN (PASSWORD gh28) ---
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown("<h1 style='text-align: center;'>🔒 G&H Dark Access</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Password:", type="password")
        if st.form_submit_button("Entra"):
            if pwd == "gh28":
                st.session_state.autenticato = True
                st.rerun()
            else: st.error("❌ Password errata!")
    st.stop()

# --- INTERFACCIA ---
st.title("🏠 G&H Family Hub")
tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "🧹 Task", "💪 Gym", "💬 Note"])

with tabs[0]:
    st.header("🌡️ Meteo Roma")
    components.html('<a class="weatherwidget-io" href="https://forecast7.com/it/41p9012p50/rome/" data-label_1="ROMA" data-theme="dark" >ROMA</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://weatherwidget.io/js/widget.min.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","weatherwidget-io-js");</script>', height=220)

with tabs[1]:
    st.header("🛒 Lista Spesa Cloud")
    df_spesa = carica_spesa_google()
    with st.form("add"):
        item = st.text_input("Cosa manca?")
        if st.form_submit_button("Aggiungi"):
            if item:
                nuova_riga = pd.DataFrame({"Elemento": [item], "Categoria": ["Altro"]})
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

with tabs[2]: st.header("🧹 Task"); st.info("Sezione Task attiva")
with tabs[3]: st.header("💪 Gym"); st.write("Panca, Squat, Core")
with tabs[4]: st.header("💬 Note"); st.write("Sezione Note attiva")

# STILE DARK
st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
