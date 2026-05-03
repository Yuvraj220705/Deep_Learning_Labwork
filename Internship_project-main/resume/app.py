import streamlit as st
from rag import RAG
import pandas as pd
import tempfile
from langchain_community.document_loaders import PyPDFLoader

app = RAG()
vs = app.get_vector_store()
st.title("AI Enabled Resume Management")

file = st.file_uploader("Add/Update Resume PDF: ", type=["pdf"])
if file:
    # 1. Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.getvalue())
        temp_file_path = tmp_file.name
    
    st.success(f"File uploaded to: {temp_file_path}")

    # 2. Use PyPDFLoader with the temporary file path
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()
    # Load the documents (each page becomes a separate Document object)
    pdf_content = ""
    pages = loader.load()
    for page in pages:
        pdf_content += page.page_content
    
    # this is yet incomplete...

st.header("Resumes")
resume_list = vs.find_all_documents()
resume_list = [{"id": resume["id"], "type": resume["metadata"]["topic"], "document": " ".join(resume["document"].split()[:2])} for resume in resume_list]
resume_df = pd.DataFrame(resume_list)
st.dataframe(resume_df)

job_desc = st.text_area("Job Description")
find_resumes_btn = st.button("Find Resumes")
if job_desc:
    resume_details = app.get_shortlisted_resumes(job_desc)
    st.write(resume_details)
