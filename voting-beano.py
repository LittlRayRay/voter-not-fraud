from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import threading
import random

# Load config
try:
    with open("cfg.json", mode='r') as cfg_file:
        cfg = json.load(cfg_file)
except FileNotFoundError:
    cfg = {"n_threads": 1, "headless": False, "random_chance": 0.4}
    with open("cfg.json", mode='w') as cfg_file:
        json.dump(cfg, cfg_file, indent="    ")


#get counter from file
f = open("votecount.txt")
count = int(f.read())
so_far = 0
vote_limit_write = 5

successes = 0

def instance():
    schools_randoms = [1,1,1,1,1,1,1,1,1,1]
    global successes
    while True:
        try:
            
            options = webdriver.ChromeOptions()

            options.add_extension('./captcha-solver.crx')
            if cfg['headless']:
                options.add_argument('--headless=new')

            driver = webdriver.Chrome(options)
            driver.get("https://www.beano.com/posts/britains-funniest-class")
            driver.implicitly_wait(3)

            cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            cookie_button.click()

            
            if random.random() < cfg['random_chance']:
                # Select a random one
                schools = driver.find_elements(By.CSS_SELECTOR, '.beano-poll-v2__answer>button')
                
                
                running_total = 0
                total_sum = sum(schools_randoms)
                randum_num = random.random()
				
                for idx, i in enumerate(schools_randoms):
                    
                    running_total += i
                    
                    if running_total >= randum_num * total_sum:
                        school = schools[idx]
                        break
                    
                    #school = random.choice(schools)
            else:
                school = driver.find_element(By.XPATH, "//*[@src='https://www.beano.com/wp-content/uploads/2023/03/BFC24_Joke-10.png?strip=all&quality=76&w=434']")
            school.click()

            # div_element = driver.find_element(By.CSS_SELECTOR, ".beano-poll-v2__question-results")
            # while True:
            while True:
                try:
                    element= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Results')]")))
                    
                    if successes % 25 == 0:
                        print("####################################")
                        percentages = driver.find_elements(By.CLASS_NAME,"progress--filled")
                        
                        for idx,i in enumerate(percentages):
                            percent_val = i.get_attribute('style').split(';')[0].split(':')[1]
                            schools_randoms[idx] = 1/(float(percent_val.strip('%'))/100) 
                            print("School, percentage vote, stratified val", idx,percent_val,schools_randoms[idx])
                            
                    break
                except:
                    pass

            # except:
                    # break

                
            successes += 1
            if successes % 5 == 0:
                print(successes, "completed")

            driver.close()

            # so_far += 1
            # if so_far == vote_limit_write:
            #         count += vote_limit_write
            #         so_far = 0
            #         f = open("votecount.txt", "w")
            #         f.write(f"{count}")
            # print (count + so_far)
                    # wait_until = input("PRESS ENTER TO CONTINUE")
                # except:
                #     pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("E003: error")
  
if __name__ == "__main__":
    for _ in range(cfg['n_threads']):
        threading.Thread(target=instance).start()

