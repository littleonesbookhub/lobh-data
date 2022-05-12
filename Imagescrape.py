import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse

#open the website

#URL= 'https://openlibrary.org/'
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")


#find the search bar
#search_bar= soup.find(placeholder="Search")
#print(search_bar.prettify())


#read the title and author from excel
data = pd.read_excel(r'LBH.xlsx')
df= pd.DataFrame(data,columns=['Title'])
#getTitle=df.at[2,'Title']
#print(getTitle)

df = df.reset_index()  # make sure indexes pair with number of rows
for index, row in df.iterrows():
    # search on internet based on title
    # extract author name and store it
    title = row['Title']
    print(title)
    search_url = 'https://www.google.com/search?tbm=bks&q=' + urllib.parse.quote_plus(title)
    print(search_url)
    page = requests.get(search_url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup)
    #list_books = soup.find_all("ul", {"class": "list-books"})
    #if list_books:
    #    first_book = list_books[0]
    #    anchors = first_book.find_all(attrs={"itemprop": "url"})
    #    if len(anchors) > 1:
    #        print(anchors[1].text)
    user_input = input("Press any key to continue ...")
    
