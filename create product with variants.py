import requests
import json

# Set the WooCommerce API endpoint URL and keys
woocommerce_url = "https://zadexstore.com/wp-json/wc/v3/products"
consumer_key = "ck_9464c0ec6d02cb5b421d6bd4d8a4a96f6df51eb5"
consumer_secret = "cs_8f5cc4576ae0a6ce66fcd4fbe402bc21e18da437"

product_data = {
    "name": "simple product with variants",
    "type": "variable",
    "regular_price": "35.00",
    "attributes": [
        {
            "name": "SIZE",
            "position": 0,
            "visible": True,
            "variation": True,
            "options": ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        }
    ],
    "variations": []
}


attribute_name = "SIZE"
attribute_options = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

for option in attribute_options:
    variation = {
        "regular_price": "35.00",
        "attributes": [{"name": attribute_name, "option": option}]
    }
    product_data["variations"].append(variation)

headers = {
    "Content-Type": "application/json"
}
data = json.dumps(product_data)
auth = (consumer_key, consumer_secret)

response = requests.post(woocommerce_url, headers=headers, data=data, auth=auth)

if response.status_code == 201:
    product_id = response.json()["id"]
    print("Product created successfully with ID: {}".format(product_id))
else:
    print("Failed to create product: {}".format(response.content))