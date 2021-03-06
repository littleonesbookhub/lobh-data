import os
from dotenv import load_dotenv
import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import quote
import re
from imagekitio import ImageKit

imagekit = None

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")
public_key = os.getenv("PUBLIC_KEY")
url_endpoint = os.getenv("URL_ENDPOINT")

if private_key and public_key and url_endpoint:
    imagekit = ImageKit(
        private_key=private_key,
        public_key=public_key,
        url_endpoint=url_endpoint
    )

#open the website

#URL= 'https://openlibrary.org/'
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")


#find the search bar
#search_bar= soup.find(placeholder="Search")
#print(search_bar.prettify())


#read the title and author from excel
data = pd.read_excel(r'LOBH.xlsx')
df= pd.DataFrame(data,columns=['Title'])


df = df.reset_index() # make sure indexes pair with number of rows
header = ['Title', 'Author', 'Description', 'Image URL']

def get_book_metadata(soup, parent, title):
    booklist=[]
    image_base64_scripts = soup.find_all("script", string=re.compile(re.escape("(function(){var s='data")))
    image_base64s = [re.sub(re.compile("\\'\\;var\\ ii\\=\\[\\'dimg_\d\d?\\'\\]\\;\\_setImagesSrc\\(ii\\,s\\)\\;\\}\\)\\(\\)\\;"), "", x.string.replace("(function(){var s='", "")) for x in image_base64_scripts]

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
        data = [title, " ", " ", " "]
        #reader=csv.reader(data, quoting=csv.QUOTE_NONE)
        return data

    if(userchoicedesc in bookrange):
        print(booklist[userchoicedesc-1])
    else:
        print("Out of range")
# converting into CSV files

    image_base64 = None
    if userchoicedesc < len(image_base64s):
        image_base64 = image_base64s[userchoicedesc]
    
    image_url = "None"
    if image_base64 and imagekit:
        image_upload_result = imagekit.upload_file(
            file=image_base64, # required
            file_name=title, # required
            options= {
                "folder" : "/LOBH/book-thumbs/",
                "tags": ["lobh-book-thumb"],
                "is_private_file": False,
                "use_unique_file_name": True,
                "response_fields": ["is_private_file", "tags"],
            }
        )
        print(image_upload_result)
        image_url = image_upload_result["response"]["url"]
        print(image_url)
    else:
        image_url = image_base64
    data = [title, booklist[userchoicedesc-1]["author"], booklist[userchoicedesc-1]["description"], image_url]
    #reader=csv.reader(data, quoting=csv.QUOTE_NONE)
    return data

with open('data.csv', 'a', encoding='UTF8', newline='') as csv_file:
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
            
        #Lists all the books from Google
        text_encoded = title
        #check
        print(text_encoded)
        text_encoded = text_encoded.strip().replace(" ", "%20").replace(",", "%2C").replace("?", "%3F")
        parent = soup.find("div",attrs={"data-async-context": "query:"+text_encoded})
        book_metadata=get_book_metadata(soup, parent, title)
        if(book_metadata!= None):
            writer.writerow(book_metadata)
            csv_file.flush()


        


        



            
        
        
        
