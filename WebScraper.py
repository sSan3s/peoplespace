import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

base_url = "https://www.gunviolencearchive.org/reports/number-of-gun-deaths"
result_list = []  # List to store the collected results
processed_incident_ids = set()  # Set to store processed incident IDs

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Iterate through pages
    while True:
        driver.get(base_url)
        time.sleep(2)

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, features='html.parser')

        # Find all <td> tags
        equal = soup.find_all('tr', 'odd')
        equal = equal + soup.find_all('tr', 'even')

        if equal:
            # Iterate through each <tr> element
            for elem in equal:
                # Extract incident ID
                incident_id = elem.find_next('td').text.strip()

                # Check if incident ID is already processed
                if incident_id not in processed_incident_ids:
                    # Add incident ID to set
                    processed_incident_ids.add(incident_id)

                    # Extract data from <td> tags and populate the result_list
                    result_list.append({
                        'incident_id': incident_id,
                        'incident_date': elem.find_next('td').find_next('td').text.strip(),
                        'state': elem.find_next('td').find_next('td').find_next('td').text.strip(),
                        'city_or_county': elem.find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'address': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'victims_killed': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'victims_injured': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'suspects_killed': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'suspects_injured': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip(),
                        'suspects_arrested': elem.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text.strip()
                    })

        # Find the next page link
        next_page = soup.find('li', class_='pager-next')
        if next_page:
            next_page_link = next_page.find('a')['href']
            base_url = f"https://www.gunviolencearchive.org{next_page_link}"
        else:
            break  # Exit the loop if there is no next page

except NoSuchElementException as e:
    print(f"Element not found: {e}")

finally:
    # Quit the WebDriver
    driver.quit()

# Save the result_list to a CSV file
csv_filename = 'gun_violence_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['incident_id', 'incident_date', 'state', 'city_or_county', 'address', 'victims_killed', 'victims_injured', 'suspects_killed', 'suspects_injured', 'suspects_arrested']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()

    # Write data
    for result in result_list:
        writer.writerow(result)

print(f'Data saved to {csv_filename}')
