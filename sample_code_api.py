import os
import base64
import requests
import json

# Initialize WooCommerce API client
url = "https://zadexstore.com/wp-json/wc/v3/products"
consumer_key = "ck_9464c0ec6d02cb5b421d6bd4d8a4a96f6df51eb5"
consumer_secret = "cs_8f5cc4576ae0a6ce66fcd4fbe402bc21e18da437"

# Set up the product data
product_data = {
    "name": "New Product",
    "type": "simple",
    "regular_price": "19.99",
    "description": "This is a new product."
}

# Set up the image file path
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "main.png")

# Set up the API headers for the product creation
product_headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode((consumer_key + ":" + consumer_secret).encode("ascii")).decode("ascii")
}

# Set up the API data for the product creation
product_data = {
    "name": "New Product",
    "type": "simple",
    "regular_price": "19.99",
    "description": "This is a new product."
}

# Open the image file and read its contents
with open(image_path, "rb") as image_file:
    # Set up the API data for the image upload
    image_data = {
        "image": image_file
    }

    # Send the API request to upload the image and get its URL
    image_upload_response = requests.post(url + "/images", headers=product_headers, data=product_data, files=image_data)

    # Check the API response and get the image URL
    if image_upload_response.status_code == 201:
        image_url = image_upload_response.json()["src"]
    else:
        print("Image upload failed.")

# Add the image URL to the product data
product_data["images"] = [{"src": image_url, "position": 0}]

# Convert the product data to JSON
payload = json.dumps(product_data)

# Send the API request to create the new product
product_create_response = requests.post(url, headers=product_headers, data=payload)

# Check the API response for the product creation
if product_create_response.status_code == 201:
    print("Product created successfully.")
else:
    print("Product creation failed.")