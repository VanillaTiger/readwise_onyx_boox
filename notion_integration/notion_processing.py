import json, requests

with open('notion_integration/notion_key.txt', 'r') as f:
    notion_key = f.read()

with open('notion_integration/notion_database.txt', 'r') as f:
    notion_database = f.read()

API_ENDPOINT = "https://api.notion.com/v1/pages"
HEADERS = {"Authorization": f"Bearer {notion_key}",
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
                "name": "Business"
            }
        },
        "Idx":{
            "number":id_number
            },
    }
    }

    return data



def main():
    """This function is used to read parsed data from Readwise format and send to the notion database"""
    filepath = 'data_output\data_How_to_sell_anything_to_anybody_fixed.csv'
    data = read_csv_rows_in_dict(filepath)
    print(len(data))
    for idx, item in enumerate(data):
        print(idx) #TODO: remove this
        idx=idx+193 #TODO: adapt this to the number of items already in the database
        data = prepare_data_for_notion(idx+1, item, notion_database)
        send_to_notion(data)

if __name__ == "__main__":
    main()