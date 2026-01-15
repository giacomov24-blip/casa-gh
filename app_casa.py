import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠")

# --- IMPOSTA LA TUA PASSWORD QUI ---
PASSWORD_CORRETTA = "gh28" # <--- Puoi cambiarla con quella che vuoi!

# Funzioni di servizio
def carica_dati(file_nome):
    if os.path.exists(file_nome):
        try: return pd.read_csv(file_nome).to_dict('records')
        except: return []
    return []

def salva_dati(file_nome, dati):
    pd.DataFrame(dati).to_csv(file_nome, index=False)

# --- GESTIONE LOGIN ---
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.title("🔒 Accesso Riservato")
    pwd_inserita = st.text_input("Inserisci la password di casa:", type="password")
    if st.button("Entra"):
        if pwd_inserita == PASSWORD_CORRETTA:
            st.session_state.autenticato = True
            st.rerun()
        else:
            st.error("Password errata! Riprova.")
    st.stop() # Blocca l'esecuzione qui finché non sono autenticati

# --- SE ARRIVA QUI, L'UTENTE È AUTENTICATO ---
# Inizializzazione dati
if 'spesa' not in st.session_state: st.session_state.spesa = carica_dati('spesa.csv')
if 'tasks' not in st.session_state: st.session_state.tasks = carica_dati('tasks.csv')
if 'commenti' not in st.session_state: st.session_state.commenti = carica_dati('commenti.csv')

st.title("🏠 G&H Family Hub")
st.subheader(f"Ciao Giacomo ed Helen! ❤️")

tabs = st.tabs(["🛒 Spesa", "🧹 Compiti", "💪 Palestra", "💬 Commenti"])
with tabs[0]:
    st.header("Lista della Spesa")
    nuovo = st.text_input("Aggiungi prodotto:", key="in_spesa")
    if st.button("Inserisci"):
        if nuovo:
            st.session_state.spesa.append({"item": nuovo})
            salva_dati('spesa.csv', st.session_state.spesa)
            st.rerun()
    for i, obj in enumerate(st.session_state.spesa):
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {obj['item']}")
        if c2.button("🗑️", key=f"s_{i}"):
            st.session_state.spesa.pop(i)
            salva_dati('spesa.csv', st.session_state.spesa)
            st.rerun()

with tabs[1]:
    st.header("Compiti Casa")
    with st.form("f_tasks"):
        t_desc = st.text_input("Attività")
        # CORREZIONE: Helen nel menu
        chi = st.selectbox("Per chi?", ["Giacomo", "Helen", "Entrambi"])
        if st.form_submit_button("Assegna"):
            st.session_state.tasks.append({"task": t_desc, "chi": chi})
            salva_dati('tasks.csv', st.session_state.tasks)
            st.rerun()
    for i, t in enumerate(st.session_state.tasks):
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{t['chi']}**: {t['task']}")
        if c2.button("✅", key=f"t_{i}"):
            st.session_state.tasks.pop(i)
            salva_dati('tasks.csv', st.session_state.tasks)
            st.rerun()

with tabs[2]:
    st.header("Scheda Palestra")
    st.info("Giacomo: Ricorda l'ipertrofia! 🏋️‍♂️")
    st.write("- Giorno 1: Sopra (Panca/Lat)")
    st.write("- Giorno 2: Gambe (Squat/Press)")

with tabs[3]:
    st.header("Bacheca Note")
    # CORREZIONE: Helen nei bottoni
    autore = st.radio("Firma:", ["Giacomo", "Helen"], horizontal=True)
    msg = st.text_area("Scrivi un messaggio...")
    if st.button("Invia Nota"):
        if msg:
            nota = {"data": datetime.now().strftime("%d/%m %H:%M"), "autore": autore, "testo": msg}
            st.session_state.commenti.insert(0, nota)
            salva_dati('commenti.csv', st.session_state.commenti)
            st.rerun()
    for i, c in enumerate(st.session_state.commenti):
        with st.chat_message("user" if c['autore'] == "Giacomo" else "assistant"):
            st.write(f"**{c['autore']}** - {c['data']}\n\n{c['testo']}")