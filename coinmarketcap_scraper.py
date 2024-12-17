from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize Edge WebDriver
driver = webdriver.Edge()  # No need to specify the path if WebDriver is in the PATH

# Open the CoinMarketCap URL
url = "https://coinmarketcap.com/view/real-world-assets/"
driver.get(url)

# Wait for the page and table to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))

# Scroll to load all rows (optional, adjust range as needed)
for _ in range(10):  # Adjust range to scroll more or less
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1)

# Extract data from the table
projects = []
rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')

for row in rows:
    try:
        title = row.find_element(By.CSS_SELECTOR, '.cmc-table__column-name a').text.strip()
        ticker = row.find_element(By.CSS_SELECTOR, '.cmc-table__cell--sort-by__symbol').text.strip()
        volume = row.find_element(By.CSS_SELECTOR, '.cmc-table__cell--sort-by__volume-24-h').text.strip()
        projects.append({'Title': title, 'Ticker': ticker, '24h Volume': volume})
    except Exception as e:
        print(f"Error extracting data from a row: {e}")

# Close the browser
driver.quit()

# Save the extracted data to an Excel file
df = pd.DataFrame(projects)
df.to_excel("real_world_assets.xlsx", index=False)

print("Scraping completed! Data saved to 'real_world_assets.xlsx'.")
