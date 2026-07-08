import streamlit as st
import docx
from io import BytesIO

# Configurazione pagina
st.set_page_config(page_title="Motore LLM - Pratiche Edilizie", layout="wide")
st.title("Generatore Documenti Pratiche Edilizie")

# Inizializzazione Session State per campi dinamici
if 'num_intestatari' not in st.session_state:
    st.session_state.num_intestatari = 1
if 'num_professionisti_extra' not in st.session_state:
    st.session_state.num_professionisti_extra = 0

# ==========================================
# SEZIONE 1: RACCOGLITORE DI DATI
# ==========================================
st.header("1. Anagrafiche e Raccoglitore Dati")

# --- INTESTATARI ---
st.subheader("Intestatari")
intestatari_data = []
for i in range(st.session_state.num_intestatari):
    st.markdown(f"**Soggetto {i+1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nome = st.text_input(f"Nome", key=f"nome_{i}")
        cognome = st.text_input(f"Cognome", key=f"cogn__{i}")
        cf = st.text_input(f"Codice Fiscale", key=f"cf_{i}")
    with col2:
        data_nascita = st.date_input(f"Data di Nascita", key=f"data_{i}")
        luogo_nascita = st.text_input(f"Luogo di Nascita", key=f"luogo_{i}")
        titolo = st.selectbox(f"Diritto", ["Proprietario", "Comproprietario", "Usufruttuario", "Rappresentante Legale"], key=f"tit_{i}")
    with col3:
        via = st.text_input(f"Indirizzo di residenza (Via)", key=f"via_{i}")
        civico = st.text_input(f"Civico", key=f"civ_{i}")
        cap = st.text_input(f"CAP", key=f"cap_{i}")
    with col4:
        paese = st.text_input(f"Paese", key=f"paese_{i}")
        prov = st.text_input(f"Provincia", key=f"prov_{i}")
        mail = st.text_input(f"Mail", key=f"mail_{i}")
        tel = st.text_input(f"Telefono", key=f"tel_{i}")
    
    intestatari_data.append({
        "Nome": nome, "Cognome": cognome, "CF": cf, "Data Nascita": data_nascita, "Luogo Nascita": luogo_nascita,
        "Residenza": f"{via} {civico}, {cap} {paese} ({prov})", "Mail": mail, "Tel": tel, "Diritto": titolo
    })
    st.divider()

if st.button("➕ Aggiungi un altro intestatario"):
    st.session_state.num_intestatari += 1
    st.rerun()

# --- PROFESSIONISTI ---
st.subheader("Professionisti")
st.markdown("**Progettista (Default)**")
col_p1, col_p2 = st.columns(2)
with col_p1:
    prof_nome = st.text_input("Nome e Cognome", value="Gianfranco Andriolo")
    prof_cf = st.text_input("Codice Fiscale", value="NDRGFR83S17F964E")
    prof_nascita = st.text_input("Nato il / a", value="17/11/1983 a Noventa Vicentina")
    prof_tel = st.text_input("Telefono", value="377 9662445")
with col_p2:
    prof_pec = st.text_input("PEC", value="andriolo.18135@oamilano.it")
    prof_mail = st.text_input("Mail", value="studioandriolo@gmail.com")
    prof_albo = st.text_input("Iscrizione Albo", value="Ordine Architetti Milano, n. 18135")
    prof_studio = st.text_input("Sede Studio", value="Via Masotto 11, 36025 Noventa Vicentina")

professionisti_data = [{"Qualifica": "Progettista", "Nome": prof_nome, "CF": prof_cf, "Dati": f"Nato: {prof_nascita} | Albo: {prof_albo} | Studio: {prof_studio} | Contatti: {prof_pec}, {prof_mail}, {prof_tel}"}]

# Professionisti Extra
for i in range(st.session_state.num_professionisti_extra):
    st.markdown(f"**Professionista Aggiuntivo {i+1}**")
    c1, c2, c3 = st.columns(3)
    with c1:
        q = st.selectbox("Qualifica", ["Strutturista", "Termotecnico", "DDLL", "Coordinatore Sicurezza", "Collaudatore"], key=f"q_{i}")
    with c2:
        n = st.text_input("Nome e Cognome", key=f"pn_{i}")
    with c3:
        cf_ext = st.text_input("Codice Fiscale", key=f"pcf_{i}")
    professionisti_data.append({"Qualifica": q, "Nome": n, "CF": cf_ext, "Dati": "..."}) # Da espandere se necessario

if st.button("➕ Aggiungi altro professionista"):
    st.session_state.num_professionisti_extra += 1
    st.rerun()

# ==========================================
# SEZIONE 2: ELEMENTI COGNITIVI
# ==========================================
st.header("2. Elementi Cognitivi del Progetto")
tipo_pratica = st.selectbox("Tipo di pratica edilizia", ["CILA", "SCIA art.22", "SCIA art.23", "PdC"])
tipo_intervento = st.text_input("Tipo di intervento (es. Manutenzione Straordinaria, Ristrutturazione)")
rel_sintetica = st.text_area("Relazione Sintetica dell'intervento", height=150)
elaborati = st.file_uploader("Elaborati grafici (Carica PDF)", type=['pdf'], accept_multiple_files=True)


# ==========================================
# SEZIONE 3: GENERAZIONE DOCUMENTI (LLM)
# ==========================================
st.header("3. Documenti da Redigere")
st.caption("Seleziona i documenti necessari. Per ognuno, carica un documento di spunto e il template .docx da compilare.")

docs_necessari = {
    "Relazione tecnico-illustrativa": st.checkbox("Relazione tecnico-illustrativa", value=True), # Sempre spuntato
    "Relazione paesaggistica": st.checkbox("Relazione paesaggistica"),
    "Relazione stato legittimo": st.checkbox("Relazione stato legittimo"),
    "Modello FCA (P/P/P/I/A)": st.checkbox("Modello FCA (P/P/P/I/A)"),
    "Relazione FLDm": st.checkbox("Relazione fattore luce diurna media (FLDm)"),
    "Relazione calcolo volumi": st.checkbox("Relazione sul calcolo dei volumi")
}

file_templates = {}

for doc_name, is_checked in docs_necessari.items():
    if is_checked:
        with st.expander(f"Configura: {doc_name}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                spunto = st.file_uploader(f"Spunto per {doc_name} (PDF/DOCX)", key=f"spunto_{doc_name}")
            with col2:
                template = st.file_uploader(f"Template da compilare per {doc_name} (.docx)", type=['docx'], key=f"tpl_{doc_name}")
            
            file_templates[doc_name] = {"spunto": spunto, "template": template}


# ==========================================
# LOGICA DI ESPORTAZIONE E GENERAZIONE
# ==========================================
st.divider()

# 1. Generatore File Anagrafica (Copia-Incolla)
def genera_docx_anagrafica():
    doc = docx.Document()
    doc.add_heading('Dati per Portale "Impresa in un giorno"', 0)
    
    doc.add_heading('Intestatari', level=1)
    for idx, int_data in enumerate(intestatari_data):
        doc.add_heading(f'Soggetto {idx+1} - {int_data["Diritto"]}', level=2)
        for key, value in int_data.items():
            doc.add_paragraph(f"{key}: {value}", style='List Bullet')
            
    doc.add_heading('Professionisti', level=1)
    for prof in professionisti_data:
        doc.add_heading(f'{prof["Qualifica"]}: {prof["Nome"]}', level=2)
        doc.add_paragraph(f"C.F.: {prof['CF']}", style='List Bullet')
        doc.add_paragraph(f"Dati aggiuntivi: {prof['Dati']}", style='List Bullet')
        
    doc.add_heading('Dati Progetto', level=1)
    doc.add_paragraph(f"Pratica: {tipo_pratica}", style='List Bullet')
    doc.add_paragraph(f"Intervento: {tipo_intervento}", style='List Bullet')
    doc.add_paragraph(f"Sintesi: {rel_sintetica}", style='List Bullet')
    
    # Salva in RAM
    io_stream = BytesIO()
    doc.save(io_stream)
    return io_stream.getvalue()

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.download_button(
        label="📄 Scarica File Dati (Copia-Incolla)",
        data=genera_docx_anagrafica(),
        file_name="dati_portale_impresainungiorno.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary"
    )

with col_btn2:
    if st.button("🤖 Genera Relazioni con LLM"):
        # Qui andrà la logica per chiamare OpenAI/Anthropic
        # 1. Estrarre il testo dal file di "spunto" e dai dati della Sezione 1 e 2
        # 2. Passare il contesto al LLM
        # 3. Identificare i placeholder nel file "template .docx" e sostituirli con l'output generato
        st.info("Logica LLM da implementare. Pronta la struttura di base!")
