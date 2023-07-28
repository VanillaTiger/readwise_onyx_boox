import json, requests
import argparse

def read_notion_authorization_information():
    with open('notion_integration/notion_key.txt', 'r') as f:
        notion_key = f.read()

    with open('notion_integration/notion_database.txt', 'r') as f:
        notion_database = f.read()

    return notion_key, notion_database

NOTION_KEY, NOTION_DATABASE = read_notion_authorization_information()

API_ENDPOINT = "https://api.notion.com/v1/pages"
HEADERS = {"Authorization": f"Bearer {NOTION_KEY}",
"Content-Type": "application/json","Notion-Version": "2022-06-28"}

def send_to_notion(data):
    r = requests.post(url = API_ENDPOINT, headers = HEADERS, data = json.dumps(data))
    # print(r.status_code)
    # print(r.content)

def read_csv_rows_in_dict(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    headers = data[0].split(';')
    data = data[1:]
    data = [item.split(';') for item in data]
    data = [dict(zip(headers, item)) for item in data]
    return data

def prepare_data_for_notion(id_number, dict_thought, notion_database):
    #TODO: adapt this to the notion database schema
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

def retrive_last_idx_number():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE}/query"
    response = requests.post(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        first_row = data['results'][0] if data['results'] else None
        # print(first_row)
        Idx_number = first_row['properties']['Idx']['number']
        print(Idx_number)
        return Idx_number
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main(filepath):
    """This function is used to read parsed data from Readwise format and send to the notion database"""
    # filepath = 'data_output\Fix-Zero-To-One.csv'
    data = read_csv_rows_in_dict(filepath)
    print(len(data))
    last_idx = retrive_last_idx_number()
    print(f"Last idx: {last_idx}")

    for idx, item in enumerate(data):
        print(idx) #TODO: remove this
        idx=idx+last_idx # 456 TODO: make it more robust now its assuming its always first row with latest number
        data = prepare_data_for_notion(idx+1, item, NOTION_DATABASE)
        send_to_notion(data)

def read_input_file_path():
    parser = argparse.ArgumentParser(description='Readwise to Notion')
    parser.add_argument('-f', '--filepath', type=str, metavar='', required=True, help='Filepath to the csv file')
    args = parser.parse_args()
    return args.filepath

if __name__ == "__main__":
    filepath = read_input_file_path()
    main(filepath)