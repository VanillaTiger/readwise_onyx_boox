import random
from plyer import notification
import csv

# Open the CSV file for reading
with open('data_test\data_Nierozpraszalni_test.csv', newline='', encoding='utf-8') as csvfile:

    # Create a CSV reader object
    reader = csv.reader(csvfile, delimiter=';')

    # Read the headers from the first row
    headers = next(reader)

    # Create a list to store the dictionaries
    data = []

    # Iterate over each row in the CSV file
    for row in reader:
        # Append the row as a dictionary to the list
        data.append(row)

rand_int = random.randint(0, len(data))
idx = rand_int
notification.notify(
    title = data[idx][1],
    message = data[idx][0][:256],
    timeout = 10)