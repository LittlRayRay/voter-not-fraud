from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import threading

n_threads = 1

#get counter from file
f = open("votecount.txt")
count = int(f.read())
so_far = 0
vote_limit_write = 5

def instance():
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

            # div_element = driver.find_element(By.CSS_SELECTOR, ".beano-poll-v2__question-results")
            # while True:
            while True:
                try:
                    element= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Results')]")))
                    break
                    print("NE001: Found Element")
                except Exception as e:
                    print(f"E001: error on finding element: {e}")
                    
                except:
                    print("E002: something else failed when trying to find element")

            # except:
                    # break

                

            time.sleep(2)

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
            print("E003: error", e)
            pass
        except:
             print("E004: failed idk why ")

if __name__ == "__main__":
    for _ in range(n_threads):
        threading.Thread(target=instance).start()