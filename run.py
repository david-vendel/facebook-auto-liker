from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from random import randint
import random
from time_util import sleep

like_amount = 100
fb_username = '@gmail.com'
fb_password = ''
scroll_speed = 0.3

class FacebookLiker():

    def AutoLiker(self):
        baseUrl = "https://www.facebook.com/"
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)

        driver.get('http://google.com')

        driver.get(baseUrl)
        sleep(0.5)
        driver.set_window_size(1111, 1000)
        sleep(0.5)
        email = driver.find_element(By.XPATH,"//*[@id='email']")
        password = driver.find_element(By.XPATH,"//*[@id='pass']")

        email.send_keys(fb_username)
        sleep(0.1)
        password.send_keys(fb_password)
        sleep(0.2)
        driver.find_element(By.XPATH,"//input[@data-testid='royal_login_button']").click()
        sleep(1)
        liked = 0
        tre = 0 #error counter - if error 3x in a row, will refresh page
        i = -1 #index of like element in newsfeed
        body_elem = driver.find_element_by_tag_name('body')  
        print ("Going to like",like_amount,"photos.")
        while liked<like_amount: 
            print ("Liked", liked,"/",like_amount)
            try:
                
                i+=1
                likes = driver.find_elements_by_xpath("//div[contains(@class, '_khz') and contains(@class, '_4sz1')]")
                try:
                    like_el = likes[i].find_elements_by_xpath("a[contains(@aria-pressed, 'true')]")

                    if len(like_el)>0:
                        print ("Already liked")
                    else:
                        likes[i].click()
                        liked +=1                       
                except Exception as e:
                    #print (e)
                    pass

                try:
                    discover_el = driver.find_elements_by_xpath('//*[@id="appsNav"]/h4')
                except:
                    print ("Couldn't locate the left panel placeholder. Terminating.")
                    sleep(1)
                    break
                discover_el_location = discover_el[0].location
                #print (discover_el_location)
                location = likes[i].location
                size = likes[i].size
                #print(location['y'])
                #print(size)
                body_elem.send_keys(Keys.DOWN)
                body_elem.send_keys(Keys.DOWN)

                body_elem = driver.find_element_by_tag_name('body')     
                while discover_el_location['y']+80<location['y']:      
                    if discover_el_location['y']+2000<location['y']:
                        print ("Things are out of order, either you scrolled up or window width is too small. Terminating")
                        sleep(1)
                        return
                    #print ("i is",i)
                    discover_el = driver.find_elements_by_xpath('//*[@id="appsNav"]/h4')
                    discover_el_location = discover_el[0].location
                    location = likes[i].location
                    size = likes[i].size
                    body_elem.send_keys(Keys.DOWN)
                    if location['y'] > 20000: #will refresh page if scrolled too deep
                        print ("Feed too deep, refreshing")
                        driver.get("http://www.facebook.com") 
                        n = random.randint (2,11)
                        print ("sleeping for ",n)
                        sleep(n)
                        i =-1 
                                                
                    sleep(scroll_speed)    
                 
                #driver.get("https://www.facebook.com/")
            except Exception as e:
                print (e)
                if tre < 3:
                    print ("Refreshing in.. :", 4-tre)
                    tre+=1
                    sleep(1)
                    body_elem = driver.find_element_by_tag_name('body')     
                    body_elem.send_keys(Keys.DOWN)
                    body_elem.send_keys(Keys.DOWN)      
                    sleep(1)
                    
                else:
                    print ("Things are bad. refreshing")
                    tre=0
                    driver.get("http://www.facebook.com")
                    
                    sleep(5)
                    i = 0
        
        


print("*"*54)
print ("*"*11,"WELCOME AT FACEBOOK MASS LIKER","*"*11)
print("*"*54)

session = FacebookLiker()

session.AutoLiker()
sleep(5)
