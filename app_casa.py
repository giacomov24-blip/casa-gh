import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# URL del tuo foglio Google
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"

# Connessione protetta tramite Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Errore configurazione Secrets: {e}")

# --- 2. FUNZIONI DATABASE ---
def carica_dati(tab, colonna_fallback):
    try:
        df = conn.read(spreadsheet=URL_FOGLIO, worksheet=tab)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=[colonna_fallback])

def salva_dati(tab, df):
    try:
        conn.update(spreadsheet=URL_FOGLIO, worksheet=tab, data=df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Errore scrittura sul foglio: {e}")
        return False

# --- 3. GESTIONE LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center;'>🔒 G&H Dark Access</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Password:", type="password")
        if st.form_submit_button("Entra"):
            if pwd == "gh28":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ Password errata!")
    st.stop()

# --- 4. INTERFACCIA HUB ---
st.title("🏠 G&H Family Hub")
tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "📅 Bollette", "✨ Wishlist"])

# TAB METEO
with tabs[0]:
    st.header("Meteo Roma")
    components.html("""
        <a class="weatherwidget-io" href="https://weatherwidget.io/it/41p9012p50/rome/" data-label_1="ROMA" data-theme="dark" >ROMA</a>
        <script>
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
        </script>
    """, height=220)

# TAB SPESA
with tabs[1]:
    st.header("🛒 Lista Spesa")
    df_spesa = carica_dati("spesa", "Elemento")
    with st.form("add_spesa", clear_on_submit=True):
        nuovo_item = st.text_input("Aggiungi alla spesa:")
        if st.form_submit_button("Aggiungi"):
            if nuovo_item:
                df_spesa = pd.concat([df_spesa, pd.DataFrame({"Elemento": [nuovo_item]})], ignore_index=True)
                if salva_dati("spesa", df_spesa):
                    st.rerun()
    
    for i, row in df_spesa.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Elemento']}")
        if c2.button("🗑️", key=f"sp_{i}"):
            df_spesa = df_spesa.drop(i)
            salva_dati("spesa", df_spesa)
            st.rerun()

# TAB BOLLETTE
with tabs[2]:
    st.header("📅 Bollette")
    df_boll = carica_dati("bollette", "Dettaglio")
    with st.form("add_boll", clear_on_submit=True):
        nuova_boll = st.text_input("Esempio: Gas Gennaio - 60€")
        if st.form_submit_button("Salva"):
            if nuova_boll:
                df_boll = pd.concat([df_boll, pd.DataFrame({"Dettaglio": [nuova_boll]})], ignore_index=True)
                if salva_dati("bollette", df_boll):
                    st.rerun()
    
    for i, row in df_boll.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔔 {row['Dettaglio']}")
        if c2.button("🗑️", key=f"bl_{i}"):
            df_boll = df_boll.drop(i)
            salva_dati("bollette", df_boll)
            st.rerun()

# TAB WISHLIST
with tabs[3]:
    st.header("✨ Wishlist")
    df_wish = carica_dati("wishlist", "Regalo")
    with st.form("add_wish", clear_on_submit=True):
        nuovo_desiderio = st.text_input("Cosa vorresti?")
        if st.form_submit_button("Salva desiderio"):
            if nuovo_desiderio:
                df_wish = pd.concat([df_wish, pd.DataFrame({"Regalo": [nuovo_desiderio]})], ignore_index=True)
                if salva_dati("wishlist", df_wish):
                    st.rerun()
    
    for i, row in df_wish.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🎁 {row['Regalo']}")
        if c2.button("🗑️", key=f"ws_{i}"):
            df_wish = df_wish.drop(i)
            salva_dati("wishlist", df_wish)
            st.rerun()

# --- STILE ---
st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
