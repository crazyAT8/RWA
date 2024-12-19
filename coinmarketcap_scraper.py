from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize Edge WebDriver
driver_path = "C:\\WebDriver\\msedgedriver.exe"  # Replace this with your EdgeDriver path
service = Service(driver_path)
driver = webdriver.Edge(service=service)

# Open the CoinMarketCap "Real-World Assets" page
url = "https://coinmarketcap.com/view/real-world-assets/"
driver.get(url)

# Wait for the page to load (ensure table data is present)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))

# Scroll to load all rows dynamically
for _ in range(10):  # Adjust range for longer or shorter scrolls
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1)  # Add delay to allow data to load

# Extract data from the table
projects = []  # Store project data here
rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')  # Get all table rows

for row in rows:
    try:
        # Extract Title, Ticker Symbol, and 24h Volume
        title = row.find_element(By.CSS_SELECTOR, '.cmc-table__column-name a').text.strip()
        ticker = row.find_element(By.CSS_SELECTOR, '.cmc-table__cell--sort-by__symbol').text.strip()
        volume = row.find_element(By.CSS_SELECTOR, '.cmc-table__cell--sort-by__volume-24-h').text.strip()

        # Append extracted data to the list
        projects.append({'Title': title, 'Ticker': ticker, '24h Volume': volume})
    except Exception as e:
        print(f"Error extracting data from row: {e}")  # Log errors, if any

# Close the browser
driver.quit()

# Save the extracted data to an Excel file
df = pd.DataFrame(projects)
df.to_excel("real_world_assets.xlsx", index=False)

print("Scraping completed! Data saved to 'real_world_assets.xlsx'.")