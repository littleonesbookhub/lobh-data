from time import sleep
import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from random import uniform


def main():
    with open("output.csv", "a", encoding="UTF8") as csv_file:
        csv_writer = csv.writer(csv_file)

        def write_row(row):
            row_copy = list(row)
            [row_copy.append("") for i in range(6 - len(row_copy))]
            csv_writer.writerow(row_copy)
            csv_file.flush()

        process_excel("first_pass_data.xlsx", search, extract, write_row)


def process_excel(filename, search_fn, extract_fn, write_fn):
    excel_df = pd.read_excel(filename)

    start_row = int(input("Enter the start index (0-based): [0]") or 0)
    num_rows = len(excel_df)

    if start_row == 0:
        write_fn(["Title", "Title2", "Author", "Description", "Image URL", "Genres"])

    for row_index in range(start_row, num_rows):
        row = [filter_cell(s) for s in excel_df.iloc[row_index].values]

        try:
            title = row[1]
            author = row[2]

            query_raw = (title + " " + author).strip()

            print("")
            print(f'Processing {row_index} "{query_raw}" ...')
            search_query = quote(f"{query_raw} site:goodreads.com")
            print(f"search_query: {search_query}")

            def retry_fn(purpose, fn, default, *args):
                keep_going = True
                result = None
                while keep_going:
                    result = fn(*args)
                    if not result:
                        # option = input(
                        #     f'Unable to get "{purpose}". Try again y/n? [{default}]'
                        # )
                        # if not option:
                        #     option = default
                        # if option != "y":
                        #     keep_going = False
                        keep_going = False
                    else:
                        keep_going = False

                return result

            page_url = retry_fn("page url", search_fn, "y", search_query)
            processed_row = page_url and retry_fn(
                "processed row", extract_fn, "n", page_url, row
            )
            if processed_row:
                write_fn(processed_row)
            else:
                write_fn(row)

            sleep(uniform(5, 10))
        except Exception as e:
            print("Skipping as something went wrong")
            print(e)

            write_fn(row)
            sleep(uniform(5, 10))


def search(search_query):
    search_url = "https://www.google.com/search?q=" + search_query
    http_headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
    }
    search_page = requests.get(search_url, headers=http_headers)
    search_soup = BeautifulSoup(search_page.content, "html.parser")

    print(f"search_url: {search_url}")
    print(f"search_page: {search_page}")

    html_file = open("index.html", "w")
    html_file.write(str(search_soup))
    html_file.close()

    # search_query = search_query.replace("%27", "'")
    # search_results_ctr = search_soup.find(
    #    "div", attrs={"data-async-context": "query:" + search_query}
    # )
    search_results_ctr = search_soup.find("div", attrs={"data-header-feature": "0"})

    search_result_link = search_results_ctr and search_results_ctr.find("a")
    search_result_link_href = search_result_link and search_result_link["href"]

    print(f"search_result_link_href: {search_result_link_href}")
    return search_result_link_href


def extract(page_url, row):
    http_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "ccsid=991-3888659-6222803; locale=en; srb_1=0_wl; __qca=P0-1165402041-1655457566917; _session_id2=bd89430ea1312e7949d35a4ebaa35304; __gpi=UID=000006b6a1420412:T=1655457567:RT=1655705564:S=ALNI_MbLJTaifkhRM8PA5Mv7Y3KSLVkntw; blocking_sign_in_interstitial=true; __gads=ID=600aa9d504ad6635:T=1655457567:S=ALNI_MauUyHhmOLjEvQf9ssV4FFe4b6ShQ",
        "Host": "www.goodreads.com",
        "If-None-Match": 'W/"906a71575a1fd654d004373e5e96abf4"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
    }
    book_page = page_url and requests.get(page_url, headers=http_headers)
    print(f"book_page: {book_page}")
    book_soup = book_page and BeautifulSoup(book_page.content, "html.parser")

    # html_file = open("index.html", "w")
    # html_file.write(str(book_soup))
    # html_file.close()

    cover_image = book_soup and (
        book_soup.find("img", {"id": "coverImage"})
        or book_soup.select("div.mainBookCover img")
        or book_soup.select("div.BookCover__image img")
    )
    if isinstance(cover_image, list) and len(cover_image) > 0:
        cover_image = cover_image[0]
    print(f"cover_image: {cover_image}")
    cover_image_url = cover_image and cover_image["src"] or ""
    print(f"cover_image_url: {cover_image_url}")

    genres = []

    genre_divs = (
        book_soup
        and (
            book_soup.select("div.rightContainer > div.stacked div.left")
            or book_soup.select('li[itemprop="genre"]')
        )
    ) or []

    if genre_divs:
        for genre_div in genre_divs:
            genre_anchors = genre_div.select("a")
            if genre_anchors:
                genre = ">".join(
                    [genre_anchor.text.strip() for genre_anchor in genre_anchors]
                )
                genres.append(genre)

    print(f"genres: {genres}")

    if not cover_image_url and not genres:
        return None

    return [
        row[0],
        row[1],
        row[2],
        row[3],
        cover_image_url,
        ";".join(genres),
    ]


def filter_cell(s):
    return s if isinstance(s, str) else ""


if __name__ == "__main__":
    main()
