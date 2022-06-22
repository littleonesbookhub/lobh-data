import base64
import binascii
import re
import csv
from time import sleep
import requests


def main():
    process_csv("good_reads.csv", download)


def process_csv(filename, download_fn):
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        start_index = int(input("enter the 1-based start index [1]") or 1)
        to_skip = start_index
        while to_skip > 1:
            skip = next(csv_reader)
            to_skip = to_skip - 1
        print(f"header: {header}")
        for i, row in enumerate(csv_reader):
            print(f"index: {start_index + i} row: {row}")
            image_url = row[4]
            download_fn(image_url, start_index + i)
            sleep(1)


def download(url, url_index):
    url_str = str(url).strip()

    print(f'url: "{url_str}"')
    if not url_str:
        return

    out_filename = f"images/{url_index}.jpg"

    with open(out_filename, "wb") as out_file:
        b64_regex = re.compile(r"data\:image\/.*\;base64\,")
        if url_str.startswith("data:image"):
            base64_raw = b64_regex.sub("", url_str)
            bytes_b64 = None
            try:
                bytes_b64 = base64.decodebytes(bytes(base64_raw, "utf-8"))
            except binascii.Error as err:
                bytes_b64 = base64.decodebytes(bytes(base64_raw, "utf-8") + b"==")
            out_file.write(bytes_b64)
        else:
            response = requests.get(url_str)
            out_file.write(response.content)


if __name__ == "__main__":
    main()
