from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#get counter from file
f = open("votecount.txt")
count = int(f.read())
so_far = 0
vote_limit_write = 1




while True:
    try:
                
        options = webdriver.ChromeOptions()

        options.add_extension('./captcha-solver.crx')

        driver = webdriver.Chrome(options)
        driver.get("https://www.beano.com/posts/britains-funniest-class")
        driver.implicitly_wait(3)

        cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookie_button.click()
        school = driver.find_element(By.XPATH, "//*[@src='https://www.beano.com/wp-content/uploads/2023/03/BFC24_Joke-10.png?strip=all&quality=76&w=434']")
        school.click()

        time.sleep(2)
        div_element = driver.find_element(By.CSS_SELECTOR, ".beano-poll-v2__question-results")
        # while True:
            # try:
        WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_attribute((By.CSS_SELECTOR, ".beano-poll-v2__question-results"), "style", "block"))
                # pass
            # except:
                # break

            

        time.sleep(2)

        so_far += 1
        if so_far == vote_limit_write:
                count += vote_limit_write
                so_far = 0
                f = open("votecount.txt", "w")
                f.write(f"{count}")
        print (count + so_far)
                # wait_until = input("PRESS ENTER TO CONTINUE")
            # except:
            #     pass
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("error", e)
        pass