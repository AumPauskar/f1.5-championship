import requests
from bs4 import BeautifulSoup
import json
# check current date in indian standard time
from datetime import datetime
import pytz

round = 1
current_datetime = datetime.now()

with open('data/urls.json', 'r') as file:
    f1_results_url = json.load(file)

def check_date():
    global round
    while True:
        if round > 23:
            break
        if current_datetime > datetime.strptime(f1_results_url[f"rnd{round}"]["checkDate"],  "%Y-%m-%d"):
            round += 1
            print(round)
        else:
            print(datetime.strptime(f1_results_url[f"rnd{round}"]["checkDate"],  "%Y-%m-%d"))
            break
    return int(round-1) if (1 < round < 24) else 0


# URL of the webpage you want to scrape
round_number = check_date()
url = f1_results_url[f"rnd{round_number}"]["link"]

# Send an HTTP request to the URL
response = requests.get(url)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')


cells = soup.find_all('tr')
values = []


for cell in cells:
    bold_cell = cell.find('td', class_='bold')
    # Append the text content of the cell to the list
    if bold_cell:
        values.append(cell.text.strip())

# Split the string into a list of strings
driver_list = [driver.split('\n') for driver in values]

# get driver position and driver points from the list
driver_positions = [driver[0] for driver in driver_list]
driver_points = [driver[-1] for driver in driver_list]
print(driver_positions)
print(driver_points)