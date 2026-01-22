import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="Hub Casa G&H", layout="centered")

# --- CONNESSIONE GOOGLE SHEETS ---
# Sostituisci questo URL con il link "Condividi" del tuo foglio Google (impostato su "Chiunque abbia il link può modificare")
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRUUlWdGC-V38_PbOTcfyom3wT4Ez9oeuv3hh8DeXnOvBa_mHbiTNPRaKeqfYeIPdOq2vJytWubXp9Q/pubhtml"

conn = st.connection("gsheets", type=GSheetsConnection)

def carica_dati():
    return conn.read(spreadsheet=URL_FOGLIO, worksheet="spesa")

def salva_dati(df):
    conn.update(spreadsheet=URL_FOGLIO, worksheet="spesa", data=df)
    st.cache_data.clear()

# --- LOGIN ---
if 'autenticato' not in st.session_state:
    st.session_state['autenticato'] = False

if not st.session_state['autenticato']:
    st.title("🔐 Accesso Hub Casa")
    password = st.text_input("Inserisci Password", type="password")
    if st.button("Entra"):
        if password == "gh2026":
            st.session_state['autenticato'] = True
            st.rerun()
        else:
            st.error("Password errata")
else:
    # --- INTERFACCIA APP ---
    st.title("🏠 Hub Casa Giacomo & Helen")
    
    tab1, tab2 = st.tabs(["🛒 Spesa", "📝 Note"])

    with tab1:
        st.header("Lista della Spesa")
        
        # Caricamento dati da Google Sheets
        try:
            df_spesa = carica_dati()
        except:
            df_spesa = pd.DataFrame(columns=["Elemento", "Categoria", "Data"])

        # Form per aggiungere elementi
        with st.form("nuovo_elemento"):
            nuovo_item = st.text_input("Cosa manca?")
            categoria = st.selectbox("Categoria", ["Alimentari", "Casa", "Animali", "Altro"])
            if st.form_submit_button("Aggiungi alla lista"):
                nuova_riga = pd.DataFrame({
                    "Elemento": [nuovo_item],
                    "Categoria": [categoria],
                    "Data": [datetime.now().strftime("%d/%m/%Y")]
                })
                df_spesa = pd.concat([df_spesa, nuova_riga], ignore_index=True)
                salva_dati(df_spesa)
                st.success(f"{nuovo_item} aggiunto!")
                st.rerun()

        # Visualizzazione lista
        if not df_spesa.empty:
            st.write("---")
            for i, row in df_spesa.iterrows():
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{row['Elemento']}** ({row['Categoria']})")
                if col2.button("🗑️", key=f"del_{i}"):
                    df_spesa = df_spesa.drop(i)
                    salva_dati(df_spesa)
                    st.rerun()
        else:
            st.info("La lista è vuota!")

    with tab2:
        st.header("Bacheca Note")
        st.write("Funzione note in arrivo...")

# --- STILE DARK ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    button { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. CONFIGURAZIONE E STILE DARK ---
st.set_page_config(page_title="G&H Family Hub", page_icon="🏠", layout="centered")

