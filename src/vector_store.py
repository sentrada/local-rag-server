"""Vector Store using ChromaDB"""

import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages vector storage and retrieval using ChromaDB"""
    
    def __init__(
        self,
        db_path: str = "/app/data/chroma_db",
        embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
        collection_name: str = "code_chunks"
    ):
        self.db_path = db_path
        self.embedding_model_name = embedding_model
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def add_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> None:
        """Add documents to the vector store"""
        if not documents:
            return
        
        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # Generate unique ID
            doc_id = f"{doc.get('file_path', 'unknown')}_{doc.get('chunk_index', 0)}"
            ids.append(doc_id)
            
            # Extract text content
            text = doc.get('content', doc.get('code', ''))
            texts.append(text)
            
            # Prepare metadata (ChromaDB doesn't support nested dicts)
            metadata = {
                'file_path': str(doc.get('file_path', '')),
                'chunk_index': int(doc.get('chunk_index', 0)),
                'file_extension': str(doc.get('file_extension', '')),
                'chunk_type': str(doc.get('type', 'code')),
            }
            
            if 'function_name' in doc:
                metadata['function_name'] = str(doc['function_name'])
            if 'class_name' in doc:
                metadata['class_name'] = str(doc['class_name'])
            if 'start_line' in doc:
                metadata['start_line'] = int(doc['start_line'])
            if 'end_line' in doc:
                metadata['end_line'] = int(doc['end_line'])
            
            metadatas.append(metadata)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        embeddings_list = embeddings.tolist()
        
        # Add to collection (upsert to handle duplicates)
        try:
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas
            )
            logger.debug(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def search_similar(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query], show_progress_bar=False)
            query_embedding_list = query_embedding.tolist()
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=query_embedding_list,
                n_results=n_results,
                where=filter_metadata
            )
            
            logger.debug(f"Found {len(results.get('documents', [[]])[0])} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def delete_by_file(self, file_path: str) -> None:
        """Delete all chunks from a specific file"""
        try:
            self.collection.delete(
                where={"file_path": file_path}
            )
            logger.info(f"Deleted chunks for file: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file chunks: {e}")
    
    def clear_all(self) -> None:
        """Clear all documents from the collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Cleared all documents from vector store")
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")
    
    def get_collection_count(self) -> int:
        """Get total number of documents in collection"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0
