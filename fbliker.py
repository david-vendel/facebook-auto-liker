from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os  
from random import randint
import random
from time_util import sleep
import pickle
                           
scroll_speed = 0.3





class FacebookLiker():

    def LoginToFb(self):
        baseUrl = "https://www.facebook.com/"
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
       
        
  
        print ("\n**********************************************\nWelcome to Facebook mass auto liker bot.\n")
        try:
            file = open("./profiles/secret.txt","r") 
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('http://google.com')
            lines = file.readlines()
            fb_username = lines[0]
            fb_password = lines[1]
            like_amount = int(lines[2])
            file.close() 
            print ("Data loaded.")
            
        except:
            #create directory profiles
            if not os.path.exists("profiles"):
                os.makedirs("profiles")
            
            print ("To connect to Facebook, please write your facebook login info here. This will be only stored locally in your PC in secret.txt file and this program doesn't send nothing elsewhere.")
            sleep(1)
            fb_username = input("\nFacebook username ... ")  # Python 3
            sleep(0.3)    
            fb_password = input("Facebook password ... ")  # Python 3
            sleep(0.5)
            print ("\nThis information will be stored in /profiles/secret.txt file. If you want to change them, delete that file and run this program again.")
            
            sleep(0.5)
            like_amount = int(input("\nhow many likes to give? ... "))  # Python 3
            
            file = open("./profiles/secret.txt","w") 
            
            file.write(fb_username)
            file.write("\n")
            file.write(fb_password)
            file.write("\n")    
            file.write(str(like_amount))
            file.write("\n")
            file.close() 
            
            print ("\nAll great!\nI won't ask this information again. You can change them in file secret.txt in /profiles/ directory, or delete that file and run me again.")

            sleep(0.5)
            driver = webdriver.Chrome(options=chrome_options)
            
        try:
            cookies = pickle.load(open("fba-cook.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            print ("added cookies")
        except Exception as err:
            print (err)
            print ("not added cookies")            
        driver.get(baseUrl)
        sleep(0.5)
        driver.set_window_size(1111, 1000)
        try:
            sleep(0.5)
            email = driver.find_element_by_xpath("//*[@id='email']")
            password = driver.find_element_by_xpath("//*[@id='pass']")

            fb_username = fb_username.replace("\n","")
            email.send_keys(fb_username)
            sleep(0.9)
            password.send_keys(fb_password)
            sleep(0.25)
            try:
                driver.find_element_by_xpath("//input[@data-testid='royal_login_button']").click()
            except:
                pass
                sleep(0.5)
            sleep(0.5)
            
        except:
            pass
        pickle.dump(driver.get_cookies() , open("fba-cook.pkl","wb"))
        return driver


    def AutoLiker(self, driver):
        
        file = open("./profiles/secret.txt","r") 
        lines = file.readlines()
        like_amount = int(lines[2])
        file.close() 
        liked = 0
        tre = 0 #error counter - if error 3x in a row, will refresh page
        i = 0 #index of like element in newsfeed
        body_elem = driver.find_element_by_tag_name('body')  
        print ("Going to like",like_amount,"photos.")     
        while liked<=like_amount:                       
            print ("Liked", liked,"/",like_amount)
            try:
                if i>25:
                    print ("Let's reload")
                   
                    driver.get("http://www.facebook.com")
                    
                    sleep(5)
                    i = 0
             
                likes = driver.find_elements_by_xpath("//a[contains(@aria-pressed, 'false')]")  
                print ("There are ",len(likes), " on this page.")
                if (random.randint(1,100)<65):    
                    print ("liking")
                    try:
                        likes[i].click()
                        liked +=1
                        n = random.randint(1,300)
                        n = n/100
                        print (n, 3**n)
                        
                        sleep(3**n )
                    except:
                        print ("cant click")
                        sleep(1)
                        i+=1
                        body_elem.send_keys(Keys.ESCAPE)
                        sleep(0.1)
                        body_elem.send_keys(Keys.DOWN)
                        sleep(0.1)
                        body_elem.send_keys(Keys.DOWN)
                        sleep(0.1)
                        body_elem.send_keys(Keys.DOWN)
                        sleep(0.1)
                        body_elem.send_keys(Keys.DOWN)
                        sleep(0.1)
                        body_elem.send_keys(Keys.DOWN)
                        
                else:
                    print ("skipping")
                    i+=1
                    
                    
                '''
                try:
                    like_el = likes[i]

                    if len(like_el)>0:
                        print ("Already liked")
                    else:
                        likes[i].click()
                        liked +=1                       
                except Exception as e:
                    #print (e)
                    pass
                '''
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
                        
                    #print ("i is",i)
                    discover_el = driver.find_elements_by_xpath('//*[@id="appsNav"]/h4')
                    discover_el_location = discover_el[0].location
                    location = likes[i].location
                    size = likes[i].size
                    body_elem.send_keys(Keys.DOWN)
                    if location['y'] > 20000: #will refresh page if scrolled too deep
                        print ("Feed too deep, refreshing")
                        driver.get("http://www.facebook.com") 
                        n = random.randint (200,1100)
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
                    sleeptime = random.randint(50,500)
                    print ("Things are bad. refreshing.\nSleeping for ",sleeptime)
                    tre=0
                    driver.get("http://www.facebook.com")
                    
                    sleep(sleeptime)
                    i = 0
    
    def ProfileLiker (self, driver, profileURL):
        
        driver.get(profileURL)

        print ("liking profile ",profileURL);
        
        sleep(2)
        ##############################################################################################
        try:
            profilePhoto = driver.find_element_by_xpath("//*[@class='photoContainer']/div/a/img").click()
            sleep(2)

            likeButton = driver.find_element_by_xpath('//*[@id="fbPhotoSnowliftFeedback"]/div/div[1]/div/div/div[2]/div/div/span[1]/div')
            try:
                like_el = likeButton.find_element_by_xpath("a[contains(@aria-pressed, 'false')]").click()
                print("liked")
            except Exception as err:
                print("already liked")
            

            sleep(1)

        except: 
            print ("couldng get to profile photo")

        body_elem = driver.find_element_by_tag_name('body')  
        body_elem.send_keys(Keys.ESCAPE)
        sleep(1)

        ##############################################################################################

        try:
            coverPicture = driver.find_element_by_xpath("//*[@id='fbProfileCover']/div/a").click()
            sleep(2)
            
            likeButton = driver.find_element_by_xpath('//*[@id="fbPhotoSnowliftFeedback"]/div/div[1]/div/div/div[2]/div/div/span[1]/div')
            try:
                like_el = likeButton.find_element_by_xpath("a[contains(@aria-pressed, 'false')]").click()
                print("liked")
            except Exception as err:
                print("already liked")
                

            sleep(1)
        except:
            print("couldnt get to cover picture")

        body_elem = driver.find_element_by_tag_name('body')  
        body_elem.send_keys(Keys.ESCAPE)
        sleep(1)

        ###############################################################################################
        
        try:
            body_elem = driver.find_element_by_tag_name('body')  
            body_elem.send_keys(Keys.PAGE_DOWN)
            sleep(1)

            try:
                like_el = driver.find_elements_by_xpath("//*[@class='commentable_item']/div/div/div/div/div[2]/div/div/span//a[contains(@aria-pressed, 'false')]")[0].click()
                print("liked")
            except Exception as err:
                print("already liked")
                print (err)
                sleep(3)

            sleep(1)
        except Exception as err:
            print (err)
            print("couldnt get to first post")
            sleep(3)

        
    def GetFriendList (self, driver):
        #driver.get("https://www.facebook.com/david.vendel")
        sleep(1)
        driver.find_elements_by_xpath("//*[@class='homeSideNav']//ul/li/a")[0].click()
        
        sleep(4)
        
        driver.find_element_by_xpath("//*[@id='fbTimelineHeadline']//div/ul/li[3]/a").click()

        last = -1
        for y in range (20):
            for i in range (35):
                body_elem = driver.find_element_by_tag_name('body')  
                body_elem.send_keys(Keys.PAGE_DOWN)
                sleep(1)
            linkElements = driver.find_elements_by_xpath("//*[@class='_698']/div/a")
            friendsUrls = []
            for linkEl in linkElements:
                urlLink = linkEl.get_attribute("href")
                sep = "?"
                cleanUrlLink = urlLink.split(sep,1)[0]
                friendsUrls.append(cleanUrlLink)

            print ("I have so far ",len(friendsUrls), " friends grabbed. Cycle ",y," out of max 20.")
            
            if (last == len(friendsUrls)):
                print ("No new friends. finishing grabbing")
                break
            else:
                print ("I want more")
                last = len(friendsUrls)
            file = open("./profiles/friends.txt","a+") 
            for friend in friendsUrls:
                file.write(friend)
                file.write("\n")
            file.close()
            print("friends saved in file friends.txt")
        return friendsUrls


print("*"*54)
print ("*"*11,"WELCOME AT FACEBOOK MASS LIKER","*"*11)
print("*"*54)

session = FacebookLiker()

driver = session.LoginToFb()
session.AutoLiker(driver)

friendsArray = ["https://www.facebook.com/fiama.canzani","https://www.facebook.com/luboszima", "https://www.facebook.com/amaiacanzani"]

#friendsArray = session.GetFriendList (driver)

for friend in friendsArray:
    session.ProfileLiker(driver, friend)
    file = open("./profiles/alreadyLiked.txt","w")
    file.write(friend)
    file.write("\n")
    file.close()
    sleep(1)

print ("Finished.")
sleep(3)
driver.close()
