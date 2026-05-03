import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "sunbeam_knowledge"

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs = {"device": "cpu"},
        encode_kwargs = {"normalize_embeddings": True}
    )

def create_chroma_db(chunks):
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)

    embeddings = get_embedding_model()
    
    if not chunks:
        print("Warning: No chunks provided. Skipping vector DB creation.")
        return load_chroma_db()

    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]

    vectordb = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,   # ✅ correct
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_DIR
    )

    vectordb.persist()
    return vectordb


def load_chroma_db():
    embeddings = get_embedding_model()

    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings  # ✅ correct
    )

    return vectordb



if __name__ == "__main__":

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from scrape_about_us import scrape_aboutus_page
    from scrap_internship import scrape_internship_page
    from scrap_sunbeam_cirtified_courses import scrape_courses_page
    from scrape_entrance_course import scrape_enter_page
    from scrape_mastering_mcq import scrape_master_page
    from chunking import normalize_scraped_output

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    try:
        about_docs = scrape_aboutus_page(
            driver,
            "https://www.sunbeaminfo.in/about-us"
        )

        internship_docs = scrape_internship_page(
            driver,
            "https://sunbeaminfo.in/internship"
        )
        
        
        urls = [
        "https://www.sunbeaminfo.in/modular-courses/aptitude-course-in-pune",
        "https://www.sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java",
        "https://sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark",
        "https://sunbeaminfo.in/modular-courses/cpp-classes",
        "https://sunbeaminfo.in/modular-courses/core-java-classes",
        "https://sunbeaminfo.in/modular-courses/Devops-training-institute",
        "https://sunbeaminfo.in/modular-courses/dreamllm-training-institute-pune",
        "https://sunbeaminfo.in/modular-courses/machine-learning-classes",
        "https://sunbeaminfo.in/modular-courses/mastering-generative-ai",
        "https://sunbeaminfo.in/modular-courses.php?mdid=57",
        "https://sunbeaminfo.in/modular-courses/mern-full-stack-developer-course",
        "https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune",
        "https://sunbeaminfo.in/modular-courses/python-classes-in-pune"

        
    ]
        courses_docs = scrape_courses_page(
            driver,
            urls
        )
        
        entrance_docs = scrape_enter_page(
            driver,
            "https://www.sunbeaminfo.in/pre-cat"
        )
        
        master_docs = scrape_master_page(
            driver,
            "https://sunbeaminfo.in/modular-courses.php?mdid=57"
        )
        

        about_chunks = normalize_scraped_output(about_docs, source="about-us")
        internship_chunks = normalize_scraped_output(internship_docs, source="internship")
        courses_chunks = normalize_scraped_output(courses_docs, source="courses")
        entrance_chunks = normalize_scraped_output(entrance_docs, source= "entrance-courses")
        master_chunks = normalize_scraped_output(master_docs , source= "mastering-mcqs ")


        all_chunks = about_chunks + internship_chunks + courses_chunks + entrance_chunks + master_chunks

        print(f"Total chunks: {len(all_chunks)}")

        create_chroma_db(all_chunks)
        print("✅ Chroma DB created using all-MiniLM embeddings")

    finally:
        driver.quit()