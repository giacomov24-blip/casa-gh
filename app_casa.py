import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# URL del tuo foglio Google
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"

# Connessione (Streamlit userà i Secrets che hai appena salvato)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONI DATABASE ---
def carica_dati(tab, colonna_base):
    try:
        df = conn.read(spreadsheet=URL_FOGLIO, worksheet=tab)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=[colonna_base])

def salva_dati(tab, df):
    try:
        conn.update(spreadsheet=URL_FOGLIO, worksheet=tab, data=df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Errore di connessione: {e}")
        return False

# --- GESTIONE LOGIN ---
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown("<h1 style='text-align: center;'>🔒 G&H Dark Access</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Inserisci Password:", type="password")
        if st.form_submit_button("Entra"):
            if pwd == "gh28":
                st.session_state.autenticato = True
                st.rerun()
            else:
                st.error("❌ Password errata!")
    st.stop()

# --- INTERFACCIA PRINCIPALE ---
st.title("🏠 G&H Family Hub")
tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "📅 Bollette", "✨ Wishlist"])

# 1. TAB METEO
with tabs[0]:
    st.header("🌡️ Meteo Roma")
    components.html("""
        <a class="weatherwidget-io" href="https://weatherwidget.io/it/41p9012p50/rome/" data-label_1="ROMA" data-theme="dark" >ROMA</a>
        <script>
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
        </script>
    """, height=220)

# 2. TAB SPESA
with tabs[1]:
    st.header("🛒 Lista Spesa")
    df_spesa = carica_dati("spesa", "Elemento")
    with st.form("add_spesa", clear_on_submit=True):
        item = st.text_input("Cosa manca in frigo?")
        if st.form_submit_button("Aggiungi"):
            if item:
                nuovo = pd.DataFrame({"Elemento": [item]})
                df_spesa = pd.concat([df_spesa, nuovo], ignore_index=True)
                if salva_dati("spesa", df_spesa):
                    st.success(f"✅ {item} aggiunto!")
                    st.rerun()
    
    st.write("---")
    for i, row in df_spesa.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Elemento']}")
        if c2.button("🗑️", key=f"del_sp_{i}"):
            df_spesa = df_spesa.drop(i)
            salva_dati("spesa", df_spesa)
            st.rerun()

# 3. TAB BOLLETTE
with tabs[2]:
    st.header("📅 Bollette e Scadenze")
    df_boll = carica_dati("bollette", "Dettaglio")
    with st.form("add_boll", clear_on_submit=True):
        boll_info = st.text_input("Esempio: Luce Gennaio - 45€")
        if st.form_submit_button("Salva Bolletta"):
            if boll_info:
                nuovo = pd.DataFrame({"Dettaglio": [boll_info]})
                df_boll = pd.concat([df_boll, nuovo], ignore_index=True)
                salva_dati("bollette", df_boll)
                st.rerun()
    
    for i, row in df_boll.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔔 {row['Dettaglio']}")
        if c2.button("🗑️", key=f"del_bl_{i}"):
            df_boll = df_boll.drop(i)
            salva_dati("bollette", df_boll)
            st.rerun()

# 4. TAB WISHLIST
with tabs[3]:
    st.header("✨ Wishlist")
    df_wish = carica_dati("wishlist", "Regalo")
    with st.form("add_wish", clear_on_submit=True):
        wish_item = st.text_input("Cosa vorresti?")
        if st.form_submit_button("Aggiungi Desiderio"):
            if wish_item:
                nuovo = pd.DataFrame({"Regalo": [wish_item]})
                df_wish = pd.concat([df_wish, nuovo], ignore_index=True)
                salva_dati("wishlist", df_wish)
                st.rerun()
    
    for i, row in df_wish.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🎁 {row['Regalo']}")
        if c2.button("🗑️", key=f"del_ws_{i}"):
            df_wish = df_wish.drop(i)
            salva_dati("wishlist", df_wish)
            st.rerun()

# --- STILE ESTETICO ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e1e26;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)
