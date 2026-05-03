from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_enter_page(driver, url):
    try:
        wait = WebDriverWait(driver, 15)
        driver.get(url)

        print("Pre CAT:", driver.title)

        docs = []

        # ✅ find all accordion headings
        headers = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".panel-title a")
            )
        )

        for header in headers:
            # scroll + click to expand
            driver.execute_script("arguments[0].scrollIntoView(true);", header)
            header.click()

            # wait for content to appear
            content = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".panel-collapse.in")
                )
            )

            text = content.text.strip()
            if text:
                docs.append(text)

        return docs

    except Exception as e:
        print("Error:", e)
        return []

    # finally:
    #     driver.quit()

if __name__ == "__main__":
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.sunbeaminfo.in/pre-cat"
    docs = scrape_enter_page(driver, url)

    for d in docs:
        print(d)
        print("-" * 60)
        
    