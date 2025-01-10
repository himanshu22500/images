import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse


def download_images(url, download_folder='downloaded_images'):
    # Create download directory if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Set up Selenium WebDriver (Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode if you don't want to see the browser
    driver = webdriver.Chrome(options=options)

    try:
        # Load the webpage
        driver.get(url)

        # Wait for images to load (adjust timeout as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))

        # Additional wait to ensure dynamic content is loaded
        time.sleep(3)

        # Get page source after JavaScript execution
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all image elements
        images = soup.find_all('img')

        # Download each image
        for i, img in enumerate(images):
            # Get image source URL
            img_url = img.get('src')

            # Skip if no source found
            if not img_url:
                continue

            # Make URL absolute if it's relative
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(url, img_url)

            try:
                # Download the image
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    # Extract file extension from URL or default to .jpg
                    file_extension = os.path.splitext(img_url)[1]
                    if not file_extension:
                        file_extension = '.jpg'

                    # Create filename
                    filename = f'image_{i}{file_extension}'
                    filepath = os.path.join(download_folder, filename)

                    # Save the image
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(f'Successfully downloaded: {filename}')

            except Exception as e:
                print(f'Error downloading image {img_url}: {str(e)}')

    finally:
        # Clean up
        driver.quit()


if __name__ == "__main__":
    # Example usage
    url = "https://www.exmark.com/mowers/stand-on/vertex/vertex-x-series/vxx999eka60600"
    download_images(url)
