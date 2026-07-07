import streamlit as st
from rag import RAG

# Configuration de la page Streamlit
st.set_page_config(page_title="Mon Assistant RAG", page_icon="🤖")

@st.cache_resource
def load_rag():
    # On charge l'orchestrateur une seule fois pour optimiser
    return RAG("chroma_db", "corpus_absurde")

# Initialisation de l'assistant
assistant = load_rag()

st.title("🤖 Assistant RAG Intelligent")
st.markdown("Posez vos questions sur le corpus (Henri le chat, les villages imaginaires, etc.)")

# Initialisation de l'historique du chat dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Que voulez-vous savoir ?"):
    # Affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse avec l'assistant
    with st.chat_message("assistant"):
        with st.spinner("L'assistant réfléchit..."):
            response = assistant.answer_question(prompt)
            st.markdown(response)
    
    # Sauvegarde de la réponse dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})