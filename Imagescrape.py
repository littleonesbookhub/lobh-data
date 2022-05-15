import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import quote

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


df = df.reset_index() # make sure indexes pair with number of rows
for index, row in df.iterrows():
    # search on internet based on title, convert it into lowercase
    # extract author name and store it
    title = row['Title'].lower()
    print(title)
    search_url = 'https://www.google.com/search?tbm=bks&q=' + urllib.parse.quote_plus(title)
    #search_url = 'https://openlibrary.org/search?q=hungry+caterpillar&mode=everything'
    #print(search_url)
    page = requests.get(search_url,headers={"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"} )
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup)
   
    #test code
    f = open("index.html", "w")
    f.write(str(soup))
    f.close()
    #exit()

    #Lists all the books with class ul(openlibrabry)
    #list_books = soup.find_all("ul", {"class": "list-books"})
    #if list_books:
        #first_book = list_books[0]
        #anchors = first_book.find_all(attrs={"itemprop": "url"})
        #if len(anchors) > 1:
            #print(anchors[1].text)
        
    #Lists all the books from Google
    text_encoded = quote(title)
    #print(text_encoded)
    parent = soup.find("div",attrs={"data-async-context": "query:"+text_encoded})
    #print(list_allbooks)
     
    #get the author
    children = parent.findChildren(recursive=False)
    print(len(children))
    for child in children:
        span = child.select("a > span") 
        print(span)
        if span: 
            print(span[0].text)
        
        #get image
        #thumbnail = child.find("img")
        #print(len(thumbnail))
        #print(thumbnail)

        # get description
        description= child.select("span > span")
        print(description[0].text)
        user_input = input("Press any key to continue ...")
        #user_input = input("Press Y or N if the title and author match")
        #if(input=="Y"):



        
    
    
    
