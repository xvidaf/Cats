import pandas as pandas
from selenium import webdriver # Could be used if i need to emulate web browsing ?
from bs4 import BeautifulSoup # Parsing html
import requests #Easy, juts gets the source
import openpyxl #Writing to excel
import pandas
import os
import time
import re

def getCatAttributes(url,cats, newCats, baseUrl, listOfUrls):
    # Requests
    print(url)
    if url in listOfUrls:
        print("Same url found!")
        return
    else:
        listOfUrls.append(url)
    page = requests.get(url)
    with open('site.html', 'wb+') as f:
        f.write(page.content)
    # Solenium
    # driver = webdriver.Chrome("chromedriver.exe")
    # driver.get("http://stambok.sverak.se/Stambok/Visa/538")
    # page = driver.page_source
    soup = BeautifulSoup(page.text, 'html.parser')
    # file1 = open("cat.txt", "a")
    # file1.write(page)
    # print(soup.prettify())
    #Helper writer
    #catDescription = soup.find_all(class_='description-cat')
    #with open('catDescription.txt', 'w+') as f:
        #for x in catDescription:
            #f.write(x.text)

    # Get a name and write it
    catName = soup.select('h1.border')[0].text.strip()
    catAttributes = soup.find_all(class_='display-field')
    """
    catBreed = catAttributes[0].text.strip()
    catAge = catAttributes[1].text.strip()
    catGender = catAttributes[2].text.strip()
    catFur = catAttributes[3].text.strip()
    catNumber = catAttributes[4].text.strip()
    """
    """
    catAttributesList = [soup.select('h1.border')[0].text.strip(),
        catAttributes[0].text.strip(),
        catAttributes[1].text.strip(),
        catAttributes[2].text.strip(),
        catAttributes[3].text.strip(),
        catAttributes[4].text.strip().replace("\n", " ").replace("\r", " ")]
    """
    # Get The father Name
    father = soup.find('td', class_={re.compile('.*parent tree-row-odd CatNode.*'), re.compile('.*parent tree-row-odd UnknownNode.*')})
    mother = soup.find('td', class_={re.compile('.*parent tree-row-even CatNode.*'),re.compile('.*parent tree-row-even UnknownNode.*')})
    fatherLink = father.find('a', href=True)
    motherLink = mother.find('a', href=True)
    fatherName = ' '.join(father.text.splitlines()[-2].split())  # Split the id from the string and remove tab
    motherName = ' '.join(mother.text.splitlines()[-2].split())  # Split the id from the string and remove tab
    try:
        print(fatherLink['href'])
        print(fatherName)
    except:
        print("Macka nema Father")
        fatherName = ""
    try:
        print(motherLink['href'])
        print(motherName)
    except:
        print("Macka nema Mother")
        motherName = ""
    newRow = ({'Name' : soup.select('h1.border')[0].text.strip(),
        'Breed' : catAttributes[0].text.strip(),
        'Birth' : catAttributes[1].text.strip(),
        'Gender' : catAttributes[2].text.strip(),
        'Fur' : catAttributes[3].text.strip(),
        'Number' : catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
        'Father' : fatherName,
        'Mother' : motherName})
    newCats.append(newRow)
    #print(newRow)
    if fatherName != "":
        time.sleep(3)
        getCatAttributes(baseUrl + fatherLink['href'], cats, newCats, baseUrl, listOfUrls)
    if motherName != "":
        time.sleep(3)
        getCatAttributes(baseUrl + motherLink['href'], cats, newCats, baseUrl, listOfUrls)
    return

