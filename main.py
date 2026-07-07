from rag import RAG

# Initialisation de l'orchestrateur
assistant = RAG("chroma_db", "corpus_absurde")

print("=== Assistant RAG Prêt ===")
while True:
    user_query = input("\nPose ta question (ou 'exit' pour quitter) : ")
    if user_query.lower() == 'exit':
        break
        
    reponse = assistant.answer_question(user_query)
    print(f"\nAssistant : {reponse}")