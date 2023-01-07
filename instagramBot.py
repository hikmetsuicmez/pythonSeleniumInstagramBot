from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from userDetails import *
import pandas as pd
import matplotlib.pyplot as plt

class Instagram:
    def __init__(self,username,password,userFollower):
        self.username = username
        self.password = password
        self.userFollower = userFollower
        self.followersList = []
        self.followUpList = []
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.maximize_window()
        sleep(1.5)
        
    def logIn(self):
        self.browser.get("https://www.instagram.com/")
        sleep(2)

        # LOG IN  
        try:
            #fill in the username input
            userInput = self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
            userInput.click()
            sleep(0.4)
            userInput.send_keys(self.username)
            sleep(0.5)
        except:
            print("userInput XPATH ERROR")
        try:
            #fill in the password input
            passwordInput = self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
            passwordInput.click()
            sleep(0.4)
            passwordInput.send_keys(self.password) 
            sleep(0.7)
        except:
            print("passwordInput XPATH ERROR")
        try:
            #Log in by clicking the log in button
            logInButton = self.browser.find_element(By.CSS_SELECTOR, 'button._acap')
            logInButton.click()
            sleep(3.4)
            self.browser.find_element(By.TAG_NAME, 'button').click()
            sleep(3.4)
        except:
            print("logInButton XPATH ERROR")

    def followUsers(self):
        # The process of following the instagram account given by the user
        self.browser.get(f"https://www.instagram.com/{self.userFollower}/") 
        sleep(4)

        button = self.browser.find_element(By.TAG_NAME, "button")
        if button == "Follow" or button == "Takip Et":
            button.click()
            sleep(2)
        else:
            print("You are already following.")
        
    def getFollowers(self): 
        # The process of scraping the followers of the instagram account given by the user
        self.browser.get(f"https://www.instagram.com/{self.userFollower}/") 
        sleep(3)

        self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div').click()
        sleep(0.9)

        self.browser.find_element(By.CLASS_NAME, '_aano').click()
        sleep(0.9)

        parentElement = self.browser.find_element(By.CLASS_NAME, '_aano')
        firstFollowers = len(parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div'))
        print(firstFollowers)
        while True:
            # fBody = self.browser.find_element(By.XPATH, "//div[@role='dialog']")
            fBody = self.browser.find_element(By.CSS_SELECTOR, "._aano")
            self.browser.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);", fBody)
            sleep(3.9)
            # Calculate new scroll height and compare with last scroll height
            newFollowers = len(parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div'))
            if firstFollowers != newFollowers:
                firstFollowers = newFollowers
                #print(f"new : {newFollowers}")
            else:
                break
        
        followers = parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div')        
        for user in followers:
            name = user.find_element(By.CSS_SELECTOR, '._aacl').text
            self.followersList.append(name)
        
        #converting incoming data into dataframe table
        df = pd.DataFrame(self.followersList)
        df.to_csv(f'{self.userFollower}followers.csv', index=False,header=None)

    def getFollowUp(self):
        # The process of scraping the followUp of the instagram account given by the user
        self.browser.get(f"https://www.instagram.com/{self.userFollower}/") 
        sleep(3)
        self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div').click()
        
        sleep(3)
        parentElement = self.browser.find_element(By.CLASS_NAME, '_aano')
        firstFollowUp = len(parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div'))
        
        print(firstFollowUp)

        while True:
            sleep(1)
            self.browser.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);", parentElement)
            sleep(3.9)
            # Calculate new scroll height and compare with last scroll height
            newFollowUp = len(parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div'))
            
            if firstFollowUp != newFollowUp:
                firstFollowUp = newFollowUp
                #print(f"new : {newFollowUp}")
            else:
                break
        
        followUps = parentElement.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div')
        for user in followUps:
            name = user.find_element(By.CSS_SELECTOR ,'._aacl').text
            self.followUpList.append(name)

        #converting incoming data into dataframe table
        df = pd.DataFrame(self.followUpList)
        df.to_csv(f'{self.userFollower}followUps.csv', index=False,header=None)    

    def toCompare(self):
        #comparison
        notFollowBackList = []
        for followUp in self.followUpList:
            if followUp in self.followersList:
                print(f"{followUp} seni takip ediyor.")
            else:
                notFollowBackList.append(followUp)

        #converting incoming data into dataframe table
        df = pd.DataFrame(notFollowBackList)
        df.to_csv(f'{self.userFollower}notFollowBack.csv', index=False,header=None)
        sleep(2)

        # Graphing with matplotlib
        labels = ['Followers','Follow Up','NotFollowBack']
        followersLen = len(self.followersList)
        followUpLen = len(self.followUpList)
        notFollowBackLen = len(notFollowBackList)
        followLen = [followersLen,followUpLen,notFollowBackLen]
        colors = ['y','r','b']

        plt.pie(followLen,labels=labels,colors=colors,shadow=True,explode=(0.05,0.05,0.05),autopct='%1.1f%%')
        plt.show()
        plt.close()

        labels = ['Followers','Follow Up','NotFollowBack']
        followLen = [followersLen,followUpLen,notFollowBackLen]
        plt.bar(labels,followLen,color='green')
        plt.show()
        plt.close()

        # quit driver
        self.browser.quit()



instagram = Instagram(username,password,userFollower)

instagram.logIn()
sleep(3)
instagram.getFollowers()
sleep(3)
instagram.getFollowUp()
sleep(3)
instagram.toCompare()













    