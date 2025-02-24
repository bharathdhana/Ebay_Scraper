from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Function to scrape product details from eBay search results
def scrape_ebay_product_by_name(product_name):
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
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.s-item")))

    # Find the first product listing
    try:
        first_listing = driver.find_element(By.CSS_SELECTOR, "li.s-item")
        product_link = first_listing.find_element(By.CSS_SELECTOR, "a.s-item__link").get_attribute("href")
    except Exception as e:
        print(f"Error finding the first listing: {e}")
        driver.quit()
        return

    # Navigate to the product page
    driver.get(product_link)

    # Wait for the product page to load
    time.sleep(3)

    # Initialize a dictionary to store the scraped data
    product_details = {}

    try:
        # Extract product title
        product_details["Title"] = driver.find_element(By.CSS_SELECTOR, "h1.x-item-title__mainTitle").text.strip()
    except:
        product_details["Title"] = "N/A"

    try:
        # Extract product price
        product_details["Price"] = driver.find_element(By.CSS_SELECTOR, "div.x-price-primary span.ux-textspans").text.strip()
    except:
        product_details["Price"] = "N/A"

    try:
        # Extract product description
        product_details["Description"] = driver.find_element(By.CSS_SELECTOR, "div.d-item-description").text.strip()
    except:
        product_details["Description"] = "N/A"

    try:
        # Extract seller information
        product_details["Seller"] = driver.find_element(By.CSS_SELECTOR, "div.ux-seller-section__item--seller a.ux-seller-section__link").text.strip()
    except:
        product_details["Seller"] = "N/A"

    try:
        # Extract seller rating
        product_details["Seller Rating"] = driver.find_element(By.CSS_SELECTOR, "div.ux-seller-section__item--seller span.ux-seller-section__rating-count").text.strip()
    except:
        product_details["Seller Rating"] = "N/A"

    try:
        # Extract product condition
        product_details["Condition"] = driver.find_element(By.CSS_SELECTOR, "div.x-item-condition-text div.ux-textspans").text.strip()
    except:
        product_details["Condition"] = "N/A"

    try:
        # Extract product image URL
        product_details["Image URL"] = driver.find_element(By.CSS_SELECTOR, "div.image-viewer img").get_attribute("src")
    except:
        product_details["Image URL"] = "N/A"

    try:
        # Extract product specifications (if available)
        specifications = {}
        spec_elements = driver.find_elements(By.CSS_SELECTOR, "div.ux-layout-section-evo__item")
        for spec in spec_elements:
            try:
                key = spec.find_element(By.CSS_SELECTOR, "div.ux-labels-values__labels").text.strip()
                value = spec.find_element(By.CSS_SELECTOR, "div.ux-labels-values__values").text.strip()
                specifications[key] = value
            except:
                continue
        product_details["Specifications"] = specifications
    except:
        product_details["Specifications"] = "N/A"

    # Close the WebDriver
    driver.quit()

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame([product_details])

    # Save the DataFrame to a CSV file
    df.to_csv(f"ebay_product_{product_name.replace(' ', '_')}.csv", index=False)
    print(f"Scraping completed! Data saved to 'ebay_product_{product_name.replace(' ', '_')}.csv'")

# Main function
if __name__ == "__main__":
    # Get user input for the product name
    product_name = input("Enter the product name to search on eBay: ").strip()

    # Call the scraping function
    scrape_ebay_product_by_name(product_name)