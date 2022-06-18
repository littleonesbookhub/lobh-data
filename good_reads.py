import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
import time
import math

def main():
    with open("output.csv", 'w', encoding='UTF8') as csv_file:
        csv_writer = csv.writer(csv_file)
        def write_row(row):
            csv_writer.writerow(row)
            csv_file.flush()
        write_row(['Title', 'Title2', 'Author', 'Description', 'Image URL', 'Genres'])
        process_excel("first_pass_data.xlsx", process_row, write_row)

def process_excel(filename, process_row, write_row):
    excel_df = pd.read_excel(filename)
    
    start_row = int(input("Enter the start index (0-based): "))
    num_rows = len(excel_df)

    for row_index in range(start_row, num_rows):
        row = excel_df.iloc[row_index].values
        try:
            write_row(process_row(row, row_index))
        except:
            print("Skipping as something went wrong")

        time.sleep(5)

def process_row(row, row_index):
    filter_cell = lambda s : s if isinstance(s, str) else ""
    title = filter_cell(row[1])
    author = filter_cell(row[2])

    query_raw = (title + ' ' + author).strip()

    print("")
    print(f"Processing {row_index} \"{query_raw}\" ...")
    search_query = quote_plus(f"{query_raw} site:goodreads.com")
    print(f"search_query: {search_query}")
    
    search_url = 'https://www.google.com/search?q=' + search_query
    
    https_headers = {"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"}
    search_page = requests.get(search_url,headers=https_headers)
    search_soup = BeautifulSoup(search_page.content, "html.parser")
    
    #html_file = open("index.html", "w")
    #html_file.write(str(search_soup))
    #html_file.close()

    search_query = search_query.replace("+", "%20")
    search_results_ctr = search_soup.find("div",attrs={"data-async-context": "query:"+search_query})
    search_result_link = search_results_ctr and search_results_ctr.find("a")
    search_result_link_href = search_result_link and search_result_link['href']

    print(f"search_result_link_href: {search_result_link_href}")

    book_page = search_result_link_href and requests.get(search_result_link_href)
    book_soup = book_page and BeautifulSoup(book_page.content, "html.parser")

    cover_image = book_soup and book_soup.find("img", {"id": "coverImage"})
    cover_image_url = cover_image and cover_image['src']
    print(f"cover_image_url: {cover_image_url}")
    
    genres = []

    genre_divs = (book_soup and book_soup.select("div.rightContainer > div.stacked div.left")) or []
    for genre_div in genre_divs:
        genre_anchors = genre_div.select("a")
        genre = ">".join([genre_anchor.text for genre_anchor in genre_anchors])
        genres.append(genre)

    print(f"genres: {genres}")

    return [filter_cell(row[0]), filter_cell(row[1]), filter_cell(row[2]), filter_cell(row[3]), cover_image_url, ";".join(genres)]


if __name__ == "__main__":
    main()



        



            
        
        
        
