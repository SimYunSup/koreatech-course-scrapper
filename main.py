# need selenium-wire
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrap_parser import course_parser
import time
import json

with open("selector.json") as selector:
    DEFINED_ID = json.load(selector)

with open("secrets.json") as secret:
    LOGIN_INFO = json.load(secret)


def scrap_course(logininfo, definedID):
    chrome_driver_file = ChromeDriverManager().install()
    driver = webdriver.Chrome(chrome_driver_file)
    driver.implicitly_wait(3)
    url = 'https://kut90.koreatech.ac.kr/login/LoginPage.do'
    driver.get(url)
    driver.find_element_by_id('id').send_keys(logininfo["id"])
    driver.find_element_by_id('pwd').send_keys(logininfo["pwd"])
    driver.execute_script("doLogin()")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, definedID['sugang_jungbo_button'])))

    sugang_jungbo_button = driver.find_element_by_id(definedID['sugang_jungbo_button'])
    sugang_jungbo_button.click()
    sugang_plan_button = driver.find_element_by_id(definedID['sugang_plan_button'])
    sugang_plan_button.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, definedID['department_dropdown'])))
    department_dropdown = driver.find_element_by_id(definedID['department_dropdown'])
    department_dropdown.click()
    department_dropdown_item = driver.find_element_by_id(definedID['department_dropdown_item'])
    department_dropdown_item.click()
    del driver.requests
    search_button = driver.find_element_by_id(definedID['search_button'])
    search_button.click()
    time.sleep(10)

    course_data = driver.last_request.response.body.decode("utf-8")
    driver.close()

    return course_data


if __name__ == "__main__":
    data = scrap_course(LOGIN_INFO, DEFINED_ID)
    json = course_parser(data)
