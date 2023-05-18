import os
import requests
import base64

# Set the WordPress API endpoint URL
wordpress_url = "https://zadexstore.com/wp-json/wp/v2/media"

# Set up the image file path
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "main.png")

# Set the username and password for basic authentication
username = "Sdgamine"
password = "ehPOX4!jqiWEmRIs9HXOnfFs"

# Encode the username and password in base64
credentials = base64.b64encode("{}:{}".format(username, password).encode("utf-8")).decode("utf-8")

# Open the image file and read the contents
with open(image_path, "rb") as f:
    image_data = f.read()

# Set the request headers
headers = {
    "Content-Disposition": "attachment; filename=image.jpg",
    "Content-Type": "image/jpeg",
    "Authorization": "Basic {}".format(credentials)
}

# Make the POST request to upload the image
response = requests.post(wordpress_url, headers=headers, data=image_data)

# Check if the request was successful
if response.status_code == 201:
    # Print the URL of the uploaded image
    image_url = response.json()["guid"]["rendered"]
    print("Image uploaded successfully with URL: {}".format(image_url))
else:
    print("Failed to upload image: {}".format(response.content))