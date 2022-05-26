import pandas as pd
import csv
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
header = ['Title', 'Author', 'Description']

with open('data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
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
        booklist=[]
        children = parent.findChildren(recursive=False)
        for child in children:
            authorname = ""
            descriptiontext = ""
            span = child.select("a > span") 
            #print(span)
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
        if(userchoicedesc in bookrange):
            print(booklist[userchoicedesc-1])
        
        elif(userchoicedesc=="11"):
            print("None")
            continue

        else:
            print("Out of range")
    # converting into CSV files
        data = [title, booklist[userchoicedesc-1]["author"], booklist[userchoicedesc-1]["description"]]
        reader=csv.reader(data,delimiter=':', quoting=csv.QUOTE_NONE)
        

        writer.writerow(reader)



    

#testcode
 #get image
        #thumbnail = child.find("img")
        #print(len(thumbnail))
        #print(thumbnail)
       



        
    
    
    
