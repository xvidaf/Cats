import pandas as pandas
from selenium import webdriver # Could be used if i need to emulate web browsing ?
from bs4 import BeautifulSoup # Parsing html
import requests #Easy, juts gets the source
import openpyxl #Writing to excel
import pandas
import os
import time

def getCatAttributes(url,cats):
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
    """
    catAttributesList = [soup.select('h1.border')[0].text.strip(),
        catAttributes[0].text.strip(),
        catAttributes[1].text.strip(),
        catAttributes[2].text.strip(),
        catAttributes[3].text.strip(),
        catAttributes[4].text.strip().replace("\n", " ").replace("\r", " ")]
    """
    # Get The father Name
    father = soup.find('td', class_={"parent tree-row-odd CatNode", "parent tree-row-odd UnknownNode"})
    mother = soup.find('td', class_={"parent tree-row-even CatNode", "parent tree-row-even UnknownNode"})
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
    newRow = pandas.Series({'Name' : soup.select('h1.border')[0].text.strip(),
        'Breed' : catAttributes[0].text.strip(),
        'Birth' : catAttributes[1].text.strip(),
        'Gender' : catAttributes[2].text.strip(),
        'Fur' : catAttributes[3].text.strip(),
        'Number' : catAttributes[4].text.strip().replace("\n", " ").replace("\r", " "),
        'Father' : fatherName,
        'Mother' : motherName})
    print(newRow)
    return newRow

def check_for_csv():
    if not os.path.exists("cat.csv"):
        df = pandas.DataFrame(columns=['Name', 'Breed', 'Birth', 'Gender', 'Fur', 'Number', 'Father', 'Mother'])
        df.to_csv('cat.csv', mode='w')

def read_cats():
    if os.path.exists("cat.csv"):
       print(pandas.read_csv("cat.csv", index_col=0))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #TODO ENCODING FOR SWEDISH ?
    #TODO ADD ALL CATS TROUGH PARENTS
    #TODO CHECK IF CAT IS ALREADY IN
    #Test Urls
    baseUrl = "http://stambok.sverak.se"
    url1 = "http://stambok.sverak.se/Stambok/Visa/538"
    url2 = "http://stambok.sverak.se/Stambok/Visa/205375"
    url3 = "http://stambok.sverak.se/Stambok/Visa/204563"
    url4 = "http://stambok.sverak.se/Stambok/Visa/204552"
    file = open("cat.txt", 'a')
    check_for_csv()
    cats = pandas.read_csv("cat.csv", index_col=0)
    #print(cats)
    cats = cats.append(getCatAttributes(url3, cats), ignore_index=True)
    cats.to_csv('cat.csv', mode='w')
    read_cats()
    file.close()


    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
