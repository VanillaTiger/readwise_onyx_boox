import json, requests

with open('notion_integration/notion_key.txt', 'r') as f:
    notion_key = f.read()

with open('notion_integration/notion_database.txt', 'r') as f:
    notion_database = f.read()

API_ENDPOINT = "https://api.notion.com/v1/pages"
HEADERS = {"Authorization": f"Bearer {notion_key}",
"Content-Type": "application/json","Notion-Version": "2021-08-16"}

data= {

"parent":
    {"type":"database_id",
    "database_id":notion_database,
},
"properties":{
    "Highlight":{
        "id":"%3Eol%3B",
        "type":"rich_text",
        "rich_text":[]},
    "Tags":{
        "id":"MGgF",
        "type":"select",
        "select":None},
    "id":{
        "id":"TcFb",
        "type":"number",
        "number":1},
    "ToCorrect":{
        "id":"%5D%7D%5By",
        "type":"checkbox",
        "checkbox":False},
    "URL":{
        "id":"gMKa",
        "type":"url",
        "url":None},
    "Date":{
        "id":"i_sf",
        "type":"date",
        "date":None},
    "Location":{
        "id":"stDz",
        "type":"number",
        "number":None},
    "Author":{
        "id":"%7DJG%3C",
        "type":"rich_text",
        "rich_text":[]},
    "Note":{
        "id":"title",
        "type":"title",
        "title":[{
            "type":"text",
            "text":{"content":"Yurts in Big Sur, California","link":None},
            "annotations":{"bold":False,"italic":False,"strikethrough":False,"underline":False,"code":False,"color":"default"},
            "plain_text":"Yurts in Big Sur, California","href":None}]}},
"url":"https://www.notion.so/Yurts-in-Big-Sur-California-8c5dbbe26ed9486396b0a05b2dee32e0"}

r = requests.post(url = API_ENDPOINT, headers = HEADERS, data = json.dumps(data))
print(r.content)