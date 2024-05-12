from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Initialize the web driver

# URL of the website
url = "http://www.koeri.boun.edu.tr/sismo/zeqdb/indexeng.asp"

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {
  "download.default_directory": r"D:\Boun\SWE 599\project\earthquake_analysis\data\files2\\",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=chromeOptions)

# Open the website in the browser
driver.get(url)

main_window_handle = driver.current_window_handle

def fetch_data_for_year(year):
    # Wait for the element to be located
    wait = WebDriverWait(driver, 20)
    year_begin = wait.until(EC.presence_of_element_located((By.ID, "recYYYY1")))
    month_begin = wait.until(EC.presence_of_element_located((By.ID, "recAA1")))
    day_begin = wait.until(EC.presence_of_element_located((By.ID, "recGG1")))

    year_end = wait.until(EC.presence_of_element_located((By.ID, "recYYYY2")))
    month_end = wait.until(EC.presence_of_element_located((By.ID, "recAA2")))
    day_end = wait.until(EC.presence_of_element_located((By.ID, "recGG2")))

    magnitude_min = wait.until(EC.presence_of_element_located((By.ID, "recMAG1")))

    select_element = wait.until(EC.element_to_be_clickable((By.ID, "selectEventType")))

    search_btn = wait.until(EC.presence_of_element_located((By.ID, "AraBulRec")))

    # clear the input fields
    year_begin.clear()  
    month_begin.clear()
    day_begin.clear()

    year_end.clear()
    month_end.clear()
    day_end.clear()

    magnitude_min.clear()

    # Input the values
    year_begin.send_keys(str(year))
    month_begin.send_keys("01")
    day_begin.send_keys("01")

    year_end.send_keys(str(year))
    month_end.send_keys("06")
    day_end.send_keys("1")

    magnitude_min.send_keys("0")

    # Select the earthquake type
    select = Select(select_element)
    select.select_by_value("Deprem")

    # Click the search button
    search_btn.click()

    # Wait for the result to be generated
    iframe = wait.until(EC.presence_of_element_located((By.ID, "eqListFrame")))
    driver.switch_to.frame(iframe)

    download_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSave")))
    download_btn.click()

    time.sleep(10)

    # Close the popup window
    for handle in driver.window_handles:
        if handle != main_window_handle:
            driver.switch_to.window(handle)
            driver.close()

    # Switch back to the main window
    driver.switch_to.window(main_window_handle)

    driver.switch_to.default_content()

    # Click new search to clear the fields for the next iteration
    new_search = wait.until(EC.element_to_be_clickable((By.ID, "temizle")))
    new_search.click()

    wait = WebDriverWait(driver, 20)
    year_begin = wait.until(EC.presence_of_element_located((By.ID, "recYYYY1")))
    month_begin = wait.until(EC.presence_of_element_located((By.ID, "recAA1")))
    day_begin = wait.until(EC.presence_of_element_located((By.ID, "recGG1")))

    year_end = wait.until(EC.presence_of_element_located((By.ID, "recYYYY2")))
    month_end = wait.until(EC.presence_of_element_located((By.ID, "recAA2")))
    day_end = wait.until(EC.presence_of_element_located((By.ID, "recGG2")))

    magnitude_min = wait.until(EC.presence_of_element_located((By.ID, "recMAG1")))

    select_element = wait.until(EC.element_to_be_clickable((By.ID, "selectEventType")))

    search_btn = wait.until(EC.presence_of_element_located((By.ID, "AraBulRec")))

    # clear the input fields
    year_begin.clear()  
    month_begin.clear()
    day_begin.clear()

    year_end.clear()
    month_end.clear()
    day_end.clear()

    magnitude_min.clear()

    # Input the values
    year_begin.send_keys(str(year))
    month_begin.send_keys("06")
    day_begin.send_keys("02")

    year_end.send_keys(str(year))
    month_end.send_keys("12")
    day_end.send_keys("31")

    magnitude_min.send_keys("0")

    # Select the earthquake type
    select = Select(select_element)
    select.select_by_value("Deprem")

    # Click the search button
    search_btn.click()

    # Wait for the result to be generated
    iframe = wait.until(EC.presence_of_element_located((By.ID, "eqListFrame")))
    driver.switch_to.frame(iframe)

    download_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSave")))
    download_btn.click()

    time.sleep(10)

    # Close the popup window
    for handle in driver.window_handles:
        if handle != main_window_handle:
            driver.switch_to.window(handle)
            driver.close()

    # Switch back to the main window
    driver.switch_to.window(main_window_handle)

    driver.switch_to.default_content()

    # Click new search to clear the fields for the next iteration
    new_search = wait.until(EC.element_to_be_clickable((By.ID, "temizle")))
    new_search.click()

# Loop through the years
for year in range(2014, 1990, -1):
    fetch_data_for_year(year)

# Close the browser
driver.quit()
