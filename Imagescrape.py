import pandas as pd
from bs4 import BeautifulSoup
import requests
import pywhatkit

#open the website

URL= 'https://openlibrary.org/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


#find the search bar
search_bar= soup.find(placeholder="Search")
print(search_bar.prettify())


#read the title and author from excel
data = pd.read_excel(r'/Users/nishel/Desktop/LBH.py/LBH.xlsx')
df= pd.DataFrame(data,columns=['Title'])
getTitle=df.at[2,'Title']
print(getTitle)
