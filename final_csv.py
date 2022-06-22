import csv


def main():
    process_csv("good_reads.csv", "final.csv")


def process_csv(in_ilename, out_filename):
    with open(in_ilename, "r") as csv_file:
        with open(out_filename, "w") as out_csv_file:
            csv_reader = csv.reader(csv_file)
            csv_writer = csv.writer(out_csv_file)

            header = next(csv_reader)
            csv_writer.writerow(
                [
                    "id",
                    "title",
                    "author",
                    "genre",
                    "age_group",
                    "availability",
                    "description",
                    "thumbnail_url",
                ]
            )
            for i, row in enumerate(csv_reader):
                id = i + 1
                title = row[0]
                author = row[2]
                genre = row[5]
                age_group = "0-2;2-4;4-10;10+"
                availability = "available"
                description = row[3]
                folder_index = 6
                if id < 201:
                    folder_index = 1
                elif id < 401:
                    folder_index = 2
                elif id < 600:
                    folder_index = 3
                elif id < 800:
                    folder_index = 4
                elif id < 1000:
                    folder_index = 5
                thumbnail_url = (
                    f"https://ik.imagekit.io/qdxmlqyzh/LOBH/images-{folder_index}/{id}.jpg"
                    if str(row[4]).strip()
                    else ""
                )
                csv_writer.writerow(
                    [
                        id,
                        title,
                        author,
                        genre,
                        age_group,
                        availability,
                        description,
                        thumbnail_url,
                    ]
                )


if __name__ == "__main__":
    main()
