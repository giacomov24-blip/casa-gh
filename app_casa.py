import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurazione della pagina
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# Funzioni per salvare e caricare i dati
def carica_dati(file_nome):
    if os.path.exists(file_nome):
        return pd.read_csv(file_nome).to_dict('records')
    return []

def salva_dati(file_nome, dati):
    if dati:
        pd.DataFrame(dati).to_csv(file_nome, index=False)
    else:
        if os.path.exists(file_nome):
            os.remove(file_nome)

# Caricamento iniziale dei dati
if 'spesa' not in st.session_state:
    st.session_state.spesa = carica_dati('spesa.csv')
if 'tasks' not in st.session_state:
    st.session_state.tasks = carica_dati('tasks.csv')
if 'commenti' not in st.session_state:
    st.session_state.commenti = carica_dati('commenti.csv')

st.title("🏠 G&H Family Hub")
st.write(f"Ciao Giacomo ed Helen! Oggi è il {datetime.now().strftime('%d/%m/%Y')}")

# Creazione dei Tab (Ho aggiunto "Commenti e varie")
tabs = st.tabs(["🛒 Spesa", "🧹 Compiti", "💪 Allenamento GV", "💬 Commenti e varie"])

# --- TAB 1: LISTA DELLA SPESA ---
with tabs[0]:
    st.header("Lista della Spesa")
    nuovo_item = st.text_input("Cosa manca?", key="input_spesa")
    if st.button("Aggiungi alla spesa"):
        if nuovo_item:
            st.session_state.spesa.append({"item": nuovo_item})
            salva_dati('spesa.csv', st.session_state.spesa)
            st.rerun()

    for i, obj in enumerate(st.session_state.spesa):
        col1, col2 = st.columns([4, 1])
        col1.write(f"• {obj['item']}")
        if col2.button("Preso", key=f"spesa_{i}"):
            st.session_state.spesa.pop(i)
            salva_dati('spesa.csv', st.session_state.spesa)
            st.rerun()

# --- TAB 2: COMPITI DI CASA ---
with tabs[1]:
    st.header("Compiti e Incombenze")
    with st.form("task_form"):
        task_desc = st.text_input("Attività")
        chi = st.selectbox("Per chi?", ["Giacomo", "Helen", "Entrambi"])
        if st.form_submit_button("Aggiungi Compito"):
            if task_desc:
                st.session_state.tasks.append({"task": task_desc, "chi": chi})
                salva_dati('tasks.csv', st.session_state.tasks)
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{t['chi']}**: {t['task']}")
        if col2.button("Fatto", key=f"task_{i}"):
            st.session_state.tasks.pop(i)
            salva_dati('tasks.csv', st.session_state.tasks)
            st.rerun()

# --- TAB 3: ALLENAMENTO GV ---
with tabs[2]:
    st.header("Programma Ipertrofia GV")
    giorno = st.selectbox("Seleziona Giorno:", ["Giorno 1: Sopra", "Giorno 2: Gambe/Core"])
    if "Giorno 1" in giorno:
        st.info("Focus: Spinta, Trazione Verticale, Braccia")
        st.markdown("- **Panca Manubri**: 3x8-12\n- **Lat Machine**: 3x10-15\n- **Shoulder Press**: 3x10-15\n- **Cardio finale**: 30-40 min")
    else:
        st.info("Focus: Gambe, Trazione Orizzontale, Core")
        st.markdown("- **Goblet Squat**: 3x10-15\n- **Leg Press**: 3x10-15\n- **Rematore Cavo Basso**: 3x10-15\n- **Plank + Bird Dog**: 3 serie")

# --- TAB 4: COMMENTI E VARIE ---
with tabs[3]:
    st.header("💬 Bacheca Messaggi e Note")
    
    # Input per nuovo commento
    with st.container():
        autore = st.radio("Chi scrive?", ["Giacomo", "Helen"], horizontal=True)
        testo_commento = st.text_area("Scrivi qui la tua nota o commento...")
        
        if st.button("Pubblica Nota"):
            if testo_commento:
                nuovo_commento = {
                    "data": datetime.now().strftime("%d/%m %H:%M"),
                    "autore": autore,
                    "testo": testo_commento
                }
                st.session_state.commenti.insert(0, nuovo_commento) # Mette l'ultimo in alto
                salva_dati('commenti.csv', st.session_state.commenti)
                st.rerun()

    st.divider()

    # Visualizzazione dei commenti
    for i, c in enumerate(st.session_state.commenti):
        with st.chat_message("user" if c['autore'] == "Giacomo" else "assistant"):
            st.write(f"Ciao Giacomo ed Helen! Oggi è il {datetime.now().strftime('%d/%m/%Y')}")
            st.write(c['testo'])
            if st.button("Elimina", key=f"comm_{i}"):
                st.session_state.commenti.pop(i)
                salva_dati('commenti.csv', st.session_state.commenti)
                st.rerun()