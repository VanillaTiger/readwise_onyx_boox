import json, requests
import argparse, logging
from tqdm import tqdm

from notion_integration.notion_book_database import NotionDatabase

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

def read_csv_rows_in_dict(filepath):
    """This function reads the csv file and returns a list of dictionaries with the data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    headers = data[0].split(';')
    data = data[1:]
    if data[-1] == "":
        data.pop(-1) #remove last empty line
        data = [item.split(';') for item in data]
        data = [dict(zip(headers, item)) for item in data]
    return data

def prepare_data_for_notion(id_number, dict_thought, notion_database):
    """This function prepares the data to be sent to notion database"""
    #TODO: adapt this to the notion database schema if changes
    data= {

    "parent":
        {"database_id":notion_database},
    "properties":
    {
         "Note": {
            "title": [
            {
                "text": {
                "content": dict_thought['Note']
                },
         }]
        },
        "Author":{
            "rich_text": [
            {"type": "text",
            "text": {
                "content": dict_thought['Author']
                },
            }]    
        },
        "Highlight":{
            "rich_text": [
            {"type": "text",
            "text": {
                "content": dict_thought['Highlight']
                },
            }]    
        },
        "Date":{
            "date": {
                "start":dict_thought['Date'].replace('.','-')
            }
        },
        "ToCorrect": {
            "checkbox": False
        },
        "Location":{
            "number":int(dict_thought['Location'])
            },
        "Book":{
            "rich_text":[
                {
                    'type':'text', 
                    'text': {
                        'content':dict_thought['Title']}
                }
        ]},
        "Tags":{
            "select": {
                "name": "Understanding"
            }
        },
        "Idx":{
            "number":id_number
            },
    }
    }

    return data


def main(filepath):
    """This function is used to read parsed data from Readwise format and send to the notion database"""
    # filepath = 'data_output\Fix-Zero-To-One.csv'
    data = read_csv_rows_in_dict(filepath)
    logging.info(f"Read {len(data)} rows from {filepath}")
    notioon_book_databse = NotionDatabase()
    last_idx = notioon_book_databse.retrive_last_idx_number()

    for idx, item in tqdm(enumerate(data)):
        idx=idx+last_idx # 592 TODO: make it more robust now its assuming its always first row with latest number
        data = prepare_data_for_notion(idx+1, item, notioon_book_databse.notion_database_id)
        notioon_book_databse.send_to_notion(data)

    logging.info(f"{idx-last_idx+1} rows sent to Notion. New last idx {idx+1}")

def read_input_file_path():
    parser = argparse.ArgumentParser(description='Readwise to Notion')
    parser.add_argument('-f', '--filepath', type=str, metavar='', required=True, help='Filepath to the csv file')
    args = parser.parse_args()
    return args.filepath

if __name__ == "__main__":
    filepath = read_input_file_path()
    main(filepath)
    logging.info("Done, check notion database")