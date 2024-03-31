import argparse
import csv
import random
import smtplib
import ssl
from email.message import EmailMessage

import yaml
from plyer import notification

from notion_integration.notion_book_database import NotionDatabase
from thought_processing.thought import WiseThought


def read_database(database_path):
    # Open the CSV file for reading
    with open(database_path, newline="", encoding="utf-8") as csvfile:

        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=";")

        # Create a list to store the dictionaries
        data = []

        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row as a dictionary to the list
            row_dict = {
                "Highlight": row[0],
                "Book": row[1],
                "Author": row[2],
                "URL": row[3],
                "Note": row[4],
                "Location": row[5],
                "Date": row[6],
            }
            data.append(row_dict)

    rand_int = random.randint(0, len(data))
    idx = rand_int

    return data[idx]


def send_notification_popup(thought: WiseThought):
    notification.notify(
        title=thought.title, message=thought.highlight[:256], timeout=10
    )


def prepare_html_body(thought):
    with open("notification/email_template.html") as f:
        html = f.read()

    html = html.replace("ReadWise_Title", thought.title)
    html = html.replace("ReadWise_Author", thought.author)
    html = html.replace("ReadWise_Date", f"Date: {thought.date}")
    html = html.replace("ReadWise_Location", f"Page: {thought.location}")
    html = html.replace("ReadWise_Note", f"Note: {thought.note}")
    html = html.replace("ReadWise_Highlight", f"{thought.highlight}")

    return html


def send_email(thought, email_sender, email_receiver):
    """This function is used to send email with the data retrieved from the database"""

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    with open(config["secrets"]["google"]) as f:
        password = f.read()

    email_sender = email_sender
    email_password = password
    email_receiver = email_receiver

    subject = f"Personal ReadWise - {thought.title} - {thought.author}"

    msg = EmailMessage()
    msg.add_header("Content-Type", "text/html")
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = subject
    msg.set_payload(prepare_html_body(thought))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string().encode("utf-8"))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender")
    parser.add_argument("--receiver")
    parser.add_argument("--database_path")
    args = parser.parse_args()
    return args.sender, args.receiver, args.database_path


if __name__ == "__main__":
    sender, receiver, database_path = parse_args()
    if database_path != "notion":
        data = read_database(database_path)
    else:
        notion_database = NotionDatabase()
        data = notion_database.get_random_row_data()
    send_email(data, sender, receiver)
    # send_notification_popup(data) #TODO: select option or separete script to pop up
