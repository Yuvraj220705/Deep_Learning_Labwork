from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_modular_courses_page(driver, url):
    
    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        docs = []
        
        # Wait for course container
        container = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.row.modular_courses_home_wrap")
            )
        )

        # Get all course cards
        course_cards = container.find_elements(By.CSS_SELECTOR, ":scope > div")


        courses = []

        for card in course_cards:
            try:
                title = card.find_element(By.TAG_NAME, "h4").text.strip()
            except:
                title = "N/A"

            try:
                duration = card.find_element(By.XPATH, ".//*[contains(text(),'Duration')]").text.strip()

            except:
                duration = "N/A"

            try:
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "N/A"

            docs.append({
                "title": title,
                "duration": duration,
                "link": link
            })

        return docs

        
    except Exception as e:
        print("Error: ", e)
      
    finally:
        driver.quit()   
        
             
def scrape_courses_page(driver, urls):
    wait = WebDriverWait(driver, 15)
    docs = []

    try:
        for url in urls:
            driver.get(url)
            # print("Page title:", driver.title)

            # -----------------------------
            # Main course info
            # -----------------------------
            container = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".course_info.wow.fadeInUp")
                )
            )

            paras = container.find_elements(By.CSS_SELECTOR, "h3, p, span")
            for p in paras:
                text = p.text.strip()
                if text:
                    docs.append(text)

            # -----------------------------
            # Accordion panels
            # -----------------------------
            headers = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".panel-title a")
                )
            )

            for header in headers:
                driver.execute_script("arguments[0].scrollIntoView(true);", header)
                driver.execute_script("arguments[0].click();", header)

                panel = wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".panel-collapse.in")
                    )
                )

                # 📄 Panel text
                panel_text = panel.text.strip()
                if panel_text:
                    docs.append(panel_text)

                # 🎥 YouTube links (add directly to docs)
                iframes = panel.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    src = iframe.get_attribute("src")
                    if src and "youtube.com" in src:
                        docs.append(f"VIDEO: {src}")

        return docs

    except Exception as e:
        print("Error:", e)
        return []

    # finally:
    #     driver.quit()


if __name__ == "__main__":
    
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

    driver = webdriver.Chrome()
    docs = scrape_modular_courses_page(driver, urls)
    
    for d in docs:
        print(d)