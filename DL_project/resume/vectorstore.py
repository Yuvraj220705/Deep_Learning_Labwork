import chromadb

class VectorStore:
    def __init__(self, persist_dir:str, query_embed_func=None, docs_embed_func=None):
        self.persist_dir = persist_dir
        self.db = chromadb.PersistentClient(path=persist_dir)
        self.col = self.db.get_or_create_collection("resumes")
        self.query_embed_func = query_embed_func
        self.docs_embed_func = docs_embed_func
    
    def add_documents(self, docs, metadatas, doc_ids, embeddings=None) -> bool:
        if not embeddings:
            if self.docs_embed_func:
                embeddings = self.docs_embed_func(docs)
        if embeddings:
            self.col.add(doc_ids, embeddings, metadatas, docs)
            return True
        return False

    def add_document(self, doc, metadata:dict, doc_id:str, embedding=None) -> bool:
        embeddings = [embedding] if embedding else None
        return self.add_documents([doc], [metadata], [doc_id], embeddings)
    
    def delete_document(self, doc_id:str=None, where:dict=None) -> bool:
        result = self.col.get(ids=[doc_id], where=where)
        if result["ids"]:
            self.col.delete(ids=[doc_id], where=where)
            return True
        return False
    
    def find_document_by_id(self, doc_id):
        result = self.col.get(ids=[doc_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "document": result["documents"][0],
                "metadata": result["metadatas"][0]
            }
        return None
    
    def find_all_documents(self):
        results = self.col.get()
        found_results = []
        for id, doc, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            found_results.append({
                "id": id,
                "document": doc,
                "metadata": metadata
            })
        return found_results

    def update_document(self, doc, metadata:dict, doc_id:str, embedding=None) -> bool:
        if self.delete_document(doc_id):
            return self.add_document(doc, metadata, doc_id, embedding)
        return False
    
    def find_similar_documents(self, query_text, max_results=5):
        query_embedding = self.query_embed_func(query_text)
        results = self.col.query(query_embeddings=[query_embedding], n_results=max_results)
        found_results = []
        for id, doc, metadata, distance in zip(results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]):
            found_results.append({
                "id": id,
                "document": doc,
                "metadata": metadata,
                "distance": distance
            })
        return found_results