def getCatAttributesSingle(url,cats, newCats, baseUrl, listOfUrls):
    # Requests
    print(url)
    if url in listOfUrls:
        print("Same url found!")
        return
    else:
        listOfUrls.append(url)
    page = requests.get(url)
    with open('site.html', 'wb+') as f:
        f.write(page.content)

    soup = BeautifulSoup(page.text, 'html.parser')
    #Check if page is valid
    pageTitle = soup.find('title')
    if pageTitle.string == "Error":
        print("Invalid page!")
        return
    # Get a name and write it
    catName = soup.select('h1.border')[0].text.strip()
    catAttributes = soup.find_all(class_='display-field')
    # Get The father Name
    father = soup.find('td', class_={re.compile('.*parent tree-row-odd CatNode.*'), re.compile('.*parent tree-row-odd UnknownNode.*')})
    mother = soup.find('td', class_={re.compile('.*parent tree-row-even CatNode.*'),re.compile('.*parent tree-row-even UnknownNode.*')})
    fatherLink = father.find('a', href=True)
    motherLink = mother.find('a', href=True)
    fatherName = ' '.join(father.text.splitlines()[-2].split())  # Split the id from the string and remove tab
    motherName = ' '.join(mother.text.splitlines()[-2].split())  # Split the id from the string and remove tab
    try:
        print(fatherLink['href'])
        print(fatherName)
    except:
        print("Macka nema Father")
        fatherName = ""
    try:
        print(motherLink['href'])
        print(motherName)
    except:
        print("Macka nema Mother")
        motherName = ""
    newRow = ({'Name' : soup.select('h1.border')[0].text.strip(),
        'Breed' : catAttributes[0].text.strip(),
        'Birth' : catAttributes[1].text.strip(),
        'Gender' : catAttributes[2].text.strip(),
        'Fur' : catAttributes[3].text.strip(),
        'Number' : catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
        'Father' : fatherName,
        'Mother' : motherName})
    newCats.append(newRow)
    #print(newRow)
    return

def check_for_csv():
    if not os.path.exists("cat.csv"):
        df = pandas.DataFrame(columns=['Name', 'Breed', 'Birth', 'Gender', 'Fur', 'Number', 'Father', 'Mother'])
        df.to_csv('cat.csv', mode='w')
    if not os.path.exists("counter.txt"):
        f = open('counter.txt', 'w')
        f.write('%d' % 0)

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
    f.write('%d' % int(counter - 1))
    f.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #TODO CHECK IF CAT IS ALREADY IN
    #Test Urls
    baseUrl = "http://stambok.sverak.se"
    url1 = "http://stambok.sverak.se/Stambok/Visa/538"
    url2 = "http://stambok.sverak.se/Stambok/Visa/205375"
    url3 = "http://stambok.sverak.se/Stambok/Visa/204563"
    url4 = "http://stambok.sverak.se/Stambok/Visa/90763"
    urlBad = "http://stambok.sverak.se/Stambok/Visa/1"
    file = open("cat.txt", 'a', encoding="utf-8")
    check_for_csv()
    cats = pandas.read_csv("cat.csv", index_col=0)
    counter = getCounter()
    newCats = []
    listOfUrls = []
    print("Welcome to the cat retrieval program")
    print("Current counter is " + str(counter))
    print("Choose wisely")
    print("Option 1: Input a Link")
    print("Option 2: Continue from counter")
    input1 = input()
    if(input1 == "1" or input1 == "2"):
        print("Choose retrieval type")
        print("Option 1: Get only the cat in the link")
        print("Option 2: Get the entire pedigree of the cat")
        input2 = input()
        if (input2 == "1" or input2 == "2"):
            print("How many cats do we take ?")
            amount = input()
            if(input1 == "2" and input2 == "1"):
                for x in range(int(amount)):
                    url = incrementPage(baseUrl, counter)
                    counter = incrementCounter(counter)
                    time.sleep(3)
                    getCatAttributesSingle(url, cats, newCats, baseUrl, listOfUrls)
                newCats = pandas.DataFrame(newCats)
                # print(newCats)
                cats = cats.append(newCats, ignore_index=True)
                cats.to_csv('cat.csv', mode='w', encoding="utf-8")
                # read_cats()
                file.close()
                writeCounter(counter)
            elif (input1 == "2" or input2 == "2"):
                for x in range(int(amount)):
                    url = incrementPage(baseUrl, counter)
                    counter = incrementCounter(counter)
                    time.sleep(3)
                    getCatAttributes(url, cats, newCats, baseUrl, listOfUrls)
                newCats = pandas.DataFrame(newCats)
                # print(newCats)
                cats = cats.append(newCats, ignore_index=True)
                cats.to_csv('cat.csv', mode='w', encoding="utf-8")
                # read_cats()
                file.close()
                writeCounter(counter)
            else:
                print("Not implemented yet, stay tuned")

        else:
            print("Invalid Value")
    else:
        print("Invalid Value")


    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
