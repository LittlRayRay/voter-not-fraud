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


successes = 0

def instance():
    schools_randoms = [1,1,1,1,1,1,1,1,1,1]
    global successes
    while True:
        
        # proxy = "185.245.80.156:3128"

        try:
            
            options = webdriver.ChromeOptions()
            webdriver.DesiredCapabilities.CHROME['acceptInsecureCerts']=True
            options.add_extension('./captcha-solver.crx')
            # options.add_argument(f'--proxy-server=http://' + str(proxy))
            if cfg['headless']:
                options.add_argument('--headless=new')

            driver = webdriver.Chrome(options)
            driver.get("https://www.beano.com/posts/britains-funniest-class")
            driver.implicitly_wait(3)
            time.sleep(2)
            cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            cookie_button.click()
            time.sleep(2)
            
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
                    
            else:
                school = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div[1]/article/div/div[2]/div[1]/div[9]/figure/img")
            school.click()

            try:
                time.sleep(3)
                element= WebDriverWait(driver, 75).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Results')]")))
                successes += 1
                print(successes, "completed")
                time.sleep(2)
                driver.close()

                
                if successes % 25 == 0:
                    print("####################################")
                    percentages = driver.find_elements(By.CLASS_NAME,"progress--filled")
                    
                    for idx,i in enumerate(percentages):
                        percent_val = i.get_attribute('style').split(';')[0].split(':')[1]
                        schools_randoms[idx] = 1/(float(percent_val.strip('%'))/100) 
                        print("School, percentage vote, stratified val", idx,percent_val,schools_randoms[idx])
            except:
                pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error: ", e)
            

if __name__ == "__main__":
    for _ in range(cfg['n_threads']):
        threading.Thread(target=instance).start()
