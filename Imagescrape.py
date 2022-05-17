import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse
import openpyxl
from urllib.parse import quote

 #Lists all the books with class ul(openlibrabry)
    #list_books = soup.find_all("ul", {"class": "list-books"})
    #if list_books:
        #first_book = list_books[0]
        #anchors = first_book.find_all(attrs={"itemprop": "url"})
        #if len(anchors) > 1:
            #print(anchors[1].text)

#open the website

#URL= 'https://openlibrary.org/'
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")


#find the search bar
#search_bar= soup.find(placeholder="Search")
#print(search_bar.prettify())

#get image
        #thumbnail = child.find("img")
        #print(len(thumbnail))
        #print(thumbnail)


code_restart= "true"
#read the title and author from excel
data = pd.read_excel(r'LBH.xlsx')
df= pd.DataFrame(data,columns=['Title'])
df = df.reset_index() # make sure indexes pair with number of rows
for index, row in df.iterrows():
        # Search title from website 
        title = row['Title'].lower()
        print(title)
        search_url = 'https://www.google.com/search?tbm=bks&q=' + urllib.parse.quote_plus(title)
        page = requests.get(search_url,headers={"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"} )
        soup = BeautifulSoup(page.content, "html.parser")
        
        #code writes to index.html
        f = open("index.html", "w")
        f.write(str(soup))
        f.close()
        
        #Lists all the books from Google
        text_encoded = quote(title)
        parent = soup.find("div",attrs={"data-async-context": "query:"+text_encoded})
        
        # Get the author
        titlelist=[]
        children = parent.findChildren(recursive=False)
        for child in children:
            span = child.select("a > span") 
            print(span)
            if span: 
                print(span[0].text)
                titlelist.append(span[0].text)
        print(titlelist)

        
        # Get the description
            description= child.select("span > span")
            print(description[0].text)
            userinput= input("Press any key to continue")
       #Checking if the author and descrition match for the title
        

            

            
            