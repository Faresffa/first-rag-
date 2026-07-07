import os
from groq import Groq
from dotenv import load_dotenv
from constants import LLM_MODEL_NAME
from vector_db import VectorDB
from moderator import Moderator

load_dotenv()

class RAG:
    def __init__(self, db_path, collection_name):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.vdb = VectorDB(db_path, collection_name)
        self.moderator = Moderator()
        
        # Chargement du template de prompt
        with open("prompts/rag_system_prompt.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def answer_question(self, question):
        # ÉTAPE 1 : Modération (Sécurité)
        mod_result = self.moderator.moderate(question)
        if mod_result.get("is_prompt_injection"):
            return "ALERTE : Requête bloquée par le système de sécurité (tentative d'injection)."

        # ÉTAPE 2 : Recherche (Retrieval)
        search_results = self.vdb.retrieve(question, top_k=3)
        
        # Mise en forme des chunks pour le prompt
        context_chunks = ""
        for i, doc in enumerate(search_results['documents'][0]):
            source = search_results['metadatas'][0][i]['source']
            context_chunks += f"\nExtrait {i+1} : {doc} [Source: {source}]"

        # ÉTAPE 3 : Génération (Augmentation)
        full_system_prompt = self.prompt_template.replace("{{Chunks}}", context_chunks)
        
        completion = self.client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0 # Zéro créativité pour une fidélité maximale
        )
        
        return completion.choices[0].message.content
