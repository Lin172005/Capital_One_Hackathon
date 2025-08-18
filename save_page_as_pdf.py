from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
import time
import os
from datetime import datetime

def save_page_as_pdf():
    url = "https://www.kisandeals.com/mandiprices/PADDY/ALL/ALL"
    output_dir = "pdf_reports"
    os.makedirs(output_dir, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")   # new headless mode (stable)
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # wait for table to load (increase if needed)
    time.sleep(5)

    # Call DevTools Protocol directly
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})

    today = datetime.now().strftime("%Y-%m-%d")
    pdf_path = os.path.join(output_dir, f"paddy_price_{today}.pdf")

    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf['data']))

    print(f"✅ PDF saved to {pdf_path}")
    driver.quit()

if __name__ == "__main__":
    save_page_as_pdf()
