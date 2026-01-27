import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date
import streamlit.components.v1 as components

# CONFIGURAZIONE
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1W-bkKWbTANZ0O1033m81A8VeM2nurAE9FM3aqL4Qvqk/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONI DATABASE ---
def carica_dati(tab_name, colonne):
    try:
        return conn.read(spreadsheet=URL_FOGLIO, worksheet=tab_name)
    except:
        return pd.DataFrame(columns=colonne)

def salva_dati(tab_name, df):
    try:
        conn.update(spreadsheet=URL_FOGLIO, worksheet=tab_name, data=df)
        st.cache_data.clear()
    except:
        st.error(f"Errore: Verifica che il tab '{tab_name}' esista sul Foglio Google!")

# --- LOGIN ---
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
            else: st.error("❌ Password errata")
    st.stop()

# --- INTERFACCIA ---
st.title("🏠 G&H Family Hub")
tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "📅 Bollette", "✨ Wishlist", "💪 Gym"])

# 1. METEO
with tabs[0]:
    components.html('<a class="weatherwidget-io" href="https://forecast7.com/it/41p9012p50/rome/" data-label_1="ROMA" data-theme="dark" >ROMA</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://weatherwidget.io/js/widget.min.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","weatherwidget-io-js");</script>', height=220)

# 2. SPESA
with tabs[1]:
    st.header("🛒 Spesa Cloud")
    df_spesa = carica_dati("spesa", ["Elemento", "Categoria"])
    with st.form("add_spesa", clear_on_submit=True):
        item = st.text_input("Cosa manca?")
        if st.form_submit_button("Aggiungi"):
            if item:
                nuovo = pd.DataFrame({"Elemento": [item], "Categoria": ["Altro"]})
                df_spesa = pd.concat([df_spesa, nuovo], ignore_index=True)
                salva_dati("spesa", df_spesa)
                st.rerun()
    for i, row in df_spesa.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Elemento']}")
        if c2.button("🗑️", key=f"sp_{i}"):
            df_spesa = df_spesa.drop(i)
            salva_dati("spesa", df_spesa); st.rerun()

# 3. BOLLETTE
with tabs[2]:
    st.header("📅 Bollette")
    df_boll = carica_dati("bollette", ["Nome", "Scadenza", "Euro"])
    with st.expander("➕ Aggiungi Bolletta"):
        with st.form("add_boll", clear_on_submit=True):
            n_b = st.text_input("Nome (es. Luce):")
            d_b = st.date_input("Scadenza:")
            e_b = st.number_input("Euro:", min_value=0.0)
            if st.form_submit_button("Salva"):
                nuovo = pd.DataFrame({"Nome": [n_b], "Scadenza": [str(d_b)], "Euro": [e_b]})
                df_boll = pd.concat([df_boll, nuovo], ignore_index=True)
                salva_dati("bollette", df_boll); st.rerun()
    for i, row in df_boll.iterrows():
        st.write(f"🔔 **{row['Nome']}**: {row['Euro']}€ (Scade: {row['Scadenza']})")
        if st.button("Pagata ✅", key=f"bl_{i}"):
            df_boll = df_boll.drop(i)
            salva_dati("bollette", df_boll); st.rerun()

# 4. WISHLIST
with tabs[3]:
    st.header("✨ Wishlist")
    df_wish = carica_dati("wishlist", ["Oggetto", "Link"])
    with st.form("add_wish", clear_on_submit=True):
        og_w = st.text_input("Cosa vorresti?")
        li_w = st.text_input("Link (opzionale):")
        if st.form_submit_button("Aggiungi"):
            if og_w:
                nuovo = pd.DataFrame({"Oggetto": [og_w], "Link": [li_w]})
                df_wish = pd.concat([df_wish, nuovo], ignore_index=True)
                salva_dati("wishlist", df_wish); st.rerun()
    for i, row in df_wish.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"🎁 **{row['Oggetto']}**")
        if row['Link']: st.caption(row['Link'])
        if c2.button("🗑️", key=f"ws_{i}"):
            df_wish = df_wish.drop(i)
            salva_dati("wishlist", df_wish); st.rerun()

# 5. GYM
with tabs[4]:
    st.header("💪 Palestra")
    st.write("🏋️ Giacomo: Panca/Squat")
    st.write("🧘 Helen: Core/Cardio")

st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
