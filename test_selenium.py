from selenium import webdriver
from selenium.webdriver.edge.service import Service

service = Service("C:\\WebDriver\\msedgedriver.exe")  # Replace with your WebDriver path
driver = webdriver.Edge(service=service)

driver.get("https://www.google.com")
print("Selenium is working!")
driver.quit()
