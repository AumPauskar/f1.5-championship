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

def remove_by_value(dict, value):
    keys_to_remove = [key for key, val in dict.items() if val == value]
    for key in keys_to_remove:
        dict.pop(key, None)

def write_race_data():
    # Load the previous json data
    with open('data/drivers-championship.json', 'r') as f:
        try:
            previous_data = json.load(f)
        except json.JSONDecodeError:
            previous_data = {}




    drivers_list = {
        "Max Verstappen": 0,
        "Sergio Perez": 0,
        "Carlos Sainz": 0,
        "Charles Leclerc": 0,
        "George Russell": 0,
        "Lando Norris": 0,
        "Lewis Hamilton": 0,
        "Oscar Piastri": 0,
        "Fernando Alonso": 0,
        "Lance Stroll": 0,
        "Zhou Guanyu": 0,
        "Kevin Magnussen": 0,
        "Daniel Ricciardo": 0,
        "Yuki Tsunoda": 0,
        "Alexander Albon": 0,
        "Nico Hulkenberg": 0,
        "Esteban Ocon": 0,
        "Pierre Gasly": 0,
        "Valtteri Bottas": 0,
        "Logan Sargeant": 0,
        "Oliver Bearman": 0
    }


    # all drivers standings
    # for count in range(1, 24):
    #     try:
    #         for position in range(1, 21):
    #             print(previous_data[f"rnd{count}"][f"{position}"])
    #         print("\n")
    #     except KeyError:
    #         break

    no_max = []

    round_number = check_date()
    # f1 list with no max verstappen
    for count in range(1, round_number+1):
        round_results = []
        no_max.append(round_results)
        try:
            for position in range(1, 21):
                if (previous_data[f"rnd{count}"][f"{position}"]) != "Max Verstappen":
                    round_results.append(previous_data[f"rnd{count}"][f"{position}"])
            print("\n\n")
        except KeyError:
            pass

    # calculating points
    for count in range(1, round_number+1):
        for position in range(1, 11):
            match position:
                case 1: # winner
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 25
                case 2: # runner up
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 18
                case 3: # podium
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 15
                case 4:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 12
                case 5:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 10
                case 6:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 8
                case 7:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 6
                case 8:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 4
                case 9:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 2
                case 10:
                    drivers_list[previous_data[f"rnd{count}"][f"{position}"]] += 1



    # sort dictionary `drivers_list` by value
    sorted_drivers = dict(sorted(drivers_list.items(), key=lambda item: item[1], reverse=True))
    # deep copy sorted_drivers into drivers_list
    drivers_list = sorted_drivers.copy()
    print(drivers_list)

    # f1 with no red bull
    # for count in range(1, 24):
    #     try:
    #         for position in range(1, 21):
    #             print(no_redbull[f"rnd{count}"][f"{position}"])
    #         print("\n")
    #     except KeyError:
    #         break
    # print(no_redbull)

def main():
    # get_race_info()
    write_race_data()

if __name__ == '__main__':
    main()