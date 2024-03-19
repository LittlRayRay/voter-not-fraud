from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#get counter from file
f = open("votecount.txt")
count = int(f.read())
so_far = 0
vote_limit_write = 1

while True:
    # try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(chrome_options)
        driver.get("https://www.beano.com/posts/britains-funniest-class")
        driver.implicitly_wait(2)
        cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookie_button.click()
        school = driver.find_element(By.XPATH, "//*[@src='https://www.beano.com/wp-content/uploads/2023/03/BFC24_Joke-10.png?strip=all&quality=76&w=434']")
        school.click()
        time.sleep(1.5)
        driver.refresh()
        so_far += 1
        if so_far == vote_limit_write:
                count += vote_limit_write
                so_far = 0
                f = open("votecount.txt", "w")
                f.write(count)
        print (count + so_far)
        # wait_until = input("PRESS ENTER TO CONTINUE")
    # except:
    #     pass