# need selenium-wire
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from scrap_parser import course_parser
import time
import json

with open("selector.json") as selector:
    DEFINED_ID = json.load(selector)

with open("secrets.json") as secret:
    LOGIN_INFO = json.load(secret)


def scrap_course(logininfo, definedID, year, semester):
    chrome_driver_file = ChromeDriverManager().install()
    driver = webdriver.Chrome(chrome_driver_file)
    driver.implicitly_wait(3)
    url = 'https://kut90.koreatech.ac.kr/login/LoginPage.do'
    driver.get(url)
    driver.find_element(By.ID, 'id').send_keys(logininfo["id"])
    driver.find_element(By.ID, 'pwd').send_keys(logininfo["pwd"])
    driver.find_element(By.ID, 'pwd').send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, definedID['sugang_jungbo_button'])))

    sugang_jungbo_button = driver.find_element(By.ID, definedID['sugang_jungbo_button'])
    sugang_jungbo_button.click()
    sugang_plan_button = driver.find_element(By.ID, definedID['sugang_plan_button'])
    sugang_plan_button.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, definedID['department_dropdown'])))
    department_dropdown = driver.find_element(By.ID, definedID['department_dropdown'])
    department_dropdown.click()
    department_dropdown_item = driver.find_element(By.ID, definedID['department_dropdown_item'])
    department_dropdown_item.click()
    year_dropdown = driver.find_element(By.ID, definedID['year_dropdown'])
    year_dropdown.click()
    year_dropdown_item = driver.find_elements(By.XPATH, f"//div[contains(@class, 'nexacontentsbox') and text()='{year}']")[0]
    year_dropdown_item.click()
    semester_dropdown = driver.find_element(By.ID, definedID['semester_dropdown'])
    semester_dropdown.click()
    semester_dropdown_item = driver.find_elements(By.XPATH, f"//div[contains(@class, 'nexacontentsbox') and text()='{semester}']")[0]
    semester_dropdown_item.click()

    del driver.requests
    search_button = driver.find_element(By.ID, definedID['search_button'])
    search_button.click()
    time.sleep(10)

    course_data = driver.last_request.response.body.decode("utf-8")
    driver.close()

    return course_data


if __name__ == "__main__":
    data = scrap_course(LOGIN_INFO, DEFINED_ID, 2022, '2학기')
    with open("test.xml", "w", encoding="UTF-8") as xml_file:
        xml_file.write(data)
    json_data = course_parser(data)
    with open("test.json", "w", encoding="UTF-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)
