import pandas as pd
from vector_db import VectorDB

# Configuration
CSV_PATH = "data/05_corpus_rag.csv"
DB_PATH = "chroma_db"
COLLECTION_NAME = "corpus_absurde"

def run_indexing():
    # Chargement du corpus (Pandas gère parfaitement le CSV)
    df = pd.read_csv(CSV_PATH)
    
    # Initialisation de la base vectorielle
    vdb = VectorDB(DB_PATH, COLLECTION_NAME)
    
    # Préparation des données
    texts = df['text'].tolist()
    ids = df['id'].tolist()
    # On garde la source et la catégorie pour que le LLM puisse citer ses sources plus tard
    metadatas = df[['source', 'categorie']].to_dict(orient='records')
    
    print(f"Indexation de {len(texts)} documents en cours...")
    vdb.add_documents(texts=texts, metadatas=metadatas, ids=ids)
    print("Base vectorielle créée et sauvegardée avec succès !")

if __name__ == "__main__":
    run_indexing()