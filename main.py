from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
CHROMEDRIVER_PATH = r'C:\Users\Rashid mohammad\Documents\PYTHON DEVELOPMENT\chromedriver_win32\chromedriver.exe'
CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
email = 'abc@gmail.com' #Your email here
pas = '********'#Your password here
id_password_field = 'passwordField'
id_usernameField_field = 'usernameField'
naukriLogin_url = 'https://www.naukri.com/nlogin/login'
xpath_profileName = '/html/body/div[2]/div/div/span/div/div/div/div[2]/div/div[2]/div[1]/div/a[1]/div[2]/div[1]'
xpath_resumeHeadline = '/html/body/div[2]/div/div/span/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[3]/span'
xpath_editbutton = '/html/body/div[2]/div/div/span/div/div/div/div/div/div[2]/div[3]/div[3]/div/div/div/div[1]/span[2]'
xpath_TextBox = '/html/body/div[5]/div[8]/div[2]/form/div[2]/div/textarea'
xpath_saveButton = '/html/body/div[5]/div[8]/div[2]/form/div[3]/div/button'
WaitTime = 30

#If you want whole process in run background then keep "Visiuals = False" else True
Visiuals = True

class NaukriProfileUpdate():

    def __init__(self):
        if Visiuals == False:
            WINDOW_SIZE = "1920,1080"
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
            chrome_options.binary_location = CHROME_PATH
            self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
            self.driver.maximize_window()
        time.sleep(2)
    def enterLoginDetails(self):
        driver = self.driver
        driver.get(url=naukriLogin_url)
        password_input_field = WebDriverWait(driver, WaitTime).until(EC.presence_of_element_located((By.ID,id_password_field)))
        username_input_field = WebDriverWait(driver, WaitTime).until(EC.presence_of_element_located((By.ID,id_usernameField_field)))

        # password_input_field = driver.find_element_by_id(id_password_field)
        # username_input_field = driver.find_element_by_id(id_usernameField_field)
        ActionChains(driver).move_to_element(username_input_field)
        username_input_field.clear()
        username_input_field.send_keys(email)
        ActionChains(driver).move_to_element(password_input_field)
        password_input_field.clear()
        password_input_field.send_keys(pas)
        password_input_field.send_keys(Keys.RETURN)

    def userHomePage(self):
        driver = self.driver
        time.sleep(3)
        #clickOn profile name to open profile home page
        profileName = WebDriverWait(driver, WaitTime).until(EC.presence_of_element_located((By.XPATH,xpath_profileName)))
        profileName.click()

    def UpdateHeadline(self):
        # click on resumeHeadline Option in homepage
        driver = self.driver
        resumeHeadlineOption = WebDriverWait(driver, WaitTime).until(
            EC.presence_of_element_located((By.XPATH, xpath_resumeHeadline)))
        resumeHeadlineOption.click()
        time.sleep(3)

        # click on edit button  to open edit box
        editButton = WebDriverWait(driver, WaitTime).until(EC.presence_of_element_located((By.XPATH, xpath_editbutton)))
        editButton.click()
        time.sleep(3)
        # Edit text field object

        self.updateProfile_textbox = WebDriverWait(driver, WaitTime).until(
            EC.presence_of_element_located((By.XPATH, xpath_TextBox)))

        # collect text from text field
        self.HeadLine_text = self.updateProfile_textbox.text
        print(f"Resume Headline updated with text : {self.HeadLine_text}")

        HeadLine_text = self.HeadLine_text
        text_length = len(HeadLine_text)
        if text_length == 250:
            HeadLine_text = HeadLine_text[:text_length-1]
        elif HeadLine_text[-1] == "." :
            HeadLine_text = HeadLine_text[:text_length-1]
        else:
            HeadLine_text = HeadLine_text + "."

        ActionChains(driver).move_to_element(self.updateProfile_textbox)
        self.updateProfile_textbox.clear()
        time.sleep(2)
        self.updateProfile_textbox.send_keys(HeadLine_text)
        time.sleep(2)
        self.driver.find_element_by_xpath(xpath_saveButton).click()
        time.sleep(2)


if __name__ == '__main__':
    naukri = NaukriProfileUpdate()
    naukri.enterLoginDetails()
    naukri.userHomePage()

    # Task scheduling After every 15mins UpdateHeadline() is called.
    schedule.every(5).minutes.do(naukri.UpdateHeadline)

    # Loop so that the scheduling task keeps on running all time.
    while True:
        schedule.run_pending()
        time.sleep(10)