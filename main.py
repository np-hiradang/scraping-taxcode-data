from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WEBSITE = "https://masothue.com"
DRIVER_PATH = "chromedriver-mac-x64/chromedriver"
COLUMN_NAMES_FULL=['Tên', 'Tên quốc tế', 'Tên viết tắt', 'Mã số thuế', 'Địa chỉ', 'Người đại diện', 'Điện thoại', 'Ngày hoạt động', 'Quản lý bởi', 'Loại hình DN', 'Tình trạng']
COLUMN_NAMES=['Tên quốc tế', 'Tên viết tắt', 'Mã số thuế', 'Địa chỉ', 'Người đại diện', 'Điện thoại', 'Ngày hoạt động', 'Quản lý bởi', 'Loại hình DN', 'Tình trạng']


def main():
    driver = initialize_driver()
    driver.get(WEBSITE)

    initialize_csv_file()

    for i in range(0, 1):
        TAX_CODE = "0317254701"

        input_search(driver, TAX_CODE)
        
        data = get_data_from_table(driver)

        print(data)

        save_data_to_csv(data)

    driver.quit()

def initialize_driver():
    service = Service(executable_path=DRIVER_PATH)
    options = webdriver.ChromeOptions()
    # options.headless = True
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def input_search(driver, taxcode):
    search_input = driver.find_element(By.ID, "search")

    if search_input.is_displayed():
        # The element is visible, safe to interact
        search_input.send_keys(taxcode)
    else:
        # The element is likely a honeypot, do not interact
        print("Honeypot detected, skipping interaction")

    searchButton = driver.find_element(By.CLASS_NAME, "btn-search-submit")
    searchButton.click()

def get_data_from_table(driver):
    data = []

    title_row = driver.find_element(By.CSS_SELECTOR, '.table-taxinfo thead span')
    data.append(title_row.text)

    # get data in the body
    table_rows = driver.find_elements(By.CSS_SELECTOR, ".table-taxinfo tbody tr")
    i = 0
    table_rows_count = len(table_rows)

    for column in COLUMN_NAMES:
        if i + 1 < table_rows_count:
            cells = table_rows[i].find_elements(By.TAG_NAME, "td")
            if len(cells) > 1:
                if cells[0].text == column:
                    data.append(cells[1].text)
                    i += 1
                else:
                    data.append(None)
            else:
                i += 1
    return data

def initialize_csv_file ():
    df = pd.DataFrame(columns=COLUMN_NAMES_FULL)
    df.to_csv('result.csv', index=False)

def save_data_to_csv(data):
    df = pd.DataFrame([data])
    # use utf-8 encoding for vietnamese characters
    df.to_csv('result.csv', index=False, mode='a', header=False, encoding='utf-8')

main()