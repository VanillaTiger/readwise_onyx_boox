"""Definition of the class WiseThought that is used to parse the text of the annotation and extract the data"""
import re

from pydantic import BaseModel


class WiseThought(BaseModel):
    """This class is used to parse the text of the annotation and extract the data"""

    highlight: str = "placeholder"
    title: str = "placeholder"
    author: str = "placeholder"
    url: str = "placeholder"
    note: str = "placeholder"
    location: str = "placeholder"
    date: str = "placeholder"
    text: str = "placeholder"

    def _extract_date(self):
        regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
        match = re.search(regex, self.text)
        if match is not None:
            indexes = match.span()
            date_text = self.text[indexes[0] : indexes[1]]
            self.text = self.text.replace(date_text, "")
            self.date = match[0].replace("-", ".")
        else:
            raise AssertionError("Date not found")

    def _extract_location(self):
        regex = r"Page No\.:\s*(\d+)"
        match = re.search(regex, self.text)
        if match is not None:
            self.location = match.group(1)
            page_text = self.text[match.start() : match.end()]
            self.text = self.text.replace(page_text, "")
        else:
            raise AssertionError("Location not found")
        self.text = self.text.replace("\xa0\xa0|\xa0\xa0", "")

    def _extract_highlight_and_note(self):
        # be careful the text is already process and date and page number is removed,
        # must run date and location before
        highlight_dirty = self.text
        start_note = highlight_dirty.find("【Note】")
        self.highlight = highlight_dirty[: start_note - 1]
        self.note = highlight_dirty[start_note + 6 : -1]
        self.note = self.note.replace(";", ",")
        self.highlight = re.sub(r"^[\n\r]+", "", self.highlight)
        self.highlight = self.highlight.replace("\n", "")
        self.highlight = self.highlight.replace(";", ",")

    def extract_information(self):
        """order matters as with each function the text is modified by removing processed data"""
        self._extract_date()
        self._extract_location()
        self._extract_highlight_and_note()
