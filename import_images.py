import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from googletrans import Translator

# create a translator object
translator = Translator()


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

#index for folders names
folderIndex = 0
# Load the downloaded album links from the file
downloaded_albums = []
if os.path.exists('downloaded_albums.json'):
    with open('downloaded_albums.json', 'r') as f:
        downloaded_albums = json.load(f)
        folderIndex = len(downloaded_albums)

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
        if album_link in downloaded_albums:
            print(f"Skipping album: {album_link} (already downloaded)")
            continue
        driver.execute_script("window.open('"+album_link+"', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Extract the album title from the div with class 'album-title'
        try:
            album_title_div = driver.find_element(By.CLASS_NAME, 'showalbumheader__gallerytitle')
        except NoSuchElementException:
            print("No title found in this album.")
            break
        album_title_ch = album_title_div.text
        try:
            album_title_en = translator.translate(album_title_ch, src='zh-CN', dest='en').text
        except Exception as e:
            print('Translation error:', e)
            album_title_en = album_title_ch
        

        # Create a new directory for the album
        folderIndex += 1
        album_dir = os.path.join('images', f'album_{folderIndex}')
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)

        # Save the album title to a file inside the album directory
        with open(os.path.join(album_dir, 'title.txt'), 'w', encoding='utf-8') as f:
            f.write(album_title_en)

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
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Find the image element and get the value of the data-src attribute
            try:
                image_element = driver.find_element(By.CLASS_NAME, "viewer__img")
            except NoSuchElementException:
                print("No image element in this album.")
                break
            image_url = image_element.get_attribute("src")

            # Download the image
            #first image name it main
            if i == 2:
                filename = os.path.join(album_dir, f'main.png')
            else:
                filename = os.path.join(album_dir, f'{i-1}.png')
            
            driver.get(image_url)
            try:
                image_element = driver.find_element(By.XPATH, '//img')
            except NoSuchElementException:
                print("No img tag in this album.")
                break
            image_element.screenshot(filename)

            # Close the tab and switch back to the main tab
            #driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        #close all tabs including album tab
        for i in range(imageMax+1):
            driver.switch_to.window(driver.window_handles[1])
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
        # Store the downloaded album link in the list
        downloaded_albums.append(album_link)

        # Save the downloaded album links to the file
        with open('downloaded_albums.json', 'w') as f:
            json.dump(downloaded_albums, f)
        

    
# Close the browser
driver.quit()
