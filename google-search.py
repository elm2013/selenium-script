from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote  


# مسیر کروم‌درایور خود را اینجا بگذارید
chrome_driver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# تنظیمات مرورگر

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # اجرای مرورگر بدون رابط گرافیکی
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-crash-reporter')
chrome_options.add_argument('--disable-in-process-stack-traces')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--output=/dev/null')
driver = webdriver.Chrome( options=chrome_options)

# تابع جستجو و ذخیره نتایج
def google_search(query):
    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # صبر برای بارگذاری نتایج جستجو
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

    results = []
   
    search_results = driver.find_elements(By.XPATH, "//div[@class='MjjYud']")
  
   
    for result in search_results:
        try:           
            title = result.find_element(By.XPATH, ".//h3").text
            link = result.find_element(By.XPATH, ".//a").get_attribute("href")
            description = result.find_element(By.XPATH, ".//div[contains(@class, 'VwiC3b') or contains(@class, 'yXK7lf') or contains(@class, 'lVm3ye') or contains(@class, 'r025kc') or contains(@class, 'hJNv6b') or contains(@class, 'Hdw6tb')]").text
            website_name = result.find_element(By.CLASS_NAME, 'VuuXrf').text
            results.append([website_name, title, description, unquote(link) ])
            # print("result 2 :",description)
            
        except Exception as e:
            print(e)
            continue
   
    return results

# ذخیره نتایج در فایل CSV
def save_to_csv(data, filename="google_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Website", "Title", "Description", "URL"])
        writer.writerows(data)

# اجرای خزنده
search_query = "محمدتقی نقدعلی after:2024-09-08 before:2024-09-11"
search_results = google_search(search_query)
save_to_csv(search_results)

# بستن مرورگر
driver.quit()

print("نتایج ذخیره شد.")
