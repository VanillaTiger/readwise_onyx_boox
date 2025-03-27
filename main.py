import argparse
import logging

from src.notion import notion_processing
from src.thought_processing.files_processing import load_new_book_annotation
from src.thought_processing.files_processing import prepare_file_and_headers
from src.thought_processing.files_processing import save_thought_to_csv
from src.thought_processing.wise_thought import WiseThought

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


def main(filepath, output_path, author, title, pipeline=False):
    """This function is used to parse the text of the annotation
    and extract the data to the readwise format"""
    annotation_text = load_new_book_annotation(filepath)
    prepare_file_and_headers(output_path)

    data_splited = annotation_text.split("-------------------")
    logging.info(f"Found {len(data_splited)-1} thoughts in the annotation")

    book_thoughts = []
    # processing input txt file
    for item in data_splited:
        if item != "" or item != "\n":  # empty line at the end of the file
            try:
                thought = WiseThought(title=title, author=author, text=item)
                thought.extract_information()
                thought_to_save = thought.model_dump(
                    include={
                        "highlight",
                        "title",
                        "author",
                        "url",
                        "note",
                        "location",
                        "date",
                    }
                )
                book_thoughts.append(thought_to_save)
                save_thought_to_csv(thought_to_save, output_path)
            except AttributeError as e:
                logging.warning(
                    f"Could not parse the following thought: {item} error {e}"
                )
        else:
            logging.info("Found an empty line. End of file.")

    logging.info("Finished parsing the annotation")
    if pipeline:
        logging.info("Starting pipeline to send data to notion database")
        notion_processing.send_thoughts_to_database(book_thoughts)
    else:
        logging.info("Notion pipeline not started")
        logging.info(
            "run notion_integration/notion_processing.py manually to send to notion database"
        )


def parse_args():
    """This function is used to parse the arguments from the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--filepath", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--pipeline", default=False, action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # title = 'Nierozpraszalni'
    # author = 'Nir Eyal'
    # filepath = "data_input\\nierozpraszalni-nir-eyal.txt"
    # output_path = f"data_test\data_{title.replace(' ','_')}_test.csv"
    main(args.filepath, args.output_path, args.author, args.title, args.pipeline)
