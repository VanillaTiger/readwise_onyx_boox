import argparse
from thought_processing.thought import WiseThought
from thought_processing.files_processing import load_new_book_annotation, prepare_file_and_headers, save_thought_to_csv

def main(filepath, output_path, author, title):
    annotation_text = load_new_book_annotation(filepath)
    prepare_file_and_headers(output_path)

    data_splited = annotation_text.split('-------------------')
    for item in data_splited[0:-1]:
        thought = WiseThought(item,author, title)
        row = thought.parse_thought()
        save_thought_to_csv(row, output_path)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author")
    parser.add_argument("--title")
    parser.add_argument("--filepath")
    parser.add_argument("--output_path")
    args = parser.parse_args()
    return args.author, args.title, args.filepath, args.output_path

if __name__ == "__main__":
    author, title, filepath, output_path = parse_args()
    # title = 'Nierozpraszalni'
    # author = 'Nir Eyal'
    # filepath = "data_input\\nierozpraszalni-nir-eyal.txt"
    # output_path = f"data_test\data_{title.replace(' ','_')}_test.csv"
    main(filepath, output_path, author, title)
    