from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_master_page(driver, url):
    wait = WebDriverWait(driver, 15)
    docs = []

    try:
        
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
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://sunbeaminfo.in/modular-courses.php?mdid=57"

    docs = scrape_master_page(driver, url)

    for d in docs:
        print(d)
        print("-" * 60)