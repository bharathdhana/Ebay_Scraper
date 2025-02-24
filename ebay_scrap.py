from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Function to scrape eBay listings
def scrape_ebay(search_query):
    # Set up Selenium WebDriver with automatic ChromeDriver installation
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Automatically download and install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Define the eBay search URL
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)

    # Find all product listings
    listings = driver.find_elements(By.CSS_SELECTOR, "li.s-item")

    # Initialize a list to store the scraped data
    data = []

    # Loop through each listing and extract relevant information
    for listing in listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, ".s-item__title").text
            price = listing.find_element(By.CSS_SELECTOR, ".s-item__price").text
            link = listing.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")
            data.append([title, price, link])
        except Exception as e:
            # Skip listings with missing data
            print(f"Skipping a listing due to error: {e}")
            continue

    # Close the WebDriver
    driver.quit()

    # Convert the list to a DataFrame
    df = pd.DataFrame(data, columns=["Title", "Price", "Link"])

    # Save the DataFrame to a CSV file
    df.to_csv(f"ebay_listings_{search_query}.csv", index=False)
    print(f"Scraping completed! Data saved to 'ebay_listings_{search_query}.csv'")

# Main function
if __name__ == "__main__":
    # Get user input for the search query
    search_query = input("Enter the product you want to search for on eBay: ").strip()

    # Call the scraping function
    scrape_ebay(search_query)