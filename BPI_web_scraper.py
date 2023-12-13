import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_bpi_data(year):
    url = f'https://www.espn.com/mens-college-basketball/bpi/_/season/{year}'
    
    # Use Chrome or Firefox driver based on your preference
    driver = webdriver.Firefox()

    try:
        driver.get(url)
        
        onetrust_accept_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        onetrust_accept_btn.click()

        # show_more_anchor = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Show More")]'))
        # )
        show_more_anchor = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Show More")]')))
        # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", show_more_anchor)
        # onetrust_pc_dark = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, 'onetrust-pc-dark-filter ot-fade-in'))
        # )
        # onetrust_pc_dark.click()

        # Click the "Show More" anchor repeatedly until it's no longer clickable
        while show_more_anchor.is_enabled():
            print("Clicking Show More")
            show_more_anchor.click()
            time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        name_table = soup.find('table', {'class': 'Table Table--align-right Table--fixed Table--fixed-left'})
        data_table = soup.find('table', {'class': 'Table Table--align-right'})
        
        if name_table and data_table:
            names = name_table.find_all('span', {'class': 'TeamLink__Name'})
            data_rows = data_table.find_all('tr')

            bpi_data = []

            for i, row in enumerate(data_rows[2:]):  # Skip the header row
                columns = row.find_all(['td', 'th'])
                
                # Check if the number of columns is as expected
                if len(columns) >= 2 and i < len(names):
                    name = names[i].text.strip()
                    bpi_value = columns[1].text.strip()
                    bpi_data.append({'name': name, 'bpi': bpi_value})
                else:
                    print(f"Skipping row with insufficient columns or names in {year}")

            return bpi_data
        else:
            print(f"No data found for {year}")
            return None
    finally:
        driver.quit()

def main():
    for year in range(2008, 2024):
        bpi_data = scrape_bpi_data(year)
        
        if bpi_data:
            print(f"\nYear: {year}")
            for entry in bpi_data:
                print(f"Name: {entry['name']}, BPI: {entry['bpi']}")

if __name__ == "__main__":
    main()
