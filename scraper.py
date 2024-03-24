import requests # for managing requests
from bs4 import BeautifulSoup # for webscraping
import json # reading and writing json files
# check current date in indian standard time
from datetime import datetime # current date and time
import pytz # timezones

# gathers date and time, round checks current round of the season
# corresponding to current date
round = 1
current_datetime = datetime.now()

# has urls for each round of the season
with open('data/urls.json', 'r') as file:
    f1_results_url = json.load(file)

# returns the newest round of the season or 0 if the season has ended
def check_date():
    global round
    while True:
        if round > 23:
            break
        if current_datetime > datetime.strptime(f1_results_url[f"rnd{round}"]["checkDate"],  "%Y-%m-%d"):
            round += 1
        else:
            print("Next round in: ",datetime.strptime(f1_results_url[f"rnd{round}"]["checkDate"],  "%Y-%m-%d"))
            break
    return int(round-1) if (1 < round < 24) else 0


def get_race_info():
    # Load the previous json data
    with open('data/drivers-championship.json', 'r') as f:
        try:
            previous_data = json.load(f)
        except json.JSONDecodeError:
            previous_data = {}

    # URL of the webpage you want to scrape
    round_number = check_date()
    print("Latest round: ", round_number)

    # provides the list of drivers, their positions, points and teams TILL THE LATEST RACE
    for i in range(1, round_number+1):
        url = f1_results_url[f"rnd{i}"]["link"]

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
        # driver_points = [driver[-1] for driver in driver_list]
        driver_name = [driver[3] + ' ' + driver[4] for driver in driver_list]
        # driver_team = [driver[7] for driver in driver_list]

        # Create a dictionary to hold the data
        data = {f"rnd{i}": {}}

        # Iterate over the positions and driver names, adding them to the dictionary
        for position, driver_name in zip(driver_positions, driver_name):
            data[f"rnd{i}"][position] = driver_name

        # Append new data to the previous data
        previous_data.update(data)

    # Write the updated data to the JSON file
    with open('data/drivers-championship.json', 'w') as f:
        json.dump(previous_data, f, indent=4)

def main():
    get_race_info()

if __name__ == '__main__':
    main()