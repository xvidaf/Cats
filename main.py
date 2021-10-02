import pandas as pandas
from selenium import webdriver # Could be used if i need to emulate web browsing ?
from bs4 import BeautifulSoup # Parsing html
import requests #Easy, juts gets the source
import openpyxl #Writing to excel
import pandas


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def getCatAttributes(url):
    # Requests
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
    catAttributesList = [soup.select('h1.border')[0].text.strip(),
        catAttributes[0].text.strip(),
        catAttributes[1].text.strip(),
        catAttributes[2].text.strip(),
        catAttributes[3].text.strip(),
        catAttributes[4].text.strip().replace("\n", " ").replace("\r", " ")]
    with file as f:
        for x in catAttributesList:
            f.write(str(x) + "###")
        f.write("\n")

def readCats():
    with open('cat.txt') as f:
        lines = f.readlines()
        for x in lines:
            print(x.strip().split("###"))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    catName = []  # List to store the name of the cat
    #Test Urls
    url1 = "http://stambok.sverak.se/Stambok/Visa/538"
    url2 = "http://stambok.sverak.se/Stambok/Visa/205375"
    url3 = "http://stambok.sverak.se/Stambok/Visa/204563"
    file = open("cat.txt", 'a')
    getCatAttributes(url3)
    readCats()
    file.close()


    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
