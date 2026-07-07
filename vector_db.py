import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from constants import EMBEDDING_MODEL_NAME

class VectorDB:
    def __init__(self, db_path, collection_name):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # Initialisation de la collection avec métadonnée de traçabilité du modèle
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"embedding_model": EMBEDDING_MODEL_NAME}
        )

    def add_documents(self, texts, metadatas, ids):
        # Encodage avec normalisation pour optimisation de la similarité cosinus
        embeddings = self.model.encode(texts, normalize_embeddings=True).tolist()
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve(self, query, top_k=3):
        query_embedding = self.model.encode([query], normalize_embeddings=True).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        return results