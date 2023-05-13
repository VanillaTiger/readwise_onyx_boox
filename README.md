# readwise_onyx_boox
Since Readwise.io and Onyx Boox did not provide integration I decided to write it myself. It allows processing annotation.txt file from Onyx boox to csv file that can be uploaded to readwise.io or if you wish notify you every day with your quote using windows console

## expected input
```bash
file.txt
```
which is a file exported from NeoReader application as click on the annotations in the book and export

## expected output
```bash
output.csv
```
which is formated to Readwise.io format ready to be imported thru option "import csv" thru Readwise webstie

# How to run
1. Get the input file from your onyx boox Neoreader as .txt file
2. run code below

```bash
python main.py --author author --title title --filepath file.txt --output_path output.csv
```

# How to use it with Readwise.io
Once you did 1,2 and you got your output.csv file continue with

3. Go to your readwise.io account and import highlights
4. Select import csv file and select output.csv file
5. Done

# How to send data to the notion database
You can now send data to the notion database. Get your database id and notion key.

adjust the notion_processing.py script and send data to common databse. Improvements to come.

```
notion_processing.py
```

--------------------------------------------
### TODO Next
- [x] Storing the highlights in common database
- [ ] Sending random email on the start of the system
- [ ] Initial cleanup after export from Onyx, first line of .txt