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
import csv
import openpyxl
import numpy as np


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

    for i in range(len(cols1))[2:][start_page:end_page+1]:
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

            parts = nameSearch.split(',')
            lastName = parts[0].strip()
            first_and_middle = parts[1].strip().split()
            firstName = first_and_middle[0]

        
        lastNameInput = driver.find_element(By.XPATH ,'/html/body//div/main/div//div[2]/div[3]//form/div/div[1]//div[2]/div[1]/input')
        submtButton = driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/div/div/div[2]/div[3]/div/div/form/div/div[1]/div/div/div[2]/div[6]/input[2]')
        driver.execute_script("arguments[0].value = arguments[1];", lastNameInput, lastName)

        firstNameInput = driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/div/div/div[2]/div[3]/div/div/form/div/div[1]/div/div/div[2]/div[2]/input')
        # submtButton.click()
        driver.execute_script("arguments[0].value = arguments[1];", firstNameInput, firstName)
        firstNameInput.send_keys(Keys.ENTER)
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
                msp = titleBox[1].text.strip().replace("MSP  ",'')
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
                    if "-" in practiceType:
                        practiceType = practiceType.split("-")[1].strip()

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
                "Column 1":col1,
                "Column 2":col2,
                "Column 3":col3,
                "Column 4":col4,
                "Column 5":col5,
                "Column 6":col6,
                "Column 7":col7,
                "Column 8":col8,
                "Column 9":col9,
                "Column 10":col10,
                "Column 11":col11,
                "Column 12":col12,
                "Column 13":col13,
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


def readDataFirst():
    file_path = "Merged_Data.csv"
    df = pd.read_csv(file_path)

    # Initialize a list to store the result
    new_data = []

    # Extract values from each column (excluding Column 13)
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
    cols12 = df["Column12"].values

    # Debugging: Print first few rows to check if the data is loaded correctly
    print("First few rows of the data:")
    print(df.head())

    # Iterate through the rows, checking for consecutive matches in Column 1
    for i in range(1, len(cols1)):
        # Check if the current row matches the previous one in Column 1
        if cols1[i].strip() == cols1[i-1].strip():
            # Debugging: Print the current and previous rows that match
            print(f"Match found between rows {i-1} and {i}:")
            print(f"Row {i-1} - {cols1[i-1]}, Row {i} - {cols1[i]}")

            # Extract the data from the current row (excluding Column 13)
            current_row = [
                cols1[i],  # Name from Column 1
                cols2[i], cols3[i], cols4[i], cols5[i], cols6[i], cols7[i],
                cols8[i], cols9[i], cols10[i], cols11[i], cols12[i]
            ]
            
            # Extract the previous row's data (excluding Column 13)
            previous_row = [
                cols2[i-1], cols3[i-1], cols4[i-1], cols5[i-1], cols6[i-1], cols7[i-1],
                cols8[i-1], cols9[i-1], cols10[i-1], cols11[i-1], cols12[i-1]
            ]
            
            # Fill the empty columns in the current row with the previous row's data
            for j in range(1, 12):  # Columns 2 to 12 are indexed from 1 to 11 (ignoring Column 13)
                if pd.isna(current_row[j]):  # Check if the current row's column is empty (NaN)
                    current_row[j] = previous_row[j-1]  # Fill with the previous row's corresponding data

            # Now check if there are extra values in the previous row that need to be appended
            # Calculate how many extra values we need to append (values beyond Column 12)
            extra_values = previous_row[11:]  # Values beyond Column 12
            
            # If there are more values, append them as new columns
            if extra_values:
                current_row.extend(extra_values)

            # Append the current row (with previous row data inserted) to the new_data list
            new_data.append(current_row)

    # Debugging: Check how many rows have been added to new_data
    print(f"Number of rows with matching data: {len(new_data)}")

    # Convert the new data list into a DataFrame
    if new_data:  # Check if there is any data to save
        # Determine the number of columns needed
        num_columns = 12 + len(extra_values)  # 12 original columns (ignoring Column 13) + extra columns

        # Create column names dynamically (if new columns are added)
        column_names = ['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6', 'Column 7', 'Column 8', 'Column 9', 'Column 10', 'Column 11', 'Column 12']
        if extra_values:
            extra_column_names = [f'Column {i}' for i in range(14, 14 + len(extra_values))]
            column_names.extend(extra_column_names)
        
        # Create DataFrame from the new_data list
        new_df = pd.DataFrame(new_data, columns=column_names)
        
        # Save the new dataframe to a CSV file
        new_df.to_csv('output_file.csv', index=False)
        print("Data has been saved to 'output_file.csv'.")
    else:
        print("No matching rows found. CSV was not created.")
    
def readDataSecond():
    output_file_path = 'output_file.csv'  # This is the first file
    sample_file_path = "Merged_Data.csv"  # This is the second file

    # Read both CSV files into DataFrames
    df_output = pd.read_csv(output_file_path)
    df_merged = pd.read_csv(sample_file_path)

    # Extract names (assuming names are in Column 1 in both files)
    output_names = df_output["Column 1"].values
    merged_names = df_merged["Column1"].values  # Column1 is the name column in Merged_Data

    # Strip spaces from both the output names and merged names
    output_names = [name.strip() for name in output_names]
    merged_names = [name.strip() for name in merged_names]

    # Convert output_names to a set for faster comparison
    output_names_set = set(output_names)

    # Initialize a list to store the non-matching rows from Merged_Data
    non_matching_rows = []

    # Loop through each row in the merged DataFrame and check if the name exists in output_names_set
    for i in range(len(merged_names)):
        if merged_names[i] not in output_names_set:
            # If the name doesn't exist in output_names, append the entire row
            row_data = df_merged.iloc[i]
            non_matching_rows.append(row_data)

    # If we found non-matching rows, save them to a new CSV
    if non_matching_rows:
        # Convert the list of rows to a DataFrame
        non_matching_df = pd.DataFrame(non_matching_rows)

        # Save to a new CSV file
        non_matching_df.to_csv("Non_Matching_Rows.csv", index=False)
        print("Non-matching rows saved to 'Non_Matching_Rows.csv'.")
    else:
        print("No non-matching rows found.")
            
    
if __name__=="__main__":
    start_page = int(input("Enter starting number and press enter: "))
    end_page = int(input("Enter End Number and press enter: "))
    driver = driver_connect()
    url = "https://www.cpsbc.ca/public/registrant-directory/"  
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.ID,'edit-ps-submit').click()
    time.sleep(10)
    dataList = []
    # readDataFirst()
    # readDataSecond()
    search()

