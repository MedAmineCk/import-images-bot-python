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

# Encode the WordPress API credentials in base64
wordpress_credentials = base64.b64encode("{}:{}".format(wordpress_username, wordpress_password).encode("utf-8")).decode("utf-8")
# Set the request headers and data for uploading the image to WordPress
wordpress_headers = {
    "Content-Disposition": "attachment; filename=image.jpg",
    "Content-Type": "image/jpeg",
    "Authorization": "Basic {}".format(wordpress_credentials)
}

# Get the absolute path of the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the folder containing the albums relative to the script directory
albums_path = os.path.join(script_dir, "images")

# Product ID to duplicate
product_id = 11351

# Get product data
url = f"{woocommerce_url}/{product_id}"
response = requests.get(url, auth=(consumer_key, consumer_secret))
if response.status_code != 200:
    print(f"Error retrieving product data: {response.json()}")
    exit()
product_data = response.json()

# Remove the original product ID from the data
del product_data["id"]
product_data["images"] = []
product_data["status"] = "draft"

# Generate variations based on attributes
attributes = product_data["attributes"]
variations = [[]]

for attribute in attributes:
    new_variations = []
    for variation in variations:
        for option in attribute["options"]:
            new_variation = variation + [{"name": attribute["name"], "option": option}]
            new_variations.append(new_variation)
    variations = new_variations

# Iterate over each album folder
for album_name in os.listdir(albums_path):
    album_path = os.path.join(albums_path, album_name)
    
    # Read the album title from the title.txt file
    title_file_path = os.path.join(album_path, "title.txt")
    with open(title_file_path, "r") as title_file:
        album_title = title_file.read().strip()
    
    # Create a slug from the album title
    album_slug = album_title.lower().replace(" ", "-")

    product_data["name"] = album_title
    product_data["variations"] = []
    
    # Upload thumbnail image
    thumbnail_path = os.path.join(album_path, "main.png")
    
    # Open the image file and read the contents
    with open(thumbnail_path, "rb") as f:
        image_data = f.read()
    
    wordpress_data = image_data

    # Make the POST request to upload the image to WordPress
    wordpress_response = requests.post(wordpress_url, headers=wordpress_headers, data=wordpress_data)
    
    # Check if the request was successful
    if wordpress_response.status_code == 201:
        # Get the URL of the uploaded image
        image_url = wordpress_response.json()["guid"]["rendered"]
        print("Main image uploaded successfully with URL: {}".format(image_url))
        # Set the product image URL in the product data
        product_data["images"].append({
            "src": image_url,
            "position": 0
        })
    else:
        print("Failed to upload main image: {}".format(wordpress_response.content))
        
    # Loop through the images in the album folder
    position = 1
    for filename in os.listdir(album_path):
        if filename.endswith(".png") and filename != "main.png":
            # Set the image file path
            image_path = os.path.join(album_path, filename)

            # Open the image file and read the contents
            with open(image_path, "rb") as f:
                image_data = f.read()

            # Set the request headers and data for uploading the image to WordPress
            wordpress_headers = {
                "Content-Disposition": "attachment; filename={}".format(filename),
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
                # Add the image URL to the product data
                product_data["images"].append({
                    "src": image_url,
                    "position": position
                })
                position += 1
            else:
                print("Failed to upload image: {}".format(wordpress_response.content))

    # Create variations for the product
    for variation in variations:
        variation_data = {
            "regular_price": "35.00",
            "attributes": variation
        }
        product_data["variations"].append(variation_data)

    # Set the request headers and data for creating the product on WooCommerce
    woocommerce_headers = {
        "Content-Type": "application/json"
    }
    woocommerce_data = json.dumps(product_data)
    woocommerce_auth = (consumer_key, consumer_secret)
    
    # print(woocommerce_data)

    # Make the POST request to create the product on WooCommerce
    woocommerce_response = requests.post(woocommerce_url, headers=woocommerce_headers, data=woocommerce_data, auth=woocommerce_auth)

    # Check if the request was successful
    if woocommerce_response.status_code == 201:
        # Print the ID of the created product
        product_id = woocommerce_response.json()["id"]
        print("Product created successfully with ID: {}".format(product_id))
    else:
        print("Failed to create product: {}".format(woocommerce_response.content))
    
    # Clear the album images from the product data
    product_data["images"] = []
    product_data["variations"] = []
    
    # Print a separator for readability
    print("="*50)
