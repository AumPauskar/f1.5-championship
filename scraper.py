import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://www.formula1.com/en/results.html/2024/races/1229/bahrain/race-result.html'

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