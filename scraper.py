import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://www.formula1.com/en/results.html/2024/races/1229/bahrain/race-result.html'

# Send an HTTP request to the URL
response = requests.get(url)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find_all('tr')
driver_positions = []

cells = soup.find_all('tr')
values = []

for row in rows:
    # Find the <td> element with class="dark" in the row
    driver_position = row.find('td', class_='dark')
    if driver_position:
        # Append the text content of the driver_position to the list
        driver_positions.append(driver_position.text.strip())

for cell in cells:
    bold_cell = cell.find('td', class_='bold')
    # Append the text content of the cell to the list
    if bold_cell:
        values.append(cell.text.strip())

print(driver_positions)
print(values)