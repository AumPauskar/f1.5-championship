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




    drivers_list_no_max = {
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
    no_redbull = []

    round_number = check_date()
    # f1 list with no max verstappen 🦁1️⃣
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
    for count in range(0, round_number):
        for position in range(0, 10):
            match position:
                case 0: # winner
                    drivers_list_no_max[no_max[count][position]] += 25
                case 1: # runner up
                    drivers_list_no_max[no_max[count][position]] += 18
                case 2: # podium
                    drivers_list_no_max[no_max[count][position]] += 15
                case 3:
                    drivers_list_no_max[no_max[count][position]] += 12
                case 4:
                    drivers_list_no_max[no_max[count][position]] += 10
                case 5:
                    drivers_list_no_max[no_max[count][position]] += 8
                case 6:
                    drivers_list_no_max[no_max[count][position]] += 6
                case 7:
                    drivers_list_no_max[no_max[count][position]] += 4
                case 8:
                    drivers_list_no_max[no_max[count][position]] += 2
                case 9:
                    drivers_list_no_max[no_max[count][position]] += 1

    # sort dictionary `drivers_list_no_max` by value
    sorted_drivers = dict(sorted(drivers_list_no_max.items(), key=lambda item: item[1], reverse=True))
    # deep copy sorted_drivers into drivers_list_no_max
    drivers_list_no_max = sorted_drivers.copy()
    print(drivers_list_no_max)

    # resetting the dictionary 0️⃣0️⃣0️⃣
    drivers_list_no_redbull = {
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

    # f1 list with no red bull 1️⃣1️⃣🐂🐐1️⃣
    for count in range(1, round_number+1):
        round_results = []
        no_redbull.append(round_results)
        try:
            for position in range(1, 21):
                if (previous_data[f"rnd{count}"][f"{position}"]) not in ["Sergio Perez", "Max Verstappen"]:
                    round_results.append(previous_data[f"rnd{count}"][f"{position}"])
            print("\n\n")
        except KeyError:
            pass

    # calculating points
    for count in range(0, round_number):
        for position in range(0, 10):
            match position:
                case 0: # winner
                    drivers_list_no_redbull[no_redbull[count][position]] += 25
                case 1: # runner up
                    drivers_list_no_redbull[no_redbull[count][position]] += 18
                case 2: # podium
                    drivers_list_no_redbull[no_redbull[count][position]] += 15
                case 3:
                    drivers_list_no_redbull[no_redbull[count][position]] += 12
                case 4:
                    drivers_list_no_redbull[no_redbull[count][position]] += 10
                case 5:
                    drivers_list_no_redbull[no_redbull[count][position]] += 8
                case 6:
                    drivers_list_no_redbull[no_redbull[count][position]] += 6
                case 7:
                    drivers_list_no_redbull[no_redbull[count][position]] += 4
                case 8:
                    drivers_list_no_redbull[no_redbull[count][position]] += 2
                case 9:
                    drivers_list_no_redbull[no_redbull[count][position]] += 1

    # sort dictionary `drivers_list_no_redbull` by value
    sorted_drivers = dict(sorted(drivers_list_no_redbull.items(), key=lambda item: item[1], reverse=True))
    # deep copy sorted_drivers into drivers_list_no_redbull
    drivers_list_no_redbull = sorted_drivers.copy()
    print(drivers_list_no_redbull)
                    

    return drivers_list_no_max, drivers_list_no_redbull

    # f1 with no red bull
    # for count in range(1, 24):
    #     try:
    #         for position in range(1, 21):
    #             print(no_redbull[f"rnd{count}"][f"{position}"])
    #         print("\n")
    #     except KeyError:
    #         break
    # print(no_redbull)

def markdown_return_standings(drivers_list_no_max, drivers_list_no_redbull):
    markdown = "Drivers' championship without Max Verstappen\n"

    # formatting drivers championship without max verstappen
    for position, driver in enumerate(drivers_list_no_max, start=1):
        markdown += f"{position}. {driver} - {drivers_list_no_max[driver]} points\n"

    markdown += "--------------------"
    markdown += "\n\nDrivers' championship without Red Bull\n"

    # formatting drivers championship without red bull drivers
    for position, driver in enumerate(drivers_list_no_redbull, start=1):
        markdown += f"{position}. {driver} - {drivers_list_no_redbull[driver]} points\n"

    markdown += "--------------------"
    markdown += "\n\nNote: Fastest lap points are not included in the standings\n"
    return markdown

def main():
    # get_race_info()
    drivers_list_no_max, drivers_list_no_redbull = write_race_data()
    print(markdown_return_standings(drivers_list_no_max, drivers_list_no_redbull))
    

if __name__ == '__main__':
    main()