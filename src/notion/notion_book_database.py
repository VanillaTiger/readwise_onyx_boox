"""This module is used to connect to the notion database and retrieve the data"""
import json
import logging
import os
import random
from datetime import datetime

import requests
from dotenv import load_dotenv
from omegaconf import OmegaConf

from src.thought_processing.wise_thought import WiseThought

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

load_dotenv()


class NotionDatabase:
    """This class is used to connect to the notion database and retrieve the data"""

    def __init__(self) -> None:
        """This class is used to connect to the notion database and retrieve the data"""

        self.config = OmegaConf.load("config.yaml")

        self.config_notion = dict(self.config)["notion"]
        self.notion_key = os.getenv("notion_API_KEY")
        self.notion_database_id = os.getenv("notion_DATABASE_ID")

        self.url_query = self.config_notion["url_query"].format(
            database_id=self.notion_database_id
        )

        self.url_add_pages = self.config_notion["url_add_pages"]
        self.headers = {
            "Authorization": self.config_notion["headers"]["Authorization"].format(
                notion_key=self.notion_key
            ),
            "accept": self.config_notion["headers"]["accept"],
            "Notion-Version": self.config_notion["headers"]["Notion-Version"],
            "content-type": self.config_notion["headers"]["content-type"],
        }

    def retrive_last_idx_number(self):
        """This function is used to retrive the last unique idx number from the notion database"""
        response = requests.post(self.url_query, headers=self.headers, timeout=10)

        # ./TODO make it more robust now its assuming its always first row with latest number

        if response.status_code == 200:
            data = response.json()
            first_row = data["results"][0]
            idx_number = first_row["properties"]["Idx"]["number"]
            logging.info(f"Last idx found in Database: {idx_number}")
            return idx_number
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")
            raise ConnectionError(f"Error: {response.status_code} - {response.text}")

    def get_all_rows_data(self):
        """This function retrieves all rows from the Notion database and stores them as WiseThought objects."""
        all_thoughts = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {"page_size": 100}
            if next_cursor:
                payload["start_cursor"] = next_cursor

            response = requests.post(
                self.url_query, json=payload, headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                for result in data["results"]:
                    thought = self._extract_thought_from_response({"results": [result]})
                    all_thoughts.append(thought)

                has_more = data.get("has_more", False)
                next_cursor = data.get("next_cursor", None)
            else:
                logging.error(f"Error: {response.status_code} - {response.text}")
                raise ConnectionError(
                    f"Error: {response.status_code} - {response.text}"
                )

        return all_thoughts

    def _retrieve_random_row_from_database(self):
        """This function is used to query notion database the random row and
        return response in json format"""

        last_idx = self.retrive_last_idx_number()
        idx_to_filter = random.randint(1, last_idx)

        payload = {
            "page_size": 1,
            "filter": {"property": "Idx", "number": {"equals": idx_to_filter}},
        }

        response = requests.post(
            self.url_query, json=payload, headers=self.headers, timeout=10
        )

        return response.json()

    def _extract_thought_from_response(self, response):
        """This function is used to retrieve the relevant content and format it from the response"""

        item_retrieved = response["results"][0]["properties"]

        # format date to human readable
        date_string = item_retrieved["Date"]["date"]["start"]
        date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        datetime_obj = datetime.strptime(date_string, date_format)
        date_formatted = datetime_obj.strftime("%Y-%m-%d %H:%M")

        # format book to human readable
        book_unformatted = item_retrieved["Book"]["rich_text"][0]["text"]["content"]
        book_formatted = book_unformatted.replace("_", " ")

        # format location
        location_unformatted = item_retrieved["Location"]["number"]
        location_formatted = str(location_unformatted)

        thought = WiseThought(
            highlight=item_retrieved["Highlight"]["rich_text"][0]["text"]["content"],
            title=book_formatted,
            author=item_retrieved["Author"]["rich_text"][0]["text"]["content"],
            location=location_formatted,
            date=date_formatted,
            note=item_retrieved["Note"]["title"][0]["text"]["content"],
        )

        return thought

    def get_random_row_data(self):
        """This function is used to retrieve the random row from the notion database and
        return it as WiseThought object"""
        response = self._retrieve_random_row_from_database()
        thought = self._extract_thought_from_response(response)
        return thought

    def send_data(self, data):
        """This function sends the data to notion database"""
        r = requests.post(
            url=self.url_add_pages,
            headers=self.headers,
            data=json.dumps(data),
            timeout=10,
        )
        if r.status_code != 200:
            logging.error(f"Error: {r.status_code} - {r.text}")

        return r.status_code
        # print(r.status_code)
        # print(r.content)
