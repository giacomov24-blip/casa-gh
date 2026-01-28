import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# URL del tuo foglio Google (ID: 1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk)
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"

# Connessione al database
conn = st.connection("gsheets", type=GSheetsConnection)

# Funzioni per i dati
def carica_dati(tab_name, colonna_base):
    try:
        df = conn.read(spreadsheet=URL_FOGLIO, worksheet=tab_name)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=[colonna_base])

def salva_dati(tab_name, df):
    try:
        conn.update(spreadsheet=URL_FOGLIO, worksheet=tab_name, data=df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Errore: {e}")
        return False

# --- 2. GESTIONE LOGIN ---
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

# --- 3. INTERFACCIA PRINCIPALE ---
st.title("🏠 G&H Family Hub")
tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "📅 Bollette", "✨ Wishlist", "💪 Gym"])

# TAB 0: METEO (ROMA)
with tabs[0]:
    st.header("🌡️ Meteo Roma")
    components.html("""
        <a class="weatherwidget-io" href="https://weatherwidget.io/it/41p9012p50/rome/" data-label_1="ROMA" data-theme="dark" >ROMA</a>
        <script>
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
        </script>
    """, height=220)

# TAB 1: SPESA
with tabs[1]:
    st.header("🛒 Lista Spesa Cloud")
    df_spesa = carica_dati("spesa", "Elemento")
    with st.form("add_spesa", clear_on_submit=True):
        item = st.text_input("Cosa manca?")
        if st.form_submit_button("Aggiungi"):
            if item:
                nuovo = pd.DataFrame({"Elemento": [item]})
                df_spesa = pd.concat([df_spesa, nuovo], ignore_index=True)
                if salva_dati("spesa", df_spesa):
                    st.success("✅ Aggiunto!")
                    st.rerun()
    for i, row in df_spesa.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Elemento']}")
        if c2.button("🗑️", key=f"del_sp_{i}"):
            df_spesa = df_spesa.drop(i)
            salva_dati("spesa", df_spesa)
            st.rerun()

# TAB 2: BOLLETTE
with tabs[2]:
    st.header("📅 Bollette")
    df_boll = carica_dati("bollette", "Dettaglio")
    with st.form("add_boll", clear_on_submit=True):
        boll_item = st.text_input("Esempio: Luce - 50€ - Scad. 10/02")
        if st.form_submit_button("Salva"):
            if boll_item:
                nuovo = pd.DataFrame({"Dettaglio": [boll_item]})
                df_boll = pd.concat([df_boll, nuovo], ignore_index=True)
                salva_dati("bollette", df_boll)
                st.rerun()
    for i, row in df_boll.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔔 {row['Dettaglio']}")
        if c2.button("🗑️", key=f"del_boll_{i}"):
            df_boll = df_boll.drop(i)
            salva_dati("bollette", df_boll)
            st.rerun()

# TAB 3: WISHLIST
with tabs[3]:
    st.header("✨ Wishlist")
    df_wish = carica_dati("wishlist", "Regalo")
    with st.form("add_wish", clear_on_submit=True):
        wish_item = st.text_input("Cosa vorresti?")
        if st.form_submit_button("Salva"):
            if wish_item:
                nuovo = pd.DataFrame({"Regalo": [wish_item]})
                df_wish = pd.concat([df_wish, nuovo], ignore_index=True)
                salva_dati("wishlist", df_wish)
                st.rerun()
    for i, row in df_wish.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🎁 {row['Regalo']}")
        if c2.button("🗑️", key=f"del_wish_{i}"):
            df_wish = df_wish.drop(i)
            salva_dati("wishlist", df_wish)
            st.rerun()

# TAB 4: GYM
with tabs[4]:
    st.header("💪 Gym Schedule")
    st.write("🏋️ **Giacomo**: Lun-Mer-Ven (Forza)")
    st.write("🧘 **Helen**: Mar-Gio-Sab (Core/Yoga)")

# STILE CSS
st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
