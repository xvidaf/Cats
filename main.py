import psycopg2
from bs4 import BeautifulSoup
import requests
import pandas
import os
import time
import re
from random import randint
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Function that retrieves a cat's entire pedigree
# Used as a first version for retrieval
def getCatAttributes(url, cats, newCats, baseUrl, listOfUrls, p):
    print(url)
    while (1):
        try:
            page = requests.get(url, timeout=45)
            break
        except requests.exceptions.Timeout:
            print("Timeout error! Retrying..")
            continue
    with open('site.html', 'wb+') as f:
        f.write(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Check if page is valid
    pageTitle = soup.find('title')
    if pageTitle.string == "Error":
        print("Invalid page!")
        return
    # Get a name and write it
    catName = soup.select('h1.border')[0].text.strip()
    catAttributes = soup.find_all(class_='display-field')
    # Get Father's Name
    try:
        father = soup.find('td', class_={re.compile('.*parent tree-row-odd CatNode.*'),
                                         re.compile('.*parent tree-row-odd UnknownNode.*')})
        # father = soup.find('td', {"class" : "parent tree-row-odd CatNode"})
        fatherLink = father.find('a', href=True)
        fatherName = ' '.join(father.text.splitlines()[-2].split())
        print(fatherLink['href'])
        print(fatherName)
    except:
        print("Macka nema Father")
        fatherName = ""
    # Get Mother's Name
    try:
        mother = soup.find('td', class_={re.compile('.*parent tree-row-even CatNode.*'),
                                         re.compile('.*parent tree-row-even UnknownNode.*')})
        # mother = soup.find('td', {"class" : "parent tree-row-even CatNode"})
        motherLink = mother.find('a', href=True)
        motherName = ' '.join(mother.text.splitlines()[-2].split())
        print(motherLink['href'])
        print(motherName)
    except:
        print("Macka nema Mother")
        motherName = ""
    # Get the attributes of the cat
    newRow = ({'Name': p.sub("", soup.select('h1.border')[0].text).strip(),
               'Breed': catAttributes[0].text.strip(),
               'Birth': catAttributes[1].text.strip(),
               'Gender': catAttributes[2].text.strip(),
               'Fur': catAttributes[3].text.strip(),
               'Number': catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
               'Title': ",".join(re.findall(p, soup.select('h1.border')[0].text.strip())),
               'Father': fatherName,
               'Mother': motherName,
               'From': "Sverak"})
    # Append the row to the list
    newCats.append(newRow)
    # print(newRow)
    # Recursively call the function on the parents, if they exist
    if fatherName != "":
        time.sleep(3)
        getCatAttributes(baseUrl + fatherLink['href'], cats, newCats, baseUrl, listOfUrls, p)
    if motherName != "":
        time.sleep(3)
        getCatAttributes(baseUrl + motherLink['href'], cats, newCats, baseUrl, listOfUrls, p)
    return


# Function to upload a cat file
# Requires credentials for GDrive first
# Mostly unused, credentials have to be renewed manually
def uploadFile(csvAmount):
    print("Uploading cat" + str(csvAmount))
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        gauth.Authorize()
        gauth.SaveCredentialsFile("mycreds.txt")
        drive = GoogleDrive(gauth)
        gfile = drive.CreateFile({'parents': [{'id': '1NpjeCaCg3_bPOb0g9tAO5TK6lgME36-M'}]})
        gfile.SetContentFile('cat' + str(csvAmount) + '.csv')
        gfile.Upload()  # Upload the file.
        print("Upload complete")
    except:
        print("Upload failed")
    # gauth.SaveCredentialsFile("mycreds.txt")

# Function to retrieve the attributes of a cat from the passed url
#
def getCatAttributesSingle(url, newCats, p):
    # Requests
    print(url)
    while (1):
        try:
            page = requests.get(url, timeout=45)
            break
        except requests.exceptions.Timeout:
            print("Timeout error! Retrying..")
            continue
    with open('site.html', 'wb+') as f:
        f.write(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Check if page is valid
    pageTitle = soup.find('title')
    if pageTitle.string == "Error":
        print("Invalid page!")
        return
    # Get a name and write it
    catName = soup.select('h1.border')[0].text.strip()
    catAttributes = soup.find_all(class_='display-field')
    # Get The father Name
    try:
        father = soup.find('td', class_={re.compile('.*parent tree-row-odd CatNode.*'),
                                         re.compile('.*parent tree-row-odd UnknownNode.*')})
        # father = soup.find('td', {"class" : "parent tree-row-odd CatNode"})
        fatherLink = father.find('a', href=True)
        fatherName = ' '.join(father.text.splitlines()[-2].split())
        print(fatherLink['href'])
        print(fatherName)
    except:
        print("Macka nema Father")
        fatherName = ""
    try:
        mother = soup.find('td', class_={re.compile('.*parent tree-row-even CatNode.*'),
                                         re.compile('.*parent tree-row-even UnknownNode.*')})
        # mother = soup.find('td', {"class" : "parent tree-row-even CatNode"})
        motherLink = mother.find('a', href=True)
        motherName = ' '.join(mother.text.splitlines()[-2].split())
        print(motherLink['href'])
        print(motherName)
    except:
        print("Macka nema Mother")
        motherName = ""
    newRow = ({'Name': p.sub("", soup.select('h1.border')[0].text).strip(),
               'Breed': catAttributes[0].text.strip(),
               'Birth': catAttributes[1].text.strip(),
               'Gender': catAttributes[2].text.strip(),
               'Fur': catAttributes[3].text.strip(),
               'Number': catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
               'Title': ",".join(re.findall(p, soup.select('h1.border')[0].text.strip())),
               'Father': fatherName,
               'Mother': motherName,
               'From': "Sverak"})
    newCats.append(newRow)
    # print(newRow)
    return

# Testing function, prints the attributes of the cat provided in url
def getCatAttributesSingleTest(url, p):
    try:
        page = requests.get(url, timeout=45)
    except:
        print("An error has occured, try again !")
        return
    soup = BeautifulSoup(page.text, 'html.parser')
    # Check if page is valid
    pageTitle = soup.find('title')
    if pageTitle.string == "Error":
        print("Invalid page!")
        return
    # Get a name and write it
    catName = soup.select('h1.border')[0].text.strip()
    catAttributes = soup.find_all(class_='display-field')
    # Get The father Name
    try:
        father = soup.find('td', class_={re.compile('.*parent tree-row-odd CatNode.*'),
                                         re.compile('.*parent tree-row-odd UnknownNode.*')})
        fatherName = ' '.join(father.text.splitlines()[-2].split())
    except:
        fatherName = ""
    try:
        mother = soup.find('td', class_={re.compile('.*parent tree-row-even CatNode.*'),
                                         re.compile('.*parent tree-row-even UnknownNode.*')})
        motherName = ' '.join(mother.text.splitlines()[-2].split())
    except:
        motherName = ""
    newRow = ({'Name': p.sub("", soup.select('h1.border')[0].text).strip(),
               'Breed': catAttributes[0].text.strip(),
               'Birth': catAttributes[1].text.strip(),
               'Gender': catAttributes[2].text.strip(),
               'Fur': catAttributes[3].text.strip(),
               'Number': catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
               'Title': ",".join(re.findall(p, soup.select('h1.border')[0].text.strip())),
               'Father': fatherName,
               'Mother': motherName,
               'From': "Sverak"})
    print("Name: " + newRow['Name'])
    print("Breed: " + newRow['Breed'])
    print("Birth date: " + newRow['Birth'])
    print("Gender: " + newRow['Gender'])
    print("Fur: " + newRow['Fur'])
    print("ID: " + newRow['Number'])
    print("Titles: " + newRow['Title'])
    print("Father: " + newRow['Father'])
    print("Mother: " + newRow['Mother'])
    print("From: " + newRow['From'])
    # print(newRow)
    return

# Helper function to check if the neccessary files exist
# csvAmount stores the amount of csv's we created
# counter stores where we left of in cat gathering
# badlinks stores links that encountered an error
def check_for_csv():
    if not os.path.exists("csvAmount.txt"):
        highestCSV = 0
    else:
        f = open("csvAmount.txt", 'r')
        highestCSV = int(f.read())
    while (1):
        fileName = "cat" + str(highestCSV + 1) + ".csv"
        if not os.path.exists(fileName):
            break
        highestCSV = highestCSV + 1
    if not os.path.exists("counter.txt"):
        f = open('counter.txt', 'w')
        f.write('%d' % 1)
    if not os.path.exists("badlinks.txt"):
        f = open('badlinks.txt', 'w')
    return highestCSV


def getCounter():
    f = open('counter.txt', 'r')
    return int(f.read())


def read_cats():
    if os.path.exists("cat.csv"):
        print(pandas.read_csv("cat.csv", index_col=0))


def incrementCounter(counter1):
    return counter1 + 1


def incrementPage(baseUrl, counter1):
    return str(baseUrl + "/Stambok/Visa/" + str(counter1))


def writeCounter(counter):
    f = open('counter.txt', 'w')
    f.write('%d' % int(counter))
    f.close()

# Helper function to check the total amount of cats written on the website
def checkTotalCats():
    mainPage = requests.get("https://stambok.sverak.se/")
    soup = BeautifulSoup(mainPage.text, 'html.parser')
    catText = soup.find("div", {"class": "findUsWelcome"})
    catNumber = catText.find('b').text
    catNumber = catNumber.replace(u'\xa0', '')
    return (int(catNumber))


def create_new_csv(maxCSV):
    df = pandas.DataFrame(
        columns=['Name', 'Breed', 'Birth', 'Gender', 'Fur', 'Number', 'Title', 'Father', 'Mother', 'From'])
    df.to_csv('cat' + str(maxCSV + 1) + '.csv', mode='w')

# Helper function to change the order of colums in csv, sometimes they are random
def changeCSVOrder():
    cols = ["Name", "Breed", "Birth", "Gender", "Fur", "Number", "Title", "Father", "Mother", "From"]
    highestCSV = 0
    while (1):
        fileName = "Cats\cat" + str(highestCSV + 1) + ".csv"
        if not os.path.exists(fileName):
            break
        print("Reordering" + str(highestCSV + 1))
        toChange = pandas.read_csv(fileName, index_col=0, encoding="utf-8")
        toChange = toChange[cols]
        toChange.to_csv('Reordered\cat' + str(highestCSV + 1) + ".csv", mode='w', encoding="utf-8")
        highestCSV = highestCSV + 1

def uploadCatsToDatabase(path="D:\Reordered"):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="catDatabase",
            user="postgres",
            password="postgres",
            port="5433")
        cur = conn.cursor()
        highestCSV = 0
        while (1):
            fileName = path + "\cat" + str(highestCSV + 1) + ".csv"
            #if not os.path.exists(fileName) or highestCSV == 10:
            if not os.path.exists(fileName):
                break
            print("Uploading" + str(highestCSV + 1))
            cur.execute(
                "COPY catapp_cat(internalid,name,breed,birth,gender,fur,number,title,father,mother,site) FROM " + "'" + path + "\cat" + str(highestCSV + 1) + ".csv'" + " ENCODING 'UTF8' DELIMITER ',' CSV HEADER;")
            conn.commit()
            highestCSV = highestCSV + 1

        cur.close()
    except:
        print("Error")
        raise


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Test Urls
    baseUrl = "https://stambok.sverak.se"
    #url1 = "http://stambok.sverak.se/Stambok/Visa/538"
    #url2 = "http://stambok.sverak.se/Stambok/Visa/205375"
    #url3 = "http://stambok.sverak.se/Stambok/Visa/204563"
    #url4 = "http://stambok.sverak.se/Stambok/Visa/90763"
    #urlBad = "http://stambok.sverak.se/Stambok/Visa/1"
    # file = open("cat.txt", 'a', encoding="utf-8")
    try:
        csvAmount = check_for_csv()
    except:
        print("Cannot get cat count, site down ?")
    # We read cat.csv to ge
    cats = pandas.read_csv("cat.csv", index_col=0)
    counter = getCounter()
    newCats = []
    listOfUrls = []
    # Known titles of cats, used to check for them in the name, and remove them
    listOfTitles = ["CH", "P", "IC", "IP", "GIC", "GIP", "EC", "EP", "SC", "SP", "JW", "DSM", "DVM", "NW", "WW", "RW",
                    "Int.", "Ch", "Cham", "RW", "CH", "GCH", "DGCH", "TGCH", "QGCH", ","]
    p = re.compile(r'\b(?:%s)\b' % '|'.join(listOfTitles))  # For regex searching
    # Find the total amount of cats
    totalCats = checkTotalCats()
    print("Welcome to the cat retrieval program")
    print("The site currently has " + str(totalCats) + " total cats.")
    print("We currently have " + str(csvAmount) + " csv files.")
    print("Current counter is " + str(counter))
    # print("Choose wisely")
    print("Option 1: Get a Single Cat")
    print("Option 2: Get a Cat's Pedigree")
    print("Option 3: Continue from counter")
    print("Option 4: Reorder Downloaded Cats")
    print("Option 5: Upload cats to the database")
    input1 = input()
    if (input1 == "1"):
        print("Input Link:")
        catLink = input()
        getCatAttributesSingleTest(catLink, p)
    elif (input1 == "2"):
        print("Input Link:")
        catLink = input()
        try:
            getCatAttributes(catLink, cats, newCats, baseUrl, listOfUrls, p)
            df = pandas.DataFrame(
                columns=['Name', 'Breed', 'Birth', 'Gender', 'Fur', 'Number', 'Title', 'Father', 'Mother', 'From'])
            df.to_csv('pedigree' + '.csv', mode='w')
            newCatsFrame = pandas.DataFrame(newCats)
            cats = cats.append(newCatsFrame, ignore_index=True)
            cats.to_csv('pedigree' + ".csv", mode='w', encoding="utf-8")
        except:
            print("Error")
            raise
    elif (input1 == "3"):
        print("Taking cats from counter until stopped")
        try:
            print("Creating new CSV")
            create_new_csv(csvAmount)
            csvAmount = csvAmount + 1
            while (counter in range(totalCats + 50000)):
                cats = pandas.read_csv('cat' + str(csvAmount) + '.csv', index_col=0)
                url = incrementPage(baseUrl, counter)
                counter = incrementCounter(counter)
                time.sleep(randint(2, 5))
                try:
                    getCatAttributesSingle(url, newCats, p)
                except requests.exceptions.ConnectionError:
                    print("Bad link ?, saving it to bad links")
                    badlinks = open('badlinks.txt', 'a')
                    badlinks.write(url + "\n")
                    badlinks.close()
                if counter % 100 == 0:
                    print("Saving cats")
                    newCatsFrame = pandas.DataFrame(newCats)
                    cats = cats.append(newCatsFrame, ignore_index=True)
                    cats.to_csv('cat' + str(csvAmount) + ".csv", mode='w', encoding="utf-8")
                    try:
                        cats = pandas.read_csv('cat' + str(csvAmount) + '.csv', index_col=0)
                    except:
                        print("Failed reading the csv(linux error?), creating new CSV")
                        uploadFile(csvAmount)
                        print("Creating new CSV")
                        create_new_csv(csvAmount)
                        csvAmount = csvAmount + 1
                        cats = pandas.read_csv('cat' + str(csvAmount) + '.csv', index_col=0)
                    newCats.clear()
                    writeCounter(counter)
                    if counter % 1000 == 0:
                        uploadFile(csvAmount)
                        print("Creating new CSV")
                        create_new_csv(csvAmount)
                        csvAmount = csvAmount + 1
                        cats = pandas.read_csv('cat' + str(csvAmount) + '.csv', index_col=0)
                        time.sleep(randint(10, 20))
                        if counter % 10000 == 0:
                            time.sleep(randint(100, 200))
                    time.sleep(randint(10, 20))
        except Exception as e:
            print("Error during retrieval, saving changes")
            print(e)
            raise
        newCatsFrame = pandas.DataFrame(newCats)
        # print(newCats)
        cats = cats.append(newCatsFrame, ignore_index=True)
        cats.to_csv('cat.csv', mode='w', encoding="utf-8")
        # read_cats()
        # file.close()
        writeCounter(counter)
    elif (input1 == "4"):
        changeCSVOrder()
    elif (input1 == "5"):
        print("Enter a path to the cat .csv files.")
        print("Example path 'D:\Reordered\cat")
        input2 = input()
        uploadCatsToDatabase(input2)
    else:
        print("Invalid Value")

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
