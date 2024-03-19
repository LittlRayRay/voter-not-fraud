from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
while True:
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(chrome_options)
        driver.get("https://www.beano.com/posts/britains-funniest-class")
        cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookie_button.click()
        school = driver.find_element(By.XPATH, "//*[@src='https://www.beano.com/wp-content/uploads/2023/03/BFC24_Joke-10.png?strip=all&quality=76&w=434']")
        school.click()
        time.sleep(2.5)
    except:
        pass