# CSS per il Tema Scuro Professionale
st.markdown("""
    <style>
    /* Sfondo principale scuro */
    .stApp { 
        background-color: #0E1117; 
        color: #FFFFFF;
    }
    /* Header e testi secondari */
    h1, h2, h3, p { color: #FFFFFF !important; }
    
    /* Pulsanti moderni */
    .stButton>button {
        border-radius: 12px;
        height: 3em;
        width: 100%;
        background-color: #4e73df;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #224abe; 
        border: 1px solid #4e73df;
    }
    
    /* Tab con stile scuro */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1A1C24;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom-color: #4e73df !important;
    }

    /* Input e Form scuri */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #262730;
        color: white;
        border-color: #4e73df;
    }
    
    /* Chat e Messaggi */
    .stChatMessage {
        background-color: #1A1C24 !important;
        border-radius: 15px !important;
        border: 1px solid #262730 !important;
        color: white !important;
    }

    /* Box e Expander */
    div[data-testid="stExpander"] {
        background-color: #1A1C24;
        border-radius: 15px;
        border: 1px solid #262730;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONI DI SERVIZIO ---
def carica_dati(file_nome):
    if os.path.exists(file_nome):
        try: return pd.read_csv(file_nome).to_dict('records')
        except: return []
    return []

def salva_dati(file_nome, dati):
    pd.DataFrame(dati).to_csv(file_nome, index=False)

# --- 3. GESTIONE LOGIN ---
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

# --- 4. INIZIALIZZAZIONE DATI ---
tabelle = ['spesa', 'tasks', 'commenti', 'bollette', 'wishlist', 'risparmi']
for t in tabelle:
    if t not in st.session_state:
        st.session_state[t] = carica_dati(f'{t}.csv')

# --- 5. INTERFACCIA PRINCIPALE ---
st.markdown("<h1 style='text-align: center;'>🏠 G&H Family Hub</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #AAA;'>Ciao Giacomo ed Helen! ❤️ {datetime.now().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

tabs = st.tabs(["🌡️ Meteo", "🛒 Spesa", "🧹 Task", "💪 Gym", "💬 Note", "📅 Bollette", "✨ Wish", "💰 Risparmi"])

# --- TAB METEO ---
with tabs[0]:
    st.header("🌡️ Meteo & Consigli")
    citta = "Rome" 
    # Widget versione scura
    html_code = f"""
    <a class="weatherwidget-io" href="https://forecast7.com/it/41p9012p50/{citta.lower()}/" data-label_1="{citta.upper()}" data-label_2="METEO" data-theme="dark" >{citta.upper()} METEO</a>
    <script>!function(d,s,id){{var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){{js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}}}(document,'script','weatherwidget-io-js');</script>
    """
    components.html(html_code, height=220)
    
    t_esterna = st.slider("Temperatura (°C):", -5, 40, 18)
    if t_esterna <= 12: st.info("🧤 Fa freddo! Giacomo, copri bene Helen.")
    elif 13 <= t_esterna <= 22: st.success("⛅ Clima perfetto per una passeggiata.")
    else: st.warning("☀️ Fa caldo! Abbigliamento leggero.")

# --- TAB SPESA ---
with tabs[1]:
    st.header("🛒 Lista Spesa")
    with st.form("add_spesa", clear_on_submit=True):
        item = st.text_input("Aggiungi prodotto:")
        if st.form_submit_button("Aggiungi"):
            if item:
                st.session_state.spesa.append({"item": item})
                salva_dati('spesa.csv', st.session_state.spesa); st.rerun()
    for i, x in enumerate(st.session_state.spesa):
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {x['item']}")
        if c2.button("🗑️", key=f"s_{i}"):
            st.session_state.spesa.pop(i); salva_dati('spesa.csv', st.session_state.spesa); st.rerun()

# --- TAB TASK ---
with tabs[2]:
    st.header("🧹 Compiti")
    with st.form("add_task"):
        tk = st.text_input("Cosa fare?")
        per = st.selectbox("Per chi?", ["Giacomo", "Helen", "Entrambi"])
        if st.form_submit_button("Assegna"):
            st.session_state.tasks.append({"task": tk, "chi": per})
            salva_dati('tasks.csv', st.session_state.tasks); st.rerun()
    for i, t in enumerate(st.session_state.tasks):
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{t['chi']}**: {t['task']}")
        if c2.button("✅", key=f"t_{i}"):
            st.session_state.tasks.pop(i); salva_dati('tasks.csv', st.session_state.tasks); st.rerun()

# --- TAB GYM ---
with tabs[3]:
    st.header("💪 Palestra")
    st.info("Focus Ipertrofia 🏋️‍♂️")
    st.write("1. **Sopra**: Panca, Lat, Spalle")
    st.write("2. **Gambe**: Squat, Pressa, Core")

# --- TAB NOTE ---
with tabs[4]:
    st.header("💬 Bacheca Note")
    aut = st.radio("Firma:", ["Giacomo", "Helen"], horizontal=True)
    txt = st.text_area("Messaggio:")
    if st.button("Invia"):
        if txt:
            n = {"data": datetime.now().strftime("%d/%m %H:%M"), "autore": aut, "testo": txt}
            st.session_state.commenti.insert(0, n); salva_dati('commenti.csv', st.session_state.commenti); st.rerun()
    for i, c in enumerate(st.session_state.commenti):
        with st.chat_message("user" if c['autore'] == "Giacomo" else "assistant"):
            st.write(f"**{c['autore']}** - {c['data']}\n\n{c['testo']}")

# --- TAB BOLLETTE ---
with tabs[5]:
    st.header("📅 Bollette")
    with st.expander("➕ Aggiungi Bolletta"):
        with st.form("f_b"):
            nb = st.text_input("Nome:"); db = st.date_input("Data:"); eb = st.number_input("Euro:", min_value=0.0)
            if st.form_submit_button("Salva"):
                st.session_state.bollette.append({"nome": nb, "data": db.strftime("%Y-%m-%d"), "euro": eb})
                salva_dati('bollette.csv', st.session_state.bollette); st.rerun()
    for i, b in enumerate(st.session_state.bollette):
        sc = datetime.strptime(b['data'], "%Y-%m-%d").date()
        gg = (sc - date.today()).days
        if gg < 0: st.error(f"🔴 {b['nome']} ({b['euro']}€) - SCADUTA")
        elif gg <= 3: st.warning(f"🟠 {b['nome']} ({b['euro']}€) - Scade tra {gg}gg")
        else: st.info(f"🔵 {b['nome']} ({b['euro']}€) - {sc.strftime('%d/%m')}")
        if st.button("Pagata", key=f"pb_{i}"):
            st.session_state.bollette.pop(i); salva_dati('bollette.csv', st.session_state.bollette); st.balloons(); st.rerun()

# --- TAB WISH ---
with tabs[6]:
    st.header("✨ Wishlist")
    with st.expander("➕ Aggiungi"):
        with st.form("f_w"):
            des = st.text_input("Oggetto?"); lnk = st.text_input("Link:"); prio = st.select_slider("Urgenza:", ["Bassa", "Media", "Alta"])
            if st.form_submit_button("Salva"):
                st.session_state.wishlist.append({"item": des, "link": lnk, "prior": prio})
                salva_dati('wishlist.csv', st.session_state.wishlist); st.rerun()
    for i, w in enumerate(st.session_state.wishlist):
        st.write(f"**{w['item']}** ({w['prior']})")
        if w['link']: st.link_button("Vedi Link", w['link'])
        if st.button("Comprato 🎁", key=f"w_{i}"):
            st.session_state.wishlist.pop(i); salva_dati('wishlist.csv', st.session_state.wishlist); st.rerun()

# --- TAB RISPARMI ---
with tabs[7]:
    st.header("💰 Risparmi")
    with st.expander("➕ Nuovo Obiettivo"):
        with st.form("f_r"):
            obj = st.text_input("Obiettivo:"); tar = st.number_input("Target (€):", min_value=1.0)
            if st.form_submit_button("Crea"):
                st.session_state.risparmi.append({"oggetto": obj, "target": tar, "risparmiato": 0.0})
                salva_dati('risparmi.csv', st.session_state.risparmi); st.rerun()
    for i, r in enumerate(st.session_state.risparmi):
        st.write(f"**{r['oggetto']}**")
        perc = min(r['risparmiato'] / r['target'], 1.0)
        st.progress(perc)
        st.write(f"{r['risparmiato']}€ su {r['target']}€")
        add_r = st.number_input("Aggiungi cifra (€):", min_value=0.0, key=f"ar_{i}")
        if st.button("Versa", key=f"br_{i}"):
            st.session_state.risparmi[i]['risparmiato'] += add_r
            salva_dati('risparmi.csv', st.session_state.risparmi); st.rerun()

