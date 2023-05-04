import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


#ask user for link
link = input("Please enter the website link: ")

#ask user for max images
imageMaxNumber = input("Please enter the max images number: ")


#config
imageMax = int(imageMaxNumber)
globalImageMax = imageMax

# Create a new directory to store the downloaded images
if not os.path.exists('images'):
    os.makedirs('images')

# Start a new Selenium session
driver = webdriver.Chrome()

for i in range(1, 10):
    # Set the website URL you want to download images from
    url = f"{link}albums?tab=gallery&page={i}"

    # Navigate to the website URL
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Find all album links on the page
    album_items = driver.find_elements(By.XPATH, "//div[@class='showindex__children']//a[@class='album__main']")
    album_links = [item.get_attribute("href") for item in album_items]

    # Loop through each album link and download all images in the album
    for album_link in album_links:
        driver.execute_script("window.open('"+album_link+"', '_blank');")
        time.sleep(2)  # Wait for the album page to load
        driver.switch_to.window(driver.window_handles[1])

        # Extract the album title from the div with class 'album-title'
        album_title_div = driver.find_element(By.CLASS_NAME, 'showalbumheader__gallerytitle')
        album_name = album_title_div.text.strip().replace('/', '_') # replace any / with _

        # Create a new directory for the album
        album_dir = os.path.join('images', album_name)
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)

        # Get all data-ids of the images in the album
        try:
            images = driver.find_elements(By.CLASS_NAME, "showalbum__children")
        except NoSuchElementException:
            print("No images found in this album.")
            break
        
        data_ids = [image.get_attribute("data-id") for image in images]

        if len(data_ids) < imageMax:
            imageMax = len(data_ids)
        else:
            imageMax = globalImageMax

        new_data_ids = data_ids[-imageMax:]

        # Construct URLs for full-sized images and open them in new tabs
        for index, data_id in enumerate(new_data_ids):
            if index < imageMax:
                image_url = f"{link}{data_id}?uid=1"
                driver.execute_script("window.open('"+image_url+"', '_blank');")
            else:
                break

        # Switch to each new tab and download the image
        # for i in range(2, len(data_ids)+2):
        for i in range(2, imageMax+2):
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[i])
            time.sleep(2)  # Wait for the page to load

            # Find the image element and get the value of the data-src attribute
            image_element = driver.find_element(By.CLASS_NAME, "viewer__img")
            image_url = image_element.get_attribute("src")

            # Download the image
            #first image name it main
            if i == 2:
                filename = os.path.join(album_dir, f'main.png')
            else:
                filename = os.path.join(album_dir, f'{i-1}.png')
            
            driver.get(image_url)
            image_element = driver.find_element(By.XPATH, '//img')
            image_element.screenshot(filename)

            # Close the tab and switch back to the main tab
            #driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)  # Wait for the page to load

        #close all tabs including album tab
        for i in range(imageMax+1):
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        

    
# Close the browser
driver.quit()
