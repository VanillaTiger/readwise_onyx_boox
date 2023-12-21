from datetime import datetime
import json
import random
import requests
import logging

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

class NotionDatabase:
    def __init__(self) -> None:
        """This class is used to connect to the notion database and retrieve the data"""
        
        self.notion_key, self.notion_database_id = self.read_notion_authorization_information()
        self.url_query = f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"
        self.url_add_pages = "https://api.notion.com/v1/pages"
        self.headers = {
            "Authorization": f"Bearer {self.notion_key}",
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }
    
    def read_notion_authorization_information(self):
        """This function reads the notion authorization information from the file"""
        with open('notion_integration/notion_key.txt', 'r') as f:
            notion_key = f.read()

        with open('notion_integration/notion_database.txt', 'r') as f:
            notion_database_id = f.read()

        return notion_key, notion_database_id

    def retrive_last_idx_number(self):
        """This function is used to retrive the last unique idx number from the notion database"""
        response = requests.post(self.url_query, headers=self.headers)

        #TODO make it more robust now its assuming its always first row with latest number

        if response.status_code == 200:
            data = response.json()
            first_row = data['results'][0] if data['results'] else None
            Idx_number = first_row['properties']['Idx']['number']
            logging.info(f"Last idx found in Database: {Idx_number}")
            return Idx_number
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")

    def query_database_notion_for_random_row(self):
        """This function is used to query notion database the random row and return response in json format"""

        last_idx = self.retrive_last_idx_number()
        idx_to_filter = random.randint(1, last_idx)

        payload = {
                    "page_size": 1,
                    "filter": {
                    "property": "Idx",
                    "number": {
                        "equals": idx_to_filter}
                    }
                }
        
        response = requests.post(self.url_query, json=payload, headers=self.headers)

        return response.json()

    def retrieve_content_from_response(self, response):
        """This function is used to retrieve the relevant content and format it from the response"""

        item_retrieved = response['results'][0]['properties']

        #format date to human readable
        date_string = item_retrieved['Date']['date']['start']
        date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
        datetime_obj = datetime.strptime(date_string, date_format)
        date_formatted = datetime_obj.strftime('%Y-%m-%d %H:%M')

        #format book to human readable
        book_unformatted = item_retrieved['Book']['rich_text'][0]['text']['content']
        book_formatted = book_unformatted.replace('_',' ')

        #format location
        location_unformatted = item_retrieved['Location']['number']
        location_formatted = str(location_unformatted)

        row_dict = {
            'Highlight': item_retrieved['Highlight']['rich_text'][0]['text']['content'],
            'Book': book_formatted,
            'Author': item_retrieved['Author']['rich_text'][0]['text']['content'],
            'Location': location_formatted,
            'Date': date_formatted,
            'Note': item_retrieved['Note']['title'][0]['text']['content'],
        }

        return row_dict

    def get_random_row_data(self):
        response = self.query_database_notion_for_random_row()
        data = self.retrieve_content_from_response(response)
        return data
    
    def send_to_notion(self, data):
        """This function sends the data to notion database"""
        r = requests.post(url = self.url_add_pages, headers = self.headers, data = json.dumps(data))
        # print(r.status_code)
        # print(r.content)
