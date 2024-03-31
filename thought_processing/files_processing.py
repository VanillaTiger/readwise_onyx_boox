import csv

from thought_processing.thought import WiseThought


def load_new_book_annotation(filepath):
    with open(filepath, encoding="utf8") as f:
        f.readline()
        print("Skipped first line")
        annotations_text = f.read()

    return annotations_text


def prepare_file_and_headers(output_path):

    headers = WiseThought().model_dump(
        include={"highlight", "title", "author", "url", "note", "location", "date"}
    )

    # Open the CSV file in write mode
    with open(output_path, "w", newline="", encoding="utf-8") as file:

        # Create a writer object
        writer = csv.DictWriter(file, fieldnames=list(headers), delimiter=";")

        # Write the header row
        writer.writeheader()


def save_thought_to_csv(row, output_path):
    # Open the CSV file in write mode
    with open(output_path, "a", newline="", encoding="utf-8") as file:

        # Create a writer object
        writer = csv.DictWriter(file, fieldnames=row.keys(), delimiter=";")

        # Write the data row
        writer.writerow(row)

        # print(row)
