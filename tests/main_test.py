# content of test_sample.py
import csv
import os

from main import main


def test_main_without_pipeline():
    filepath = "data_input/Author_test-Title_test.txt"
    output_path = "output_test.csv"
    author = "test_author"
    title = "test_title"
    pipeline = False
    main(filepath, output_path, author, title, pipeline)

    assert os.path.exists(output_path) == True

    # check if the file has the right content
    data = []
    with open(output_path, newline="\n", encoding="utf-8") as csvfile:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csvfile, delimiter=";")

        # Iterate over rows and convert each row to a dictionary
        for row in csv_reader:
            data.append(row)

    assert data[0]["Author"] == author
    assert data[0]["Title"] == title
    assert data[0]["Highlight"] == "Test description 1"
    assert data[0]["Note"] == "Test Note 1"
    assert data[0]["Location"] == "1"
    assert data[0]["Date"] == "2023.02.25 23:58"

    # python main.py --author test --title test --filepath data_input/Author_test-Title_test.txt --output_path output_test.csv --pipeline
