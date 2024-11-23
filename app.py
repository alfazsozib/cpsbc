from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re



def driver_connect():

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("--use-gl=swiftshader")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def search():
  
    df = pd.read_csv("MSP.csv")
    cols1 = df["Column1"].values
    cols2 = df["Column2"].values
    cols3 = df["Column3"].values
    cols4 = df["Column4"].values
    cols5 = df["Column5"].values
    cols6 = df["Column6"].values
    cols7 = df["Column7"].values
    cols8 = df["Column8"].values
    cols9 = df["Column9"].values
    cols10 = df["Column10"].values
    cols11 = df["Column11"].values
    cols12 = df["Column13"].values
    cols13 = df["Column13"].values

    for i in range(len(cols1))[2:]:
        col1 = cols1[i]
        col2 = cols2[i]
        col3 = cols3[i]
        col4 = cols4[i]
        col5 = cols5[i]
        col6 = cols6[i]
        col7 = cols7[i]
        col8 = cols8[i]
        col9 = cols9[i]
        col10 = cols10[i]
        col11 = cols11[i]
        col12 = cols12[i]
        col13 = cols13[i]

        nameSearch = col1
        firstName = ''
        lastName = ''
        if "," in nameSearch:
            try:
                firstName = nameSearch.split(",")[1].strip()
                lastName = nameSearch.split(",")[0].strip()
            except:
                lastName = nameSearch
                firstName = ''
        inptField = driver.find_element(By.XPATH ,'/html/body//div/main/div//div[2]/div[3]//form/div/div[1]//div[2]/div[1]/input')
        submtButton = driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/div/div/div[2]/div[3]/div/div/form/div/div[1]/div/div/div[2]/div[6]/input[2]')
        driver.execute_script("arguments[0].value = arguments[1];", inptField, nameSearch)

        # submtButton.click()
        inptField.send_keys(Keys.ENTER)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source,'html.parser')
        try:
            mainDiv = soup.find("div",{"class":'results-main-wrapper'}).find_all("div",{'class':'result-item'})
        except:
            continue
        for div in mainDiv:
            title = ''
            msp = ''
            registrationStatus = ''
            registrationClass = ''
            practiceType = ''
            address = ''
            phone = ''
            fax = ''
            streetAddress = ''
            city = ""
            province = ""
            postalCode = ""
            country = ""
            result = 1

            titleBox = div.find("div",{'class':'ps-contact__title'}).find_all('div')
            if titleBox:
                result = 0
            title = titleBox[0].text.replace("arrow_forward",'').strip()
            try:
                msp = titleBox[1].text.strip()
            except:
                msp = "No Result"

            print(title)
            print(msp)

            datas = div.find_all('div',{'class':'ps-contact__element'})
            for data in datas:
                if "Registration status:" in data.text:
                    registrationStatus = data.text.replace("Registration status:",'').strip()
                if "Registration class:" in data.text:
                    registrationClass  = data.text.replace("Registration class:","").strip()
                if "Practice type:" in data.text:
                    practiceType = data.text.replace("Practice type:","").strip()
                if "Address:" in data.text:
                    address = data.text.replace("Address:","").strip()
                    pattern = r"^(.*?),\s*(.*?),\s*([A-Z]{2}),\s*([A-Z0-9 ]{3,7}),\s*(.*)$"
                    match = re.match(pattern, address)
                    
                    if match:
                        streetAddress, city, province, postalCode, country = match.groups()
                if "Phone:" in data.text:
                    phone = data.text.replace("Phone:","").strip()
                if "Fax:" in data.text:
                    fax = data.text.replace("Fax:","").strip()

                
            temp = {
                "Name":title,
                "MSP":msp,
                "Registration status":registrationStatus,
                "Registration Class":registrationClass,
                "Practice Type":practiceType,
                "Street Address":streetAddress,
                "City":city,
                "Province":province,
                "Postal Code":postalCode,
                "Country":country,
                "Phone":phone,
                "Fax":fax,
                "Result Status":result
            }
            dataList.append(temp)
            pd.DataFrame(dataList).to_csv("Sample.csv",index=False)


def readData(driver):
    df = pd.read_csv("MSP.csv")
    cols1 = df["Column1"].values
    cols2 = df["Column2"].values
    cols3 = df["Column3"].values
    cols4 = df["Column4"].values
    cols5 = df["Column5"].values
    cols6 = df["Column6"].values
    cols7 = df["Column7"].values
    cols8 = df["Column8"].values
    cols9 = df["Column9"].values
    cols10 = df["Column10"].values
    cols11 = df["Column11"].values
    cols12 = df["Column13"].values
    cols13 = df["Column13"].values

    for i in range(len(cols1))[2:]:
        col1 = cols1[i]
        col2 = cols2[i]
        col3 = cols3[i]
        col4 = cols4[i]
        col5 = cols5[i]
        col6 = cols6[i]
        col7 = cols7[i]
        col8 = cols8[i]
        col9 = cols9[i]
        col10 = cols10[i]
        col11 = cols11[i]
        col12 = cols12[i]
        col13 = cols13[i]

        nameSearch = col1
        try:
            nameSearch = col1.split(",")[1].strip()
        except:
            try:
                nameSearch = col1.split(" ")[1]
                if len(nameSearch)<3:
                    nameSearch = col1
            except:
                nameSearch = col1
        
        # search(driver,nameSearch,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13)
         


# nameSearch,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13



if __name__=="__main__":
    driver = driver_connect()
    url = "https://www.cpsbc.ca/public/registrant-directory/"  
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.ID,'edit-ps-submit').click()
    time.sleep(10)
    dataList = []
    # readData(driver)
    search()