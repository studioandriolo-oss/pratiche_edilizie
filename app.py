import streamlit as st
import docx
from docxtpl import DocxTemplate
import PyPDF2
import ollama
from io import BytesIO

# Configurazione pagina
st.set_page_config(page_title="Motore LLM - Pratiche Edilizie", layout="wide")
st.title("Generatore Documenti Pratiche Edilizie (Locale con Ollama)")

# ==========================================
# GESTIONE STATO (SESSION STATE)
# ==========================================
if 'intestatari_ids' not in st.session_state:
    st.session_state.intestatari_ids = [0]
if 'professionisti_ids' not in st.session_state:
    st.session_state.professionisti_ids = []
if 'counter' not in st.session_state:
    st.session_state.counter = 1

def add_intestatario(): st.session_state.intestatari_ids.append(st.session_state.counter); st.session_state.counter += 1
def remove_intestatario(id_to_remove): st.session_state.intestatari_ids.remove(id_to_remove)
def add_professionista(): st.session_state.professionisti_ids.append(st.session_state.counter); st.session_state.counter += 1
def remove_professionista(id_to_remove): st.session_state.professionisti_ids.remove(id_to_remove)

# ==========================================
# SEZIONE 1: RACCOGLITORE DI DATI
# ==========================================
st.header("1. Anagrafiche e Raccoglitore Dati")

# --- INTESTATARI ---
st.subheader("Intestatari")
intestatari_data = []

