import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import quote
import re

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
header = ['Title', 'Author', 'Description']

def get_book_metadata(parent, title):
    booklist=[]
    children = parent.findChildren(recursive=False)
    for child in children:
        authorname = ""
        descriptiontext = ""
        span = child.select("a > span") 
    
        #get the author
        if span: 
            #print(span[0].text)
            authorname=span[0].text
        
        # get description
    
        description= child.select("span > span")
        #print(description[0].text)
        if description: 
            descriptiontext = description[0].text
        booklist.append({
            "author": authorname,
            "description": descriptiontext
            })
    [print(i+1, x) for i, x in enumerate(booklist)]   #list comprehension
    
    #Entering the user's choice
    bookrange = range(1,len(booklist)+1)
    print("The list is complete..Please choose your option.Input 11 to skip", list(bookrange))
    userchoicedesc= int(input("Enter your choice"))
    if(userchoicedesc==11):
        data = [title, "None", "None"]
        reader=csv.reader(data,delimiter=':', quoting=csv.QUOTE_NONE)
        return reader

    if(userchoicedesc in bookrange):
        print(booklist[userchoicedesc-1])
    
    

    else:
        print("Out of range")
# converting into CSV files
    data = [title, booklist[userchoicedesc-1]["author"], booklist[userchoicedesc-1]["description"]]
    reader=csv.reader(data,delimiter=':', quoting=csv.QUOTE_NONE)
    return reader

with open('data.csv', 'w', encoding='UTF8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)

    start_index = int(input("Enter the start index: "))

    for index, row in df.iterrows():
        if index < (start_index-1):
            continue
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
        html_file = open("index.html", "w")
        html_file.write(str(soup))
        html_file.close()
        #exit()

        #Lists all the books with class ul(openlibrabry)
        #list_books = soup.find_all("ul", {"class": "list-books"})
        #if list_books:
            #first_book = list_books[0]
            #anchors = first_book.find_all(attrs={"itemprop": "url"})
            #if len(anchors) > 1:
                #print(anchors[1].text)
            
        #Lists all the books from Google
        text_encoded = title
        #check
        print(text_encoded)
        text_encoded = text_encoded.replace(" ", "%20")
        parent = soup.find("div",attrs={"data-async-context": "query:"+text_encoded})
        book_metadata=get_book_metadata(parent, title)
        if(book_metadata!= None):
            writer.writerow(book_metadata)
            csv_file.flush()


        

    #testcode
    #get image
            #thumbnail = child.find("img")
            #print(len(thumbnail))
            #print(thumbnail)
        



            
        
        
        
