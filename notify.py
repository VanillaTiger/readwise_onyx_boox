import random
from plyer import notification
import csv
import argparse

import smtplib
import ssl
from email.message import EmailMessage

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
            'Title': row[1],
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
        title = data['Title'],
        message = data['Highlight'][:256],
        timeout = 10)

def send_email(data, email_sender, email_receiver):

    with open('google.txt', 'r') as f:
        password = f.read()

    email_sender = 'a.szummer@gmail.com'
    email_password = password
    email_receiver = 'adam.szummer@digica.com'

    subject = f"Personal ReadWise - {data['Title']} - {data['Author']}"
    body = f" Date: {data['Date']}\n Location: {data['Location']}\n Note: {data['Note']}\n Quote:\n\n{data['Highlight']}\n"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender")
    parser.add_argument("--receiver")
    parser.add_argument("--database_path")
    args = parser.parse_args()
    return args.sender, args.receiver, args.database_path

if __name__ == "__main__":
    sender, receiver, database_path = parse_args()
    data = read_database(database_path)
    send_email(data, sender, receiver)
    send_notification_popup(data)