for idx, uid in enumerate(st.session_state.intestatari_ids):
    st.markdown(f"**Intestatario {idx+1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nome = st.text_input("Nome", key=f"int_nome_{uid}")
        cognome = st.text_input("Cognome", key=f"int_cogn_{uid}")
        cf = st.text_input("Codice Fiscale", key=f"int_cf_{uid}")
    with col2:
        data_nascita = st.date_input("Data di Nascita", key=f"int_data_{uid}")
        luogo_nascita = st.text_input("Luogo di Nascita", key=f"int_luogo_{uid}")
        titolo = st.selectbox("Diritto", ["Proprietario", "Comproprietario", "Usufruttuario", "Rappresentante Legale"], key=f"int_tit_{uid}")
    with col3:
        via = st.text_input("Indirizzo di residenza (Via)", key=f"int_via_{uid}")
        civico = st.text_input("Civico", key=f"int_civ_{uid}")
        cap = st.text_input("CAP", key=f"int_cap_{uid}")
    with col4:
        paese = st.text_input("Paese", key=f"int_paese_{uid}")
        prov = st.text_input("Provincia", key=f"int_prov_{uid}")
        mail = st.text_input("Mail", key=f"int_mail_{uid}")
        tel = st.text_input("Telefono", key=f"int_tel_{uid}")
    
    if idx > 0:
        st.button("🗑️ Rimuovi questo intestatario", key=f"del_int_{uid}", on_click=remove_intestatario, args=(uid,))
    
    intestatari_data.append({
        "Nome": nome, "Cognome": cognome, "CF": cf, 
        "Data_Nascita": data_nascita.strftime('%d/%m/%Y') if data_nascita else "", 
        "Luogo_Nascita": luogo_nascita, "Via": via, "Civico": civico, "CAP": cap, 
        "Paese": paese, "Provincia": prov, "Mail": mail, "Tel": tel, "Diritto": titolo
    })
    st.divider()

st.button("➕ Aggiungi un altro intestatario", on_click=add_intestatario)

# --- PROFESSIONISTI ---
st.subheader("Professionisti")

def render_professionista(uid, is_main=False):
    if is_main:
        qualifica = "Progettista"
        st.markdown(f"**Professionista 1 - {qualifica} (Principale)**")
    else:
        qualifica = st.selectbox("Qualifica", ["Strutturista", "Termotecnico", "DDLL", "Coordinatore Sicurezza", "Collaudatore"], key=f"prof_qual_{uid}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        tit_opzioni = ["Architetto", "Ingegnere", "Geometra", "Perito", "Altro"]
        titolo = st.selectbox("Titolo", tit_opzioni, index=0, key=f"prof_tit_{uid}")
        nome = st.text_input("Nome", value="Gianfranco" if is_main else "", key=f"prof_nome_{uid}")
        cognome = st.text_input("Cognome", value="Andriolo" if is_main else "", key=f"prof_cogn_{uid}")
        cf = st.text_input("Codice Fiscale", value="NDRGFR83S17F964E" if is_main else "", key=f"prof_cf_{uid}")
    with col2:
        luogo_nascita = st.text_input("Luogo di Nascita", value="Noventa Vicentina" if is_main else "", key=f"prof_luogo_{uid}")
        data_nascita = st.text_input("Data di Nascita", value="17/11/1983" if is_main else "", key=f"prof_data_{uid}")
        studio = st.text_input("Studio in (Indirizzo)", value="Via Masotto 11, 36025 Noventa Vicentina" if is_main else "", key=f"prof_studio_{uid}")
    with col3:
        pec = st.text_input("PEC", value="andriolo.18135@oamilano.it" if is_main else "", key=f"prof_pec_{uid}")
        mail = st.text_input("Mail", value="studioandriolo@gmail.com" if is_main else "", key=f"prof_mail_{uid}")
        tel = st.text_input("Telefono", value="377 9662445" if is_main else "", key=f"prof_tel_{uid}")
        albo_coll = st.text_input("Iscrizione all'Albo/Collegio", value="Milano" if is_main else "", key=f"prof_albo_{uid}")
        num_albo = st.text_input("N. Iscrizione", value="18135" if is_main else "", key=f"prof_num_{uid}")
        
    if not is_main:
        st.button("🗑️ Rimuovi professionista", key=f"del_prof_{uid}", on_click=remove_professionista, args=(uid,))
    
    st.divider()
    return {
        "Qualifica": qualifica, "Titolo": titolo, "Nome": nome, "Cognome": cognome, "CF": cf,
        "Luogo_Nascita": luogo_nascita, "Data_Nascita": data_nascita, "Studio": studio,
        "PEC": pec, "Mail": mail, "Tel": tel, "Albo": albo_coll, "Num_Albo": num_albo,
        "Dati": f"Nato a {luogo_nascita} il {data_nascita} | Studio: {studio} | PEC: {pec} | Mail: {mail} | Tel: {tel} | Albo: {albo_coll} n. {num_albo}"
    }

professionisti_data = [render_professionista('main', is_main=True)]
for uid in st.session_state.professionisti_ids:
    professionisti_data.append(render_professionista(uid, is_main=False))

st.button("➕ Aggiungi altro professionista", on_click=add_professionista)


# ==========================================
# SEZIONE 2: ELEMENTI COGNITIVI
# ==========================================
st.header("2. Elementi Cognitivi del Progetto")
tipo_pratica = st.selectbox("Tipo di pratica edilizia", ["CILA", "SCIA art.22", "SCIA art.23", "PdC"])
tipo_intervento = st.text_input("Tipo di intervento (es. Manutenzione Straordinaria, Ristrutturazione)")
rel_sintetica = st.text_area("Relazione Sintetica dell'intervento", height=150)
elaborati = st.file_uploader("Elaborati grafici (PDF)", type=['pdf'], accept_multiple_files=True)


# ==========================================
# SEZIONE 3: GENERAZIONE DOCUMENTI (LLM + DOCXTPL)
# ==========================================
st.header("3. Documenti da Redigere")

docs_necessari = {
    "Relazione tecnico-illustrativa": st.checkbox("Relazione tecnico-illustrativa", value=True),
    "Relazione paesaggistica": st.checkbox("Relazione paesaggistica"),
    "Relazione stato legittimo": st.checkbox("Relazione stato legittimo")
}

file_templates = {}

for doc_name, is_checked in docs_necessari.items():
    if is_checked:
        with st.expander(f"Configura: {doc_name}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                spunto = st.file_uploader(f"Spunto per {doc_name} (PDF)", type=['pdf'], key=f"spunto_{doc_name}")
            with col2:
                template = st.file_uploader(f"Template per {doc_name} (.docx)", type=['docx'], key=f"tpl_{doc_name}")
            file_templates[doc_name] = {"spunto": spunto, "template": template}

st.divider()

# --- FUNZIONI MOTORE AI E WORD ---
def estrai_testo_pdf(pdf_file):
    if not pdf_file: return ""
    lettore = PyPDF2.PdfReader(pdf_file)
    testo = ""
    for pagina in lettore.pages:
        testo += pagina.extract_text() + "\n"
    return testo

def genera_testo_ollama(doc_name, spunto_testo):
    prompt = f"""
    Sei un architetto esperto in pratiche edilizie. 
    Devi redigere il testo per il documento: '{doc_name}'.
    Il tipo di pratica è: {tipo_pratica}.
    L'intervento consiste in: {tipo_intervento}.
    Sintesi del progetto: {rel_sintetica}.
    
    Ecco un documento di spunto simile (usalo come riferimento stilistico e normativo, ma adattalo al nuovo progetto):
    {spunto_testo}
    
    Scrivi solo il testo della relazione, in modo professionale e formale, pronto per essere inserito in un documento Word.
    """
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# --- BOTTONI DI GENERAZIONE ---
if st.button("🤖 Genera Relazioni (Ollama + Word)"):
    with st.spinner("Elaborazione in corso... Il motore LLM locale sta scrivendo le relazioni (potrebbe richiedere qualche minuto)."):
        
        # 1. Costruiamo il dizionario base per i tag di docxtpl
        # Usiamo i dati del primo intestatario e del progettista come variabili principali
        int_1 = intestatari_data[0] if intestatari_data else {}
        prof_1 = professionisti_data[0] if professionisti_data else {}
        
        contesto_base = {
            "Pratica": tipo_pratica,
            "Intervento": tipo_intervento,
            "Sintesi": rel_sintetica,
            "Nome_Intestatario": int_1.get("Nome", ""),
            "Cognome_Intestatario": int_1.get("Cognome", ""),
            "CF_Intestatario": int_1.get("CF", ""),
            "Via_Intestatario": int_1.get("Via", ""),
            "Diritto": int_1.get("Diritto", ""),
            "Nome_Progettista": prof_1.get("Nome", ""),
            "Cognome_Progettista": prof_1.get("Cognome", ""),
            "Albo_Progettista": prof_1.get("Albo", ""),
            "Num_Albo_Progettista": prof_1.get("Num_Albo", ""),
            # Passiamo anche le liste complete per poter usare i cicli nei template complessi
            "Intestatari": intestatari_data,
            "Professionisti": professionisti_data
        }

        # 2. Iteriamo sui documenti richiesti
        for doc_name, files in file_templates.items():
            if files["template"] is not None:
                st.write(f"⚙️ Elaborazione: **{doc_name}**...")
                
                # A. Estrazione testo dallo spunto (se presente)
                testo_spunto = estrai_testo_pdf(files["spunto"]) if files["spunto"] else "Nessuno spunto fornito."
                
                # B. Chiamata a Ollama
                testo_ai = genera_testo_ollama(doc_name, testo_spunto)
                
                # C. Compilazione Template Word
                doc = DocxTemplate(files["template"])
                
                # Aggiungiamo il testo AI al contesto specifico per questo documento
                contesto_specifico = contesto_base.copy()
                contesto_specifico["Testo_Generato_Da_AI"] = testo_ai
                
                doc.render(contesto_specifico)
                
                # D. Prepariamo il file per il download
                io_stream = BytesIO()
                doc.save(io_stream)
                
                st.download_button(
                    label=f"⬇️ Scarica {doc_name} compilato",
                    data=io_stream.getvalue(),
                    file_name=f"{doc_name.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"dl_{doc_name}"
                )
            else:
                st.warning(f"⚠️ Carica il template .docx per la '{doc_name}' per poterla compilare.")
