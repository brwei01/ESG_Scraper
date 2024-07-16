import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Setup chrome options for downloads
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
download_path = "/Users/apple/Dev/test"
chrome_options.add_experimental_option('prefs',
                                       {
                                           "download.default_directory": download_path,
                                           "download.prompt_for_download": False,
                                           "download.directory_upgrade": True,
                                           "plugins.always_open_pdf_externally": True
                                       })

# Set up the webdriver
service = Service(r'/Users/apple/Dev/tools/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Try to click the search btn
try:
    # open target url
    url = "https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en"
    driver.get(url)

    # Search pattern for PDF files
    pdf_pattern = re.compile(r'\.pdf$', re.IGNORECASE)
    # Search patters for ESG and env-related docs
    esg_pattern = re.compile(r'\b(ESG|environment|environmental)\b', re.IGNORECASE)

    search_btn = driver.find_element(By.CLASS_NAME, 'filter__btn-applyFilters-js')
    search_btn.click()
    time.sleep(1)

    # Close cookie consent if present
    try:
        cookie_close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        cookie_close_btn.click()
    except TimeoutException:
        print("Cookie consent banner not found or no close button present.")
    except NoSuchElementException:
        print("No cookie consent banner found.")

    # Load all records
    try:
        # Find the showing count element
        showing_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "component-loadmore-leftPart__container"))
        )
        showing_count_content = showing_count_element.text
        parts = showing_count_content.split()
        showing_count_number = int(parts[1])
        total_count_number = int(parts[3])

        # while showing_count_number < total_count_number:
        while showing_count_number < 500:
            print(showing_count_number)
            try:
                # Find the "LOAD MORE" button
                load_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.component-loadmore__link.component-loadmore__icon"))
                )

                # Scroll to the "LOAD MORE" button
                driver.execute_script("arguments[0].scrollIntoView(true);", load_btn)
                time.sleep(1)  # Wait for scrolling

                # Try clicking the "LOAD MORE" button
                load_btn.click()
                time.sleep(1)  # Wait for new content to load

                # Re-fetch the showing count element
                showing_count_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "component-loadmore-leftPart__container"))
                )
                showing_count_content = showing_count_element.text
                parts = showing_count_content.split()
                showing_count_number = int(parts[1])
                total_count_number = int(parts[3])

            except ElementClickInterceptedException:
                print("Element click intercepted. Trying to scroll to the button.")
                driver.execute_script("arguments[0].scrollIntoView(true);", load_btn)
                time.sleep(1)  # Wait for scrolling
                driver.execute_script("arguments[0].click();", load_btn)

            except StaleElementReferenceException:
                print("Stale element reference exception. Refetching the element.")
                time.sleep(2)  # Wait for the page to stabilize

    except TimeoutException:
        print("Element not found within the provided time.")
    except NoSuchElementException as e:
        print(f"An error occurred: {e}")

    print("================")
    print("loading finished")
    print("================")

    # Find links to documents
    row_elements = driver.find_elements(By.CLASS_NAME, "doc-link")
    for row_element in row_elements:
        try:
            link_element = row_element.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")

            if esg_pattern.search(link_element.text):
                print(f"Found ESG related pdf doc: {href}!")
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
                    link_element.click()
                    # time.sleep(1)
                except NoSuchElementException:
                    print("Element click intercepted. try to dismiss modal or overlay")
                    driver.back()
                    continue

        except NoSuchElementException:
            print("Anchor tag (doc-link) not found in this row")

finally:
    # Close the browser
    driver.quit()