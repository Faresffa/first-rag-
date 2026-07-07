from vector_db import VectorDB

# Configuration identique à l'indexation
DB_PATH = "chroma_db"
COLLECTION_NAME = "corpus_absurde"

def test_search():
    # Initialisation (va charger la base existante sur le disque)
    vdb = VectorDB(DB_PATH, COLLECTION_NAME)
    
    # Ta question
    query = "Quelle est la couleur du chat de Bob ?"
    
    print(f"\nRecherche pour : '{query}'")
    results = vdb.retrieve(query, top_k=2)
    
    # Affichage des résultats pour vérifier la pertinence
    for i, doc in enumerate(results['documents'][0]):
        print(f"\nRésultat {i+1}:")
        print(f"Texte : {doc}")
        print(f"Source : {results['metadatas'][0][i]['source']}")

if __name__ == "__main__":
    test_search()