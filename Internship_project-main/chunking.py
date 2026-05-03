from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

from scrap_sunbeam_cirtified_courses import scrape_courses_page
from scrape_about_us import scrape_aboutus_page
from scrap_internship import scrape_internship_page
from scrape_entrance_course import scrape_enter_page
from scrape_mastering_mcq import scrape_master_page

# --------------------------------------------------
# Text Splitter
# --------------------------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

# --------------------------------------------------
# Normalize + Chunk + Metadata
# --------------------------------------------------
def normalize_scraped_output(scraped_data, source):
    documents = []

    if scraped_data is None:
        return []

    for item in scraped_data:
        if isinstance(item, str):
            documents.append(
                Document(
                    page_content=item,
                    metadata={"source": source}
                )
            )
        elif isinstance(item, dict):
            documents.append(
                Document(
                    page_content=json.dumps(item, ensure_ascii=False),
                    metadata={
                        "source": source,
                        "type": "structured"
                    }
                )
            )

    chunks = text_splitter.split_documents(documents)

    # add chunk_id
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

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

    about_us = scrape_aboutus_page(driver, "https://www.sunbeaminfo.in/about-us")
    internship = scrape_internship_page(driver, "https://sunbeaminfo.in/internship")
    courses = scrape_courses_page(driver, urls)
    entrance = scrape_enter_page(driver, "https://www.sunbeaminfo.in/pre-cat")
    mcq = scrape_master_page(driver, "https://sunbeaminfo.in/modular-courses.php?mdid=57")

    docs1 = normalize_scraped_output(about_us, "about-us")
    docs2 = normalize_scraped_output(internship, "internship")
    docs3 = normalize_scraped_output(courses, "courses")
    docs4 = normalize_scraped_output(entrance, "pre-cat")
    docs5 = normalize_scraped_output(mcq, "mcq")

    all_docs = docs1 + docs2 + docs3 + docs4 + docs5

    print("Total docs:", len(all_docs))

    # 🔍 VERIFY METADATA
    for d in all_docs:
        print("CONTENT:", d.page_content[:100])
        print("METADATA:", d.metadata)
        print("-" * 60)

    driver.quit()
