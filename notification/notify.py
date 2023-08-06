import random
from plyer import notification
import csv
import argparse

import smtplib
import ssl
from email.message import EmailMessage

import requests
from datetime import datetime

from notion_integration.notion_processing import read_notion_authorization_information, retrive_last_idx_number

class NotionDatabase:
    def __init__(self) -> None:
        """This class is used to connect to the notion database and retrieve the data"""
        
        self.notion_key, self.notion_database = read_notion_authorization_information()
        self.url = f"https://api.notion.com/v1/databases/{self.notion_database}/query"
        self.headers = {
            "Authorization": f"Bearer {self.notion_key}",
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }

    def query_database_notion_for_random_row(self):
        """This function is used to query notion database the random row and return response in json format"""

        last_idx = retrive_last_idx_number(self.notion_database, self.headers)
        idx_to_filter = random.randint(1, last_idx)

        payload = {
                    "page_size": 1,
                    "filter": {
                    "property": "Idx",
                    "number": {
                        "equals": idx_to_filter}
                    }
                }
        
        response = requests.post(self.url, json=payload, headers=self.headers)

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

    def get_row_data(self):
        response = self.query_database_notion_for_random_row()
        data = self.retrieve_content_from_response(response)
        return data
    

def read_database(database_path):
    # Open the CSV file for reading
    with open(database_path, newline='', encoding='utf-8') as csvfile:

        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=';')

        # Read the headers from the first row
        headers = next(reader)

        # Create a list to store the dictionaries
        data = []

        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row as a dictionary to the list
            row_dict = {'Highlight': row[0],
            'Book': row[1],
            'Author': row[2],
            'URL': row[3],
            'Note': row[4],
            'Location': row[5],
            'Date': row[6]}
            data.append(row_dict)

    rand_int = random.randint(0, len(data))
    idx = rand_int

    return data[idx]

def send_notification_popup(data):
    notification.notify(
        title = data['Book'],
        message = data['Highlight'][:256],
        timeout = 10)

def prepare_html_body(data):
    with open("notification/email_template.html", "r") as f:
        html = f.read()
    
    html = html.replace('ReadWise_Title', data['Book'])
    html = html.replace('ReadWise_Author', data['Author'])
    html = html.replace('ReadWise_Date', f"Date: {data['Date']}")
    html = html.replace('ReadWise_Location', f"Page: {data['Location']}")
    html = html.replace('ReadWise_Note', f"Note: {data['Note']}")
    html = html.replace('ReadWise_Highlight', f"{data['Highlight']}")

    return html

def send_email(data, email_sender, email_receiver):
    """This function is used to send email with the data retrieved from the database"""

    with open('google.txt', 'r') as f:
        password = f.read()

    email_sender = email_sender
    email_password = password
    email_receiver = email_receiver

    subject = f"Personal ReadWise - {data['Book']} - {data['Author']}"

    msg = EmailMessage()
    msg.add_header('Content-Type', 'text/html')
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.set_payload(prepare_html_body(data))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string().encode('utf-8'))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender")
    parser.add_argument("--receiver")
    parser.add_argument("--database_path")
    args = parser.parse_args()
    return args.sender, args.receiver, args.database_path

if __name__ == "__main__":
    sender, receiver, database_path = parse_args()
    if database_path != 'notion':
        data = read_database(database_path)
    else:
        notion_database = NotionDatabase()
        data = notion_database.get_row_data()
    send_email(data, sender, receiver)
    # send_notification_popup(data) #TODO: select option or separete script to pop up