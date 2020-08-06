# need selenium-wire
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


LOGIN_INFO = {
    'id': input('아이디를 입력하세요:'),
    'pwd': input('비밀번호를 입력하세요:')
}

DEFINED_ID = {
    'sugang_jungbo_button': 'mainframe.childframe.form.div_leftFrame.form.grid_leftMenu.body.gridrow_3.cell_3_0.celltreeitem.treeitemtext',
    'sugang_plan_button': 'mainframe.childframe.form.div_leftFrame.form.grid_leftMenu.body.gridrow_6.cell_6_0.celltreeitem.treeitemtext',
    'department_dropdown': 'mainframe.childframe.form.divForm8381.form.div_arg1.form.cb_dept_cd',
    'department_dropdown_item': 'mainframe.childframe.form.divForm8381.form.div_arg1.form.cb_dept_cd.combopopup',
    'search_button': 'mainframe.childframe.form.divForm8381.form.MenuBtn1.form.menuBbtn_search1',
}
chrome_driver_file = ChromeDriverManager().install()
driver = webdriver.Chrome(chrome_driver_file)
driver.implicitly_wait(3)
url = 'https://kut90.koreatech.ac.kr/login/LoginPage.do'
driver.get(url)
driver.find_element_by_id('id').send_keys(LOGIN_INFO["id"])
driver.find_element_by_id('pwd').send_keys(LOGIN_INFO["pwd"])
driver.execute_script("doLogin()")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, DEFINED_ID['sugang_jungbo_button'])))

sugang_jungbo_button = driver.find_element_by_id(DEFINED_ID['sugang_jungbo_button'])
sugang_jungbo_button.click()
sugang_plan_button = driver.find_element_by_id(DEFINED_ID['sugang_plan_button'])
sugang_plan_button.click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, DEFINED_ID['department_dropdown'])))
department_dropdown = driver.find_element_by_id(DEFINED_ID['department_dropdown'])
department_dropdown.click()
department_dropdown_item = driver.find_element_by_id(DEFINED_ID['department_dropdown_item'])
department_dropdown_item.click()
del driver.requests
search_button = driver.find_element_by_id(DEFINED_ID['search_button'])
search_button.click()
time.sleep(10)
print(driver.last_request.response.body.decode("utf-8"))
f = open("test.xml", "w", -1, 'utf-8')
f.write(driver.last_request.response.body.decode("utf-8"))
f.close()
driver.close()