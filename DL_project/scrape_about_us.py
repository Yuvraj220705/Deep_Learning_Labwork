from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_aboutus_page(driver, url):
    
    try:
        wait = WebDriverWait(driver, 15)
        driver.get(url)
        docs = []
        
        container = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
            )
        )

        paras = container.find_elements(By.TAG_NAME, "p")
        for p in paras:
            text = p.text.strip()
            if text:
                docs.append(text)
        # wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        # print("Page Title:", driver.title)

        # print("\n---- Panel Content ----\n")

        headers = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".panel-title a"))
        )

        for h in headers:
            driver.execute_script("arguments[0].scrollIntoView(true);", h)
            driver.execute_script("arguments[0].click();", h)

            # wait for the opened panel body
            panel = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".panel-collapse.in")
                )
            )

            panel_text = " ".join(panel.text.split())
            if panel_text:
                docs.append(panel_text)
                
        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".center_loc")))
        contact_text = container.text.strip()
        docs.append(contact_text)
        
        return docs


    except Exception as e:
        print("Error:", e)

    # finally:
    #     # driver.quit()


if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.sunbeaminfo.in/about-us"
    docs = scrape_aboutus_page(driver, url)
    
    print(docs)