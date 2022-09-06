from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
#chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)
url='http://dataopen.dg.gov.cn/dataopen/data2/detailIndex.do?dirId=4028818e41fb0cad0141fb0ee2160571'
browser.get(url)
button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.menu_main_content.div_bottom_border>a:nth-child(4)>div'))) 
button.click()
for j in range(1,81):
    input_ = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input._cur_page')))
    input_.clear()
    input_.send_keys(j)
    button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type=button]'))) 
    button.click()
    time.sleep(random.uniform(1,2))
    for i in range(1,6):
        button1=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'tr:nth-child({}) td:nth-child(7) span.document_div_span2 a'.format(i)))) 
        button1.click()
        #time.sleep(random.uniform(0,1))
        
        
        

