import os
import requests
import base64
import json

# Set the WooCommerce API endpoint URL and keys
woocommerce_url = "https://zadexstore.com/wp-json/wc/v3/products"
consumer_key = "ck_9464c0ec6d02cb5b421d6bd4d8a4a96f6df51eb5"
consumer_secret = "cs_8f5cc4576ae0a6ce66fcd4fbe402bc21e18da437"

# Set the WordPress API endpoint URL and keys
wordpress_url = "https://zadexstore.com/wp-json/wp/v2/media"
wordpress_username = "Sdgamine"
wordpress_password = "ehPOX4!jqiWEmRIs9HXOnfFs"

# Set the product data
product_data = {
    "name": "Example Product",
    "description": "This is an example product.",
    "regular_price": "9.99",
    "categories": [
        {
            "id": 143
        }
    ],
    "images": [
        {
            "src": "",
            "position": 0
        }
    ]
}

# Set up the image file path
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "main.png")

# Encode the WordPress API credentials in base64
wordpress_credentials = base64.b64encode("{}:{}".format(wordpress_username, wordpress_password).encode("utf-8")).decode("utf-8")

# Open the image file and read the contents
with open(image_path, "rb") as f:
    image_data = f.read()

# Set the request headers and data for uploading the image to WordPress
wordpress_headers = {
    "Content-Disposition": "attachment; filename=image.jpg",
    "Content-Type": "image/jpeg",
    "Authorization": "Basic {}".format(wordpress_credentials)
}
wordpress_data = image_data

# Make the POST request to upload the image to WordPress
wordpress_response = requests.post(wordpress_url, headers=wordpress_headers, data=wordpress_data)

# Check if the request was successful
if wordpress_response.status_code == 201:
    # Get the URL of the uploaded image
    image_url = wordpress_response.json()["guid"]["rendered"]
    print("Image uploaded successfully with URL: {}".format(image_url))
    # Set the product image URL in the product data
    product_data["images"][0]["src"] = image_url
else:
    print("Failed to upload image: {}".format(wordpress_response.content))

# Set the request headers and data for creating the product on WooCommerce
woocommerce_headers = {
    "Content-Type": "application/json"
}
woocommerce_data = json.dumps(product_data)
woocommerce_auth = (consumer_key, consumer_secret)

# Make the POST request to create the product on WooCommerce
woocommerce_response = requests.post(woocommerce_url, headers=woocommerce_headers, data=woocommerce_data, auth=woocommerce_auth)

# Check if the request was successful
if woocommerce_response.status_code == 201:
    # Print the ID of the created product
    product_id = woocommerce_response.json()["id"]
    print("Product created successfully with ID: {}".format(product_id))
else:
    print("Failed to create product: {}".format(woocommerce_response.content))