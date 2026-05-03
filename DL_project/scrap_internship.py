from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_internship_page(driver, url):
    wait = WebDriverWait(driver, 15)
    docs = []

    try:
        driver.get(url)
        print("Internship page:", driver.title)

        # --------------------------------------------------
        # MAIN INFO SECTION
        # --------------------------------------------------
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

        # --------------------------------------------------
        # ACCORDION SECTION  ✅ ADDED
        # --------------------------------------------------
        accordion = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".about_other_data.accordion_outer_box")
            )
        )

        headers = accordion.find_elements(By.CSS_SELECTOR, ".panel-title a")

        for header in headers:
            title = header.text.strip()

            # scroll & click
            driver.execute_script("arguments[0].scrollIntoView(true);", header)
            driver.execute_script("arguments[0].click();", header)

            # wait for expanded panel
            panel = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".panel-collapse.in")
                )
            )

            content = panel.text.strip()

            if title:
                docs.append(f"SECTION: {title}")
            if content:
                docs.append(content)

        # --------------------------------------------------
        # INTERNSHIP BATCH TABLE
        # --------------------------------------------------
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tbody tr")
            )
        )

        batch_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in batch_rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) < 8:
                continue

            batch_info = {
                "Sr No": cols[0].text.strip(),
                "Batch": cols[1].text.strip(),
                "Batch Duration": cols[2].text.strip(),
                "Start Date": cols[3].text.strip(),
                "End Date": cols[4].text.strip(),
                "Time": cols[5].text.strip(),
                "Fees": cols[6].text.strip(),
                "Brochure": cols[7].text.strip()
            }

            docs.append(batch_info)

        return docs

    except Exception as e:
        print("Error:", e)
        return []

    # finally:
    #     driver.quit()


if __name__ == "__main__":
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://sunbeaminfo.in/internship"
    docs = scrape_internship_page(driver, url)

    for d in docs:
        print(d)
        print("-" * 60)
