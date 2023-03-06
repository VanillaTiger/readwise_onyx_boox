import re

class WiseThought:
    """This class is used to parse the text of the annotation and extract the data"""
    def __init__(self, text, author, title):
        self.highlight = ''
        self.title = title
        self.author = author
        self.url = ''
        self.note = ''
        self.location = ''
        self.date = ''
        self.text = text
    
    def get_dict_to_save(self):
        row = {'Highlight': self.highlight,
            'Title': self.title,
            'Author':self.author,
            'URL':self.url,
            'Note':self.note,
            'Location':self.location,
            'Date':self.date}
        return row
    
    def get_date(self):
        regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
        match = re.search(regex, self.text)
        indexes = match.span()
        date_text = self.text[indexes[0]:indexes[1]]
        self.text = self.text.replace(date_text,'')
        self.date = match[0].replace('-','.')
        return self.date, self.text

    def get_location(self):
        regex = r"Page No\.:\s*(\d+)"
        match = re.search(regex, self.text)
        self.location = match.group(1)
        page_text = self.text[match.start():match.end()]
        self.text = self.text.replace(page_text,'')
        # print(text)
        # print(page_number)
        # row['Location']=page_number
        self.text = self.text.replace('\xa0\xa0|\xa0\xa0','')
        return self.location, self.text

    def get_highlight_and_note(self):
        ## be careful the text is already process and date and page number is removed,
        ## must run date and location before
        highlight_dirty=self.text
        start_Note = highlight_dirty.find('【Note】')
        self.highlight = highlight_dirty[:start_Note-1]
        self.note = highlight_dirty[start_Note+6:-1]
        self.highlight = re.sub(r"^[\n\r]+", "", self.highlight)
        self.highlight = self.highlight.replace('\n','')

        return self.highlight, self.note, self.text

    def parse_thought(self):
        """order matters as with each function the text is modified by removing processed data"""
        self.get_date()
        self.get_location()
        self.get_highlight_and_note()
        row = self.get_dict_to_save()
        return row
        
