# rag.py
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from vectorstore import VectorStore
from agent import RAGAgent

class RAG:
    def __init__(self):
        self.llm = init_chat_model(
            "qwen/qwen3-4b-2507",
            model_provider="openai",
            base_url="http://127.0.0.1:1234/v1",
            api_key="lm-studio",
        )
        self.emb = init_embeddings(
                    "text-embedding-nomic-embed-text-v1.5",
                    provider="openai",
                    base_url="http://127.0.0.1:1234/v1",
                    api_key="lm-studio",
                    check_embedding_ctx_length=False
                )
        self.vs = VectorStore("D:/Nilesh/Internship/GenAI-2/demos/chroma_db", self.emb.embed_query, self.emb.embed_documents)
        self.agent = RAGAgent(self.llm, self.vs)
    
    def get_vector_store(self) -> VectorStore:
        return self.vs

    def get_query_embed_func(self):
        return self.emb.embed_query

    def get_docs_embed_func(self):
        return self.emb.embed_documents

    def get_shortlisted_resumes(self, job_desc):
        return self.agent.run(job_desc)
