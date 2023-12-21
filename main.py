import argparse, logging
from thought_processing.thought import WiseThought
from thought_processing.files_processing import load_new_book_annotation, prepare_file_and_headers, save_thought_to_csv
from notion_integration import notion_processing

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

def main(filepath, output_path, author, title, pipeline=False):
    """This function is used to parse the text of the annotation and extract the data to the readwise format"""
    annotation_text = load_new_book_annotation(filepath)
    prepare_file_and_headers(output_path)

    data_splited = annotation_text.split('-------------------')
    logging.info(f"Found {len(data_splited)-1} thoughts in the annotation")

    book_thoughts = []
    #processing input txt file
    for item in data_splited:
        thought = WiseThought(item, author, title)
        if item != "": #empty line at the end of the file
            try:
                row = thought.parse_thought()
                book_thoughts.append(row)
                save_thought_to_csv(row, output_path)
            except(AttributeError):
                logging.warning(f"Could not parse the following thought: {item}")
        else:
            logging.info("Found an empty line. End of file.")
    
    logging.info("Finished parsing the annotation")
    if pipeline:
        logging.info("Starting pipeline to send data to notion database")
        notion_processing.send_thoughts_to_database(book_thoughts)
    else:
        logging.info("Notion pipeline not started")
        logging.info("run notion_integration/notion_processing.py manually to send to notion database")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--filepath", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--pipeline", default=False, action="store_true")
    args = parser.parse_args()
    return args.author, args.title, args.filepath, args.output_path, args.pipeline


if __name__ == "__main__":
    author, title, filepath, output_path, pipeline = parse_args()
    # title = 'Nierozpraszalni'
    # author = 'Nir Eyal'
    # filepath = "data_input\\nierozpraszalni-nir-eyal.txt"
    # output_path = f"data_test\data_{title.replace(' ','_')}_test.csv"
    main(filepath, output_path, author, title, pipeline)
    