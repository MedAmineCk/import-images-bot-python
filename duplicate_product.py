import requests
import json

# Set up authentication and base URL
consumer_key = "ck_9464c0ec6d02cb5b421d6bd4d8a4a96f6df51eb5"
consumer_secret = "cs_8f5cc4576ae0a6ce66fcd4fbe402bc21e18da437"
base_url = 'https://zadexstore.com/wp-json/wc/v3'

def duplicate_variable_product(product_id):
    # Get the original product data
    response = requests.get(
        f'{base_url}/products/{product_id}',
        auth=(consumer_key, consumer_secret)
    )
    original_product = response.json()

    # Remove unnecessary fields
    del original_product['id']
    del original_product['date_created']
    del original_product['date_modified']
    del original_product['permalink']

    # Duplicate the product
    response = requests.post(
        f'{base_url}/products',
        auth=(consumer_key, consumer_secret),
        data=json.dumps(original_product),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 201:
        duplicated_product = response.json()
        return duplicated_product
    else:
        print(f'Failed to duplicate product. Status code: {response.status_code}')
        return None

# Usage example
product_id = 11351  # Replace with the ID of the variable product
duplicated_product = duplicate_variable_product(product_id)

if duplicated_product:
    duplicated_product_id = duplicated_product['id']

    # Get the original product's variations
    response = requests.get(
        f'{base_url}/products/{product_id}/variations',
        auth=(consumer_key, consumer_secret)
    )
    variations = response.json()

    # Duplicate each variation and assign it to the duplicated product
    for variation in variations:
        del variation['id']
        del variation['date_created']
        del variation['date_modified']
        variation['product_id'] = duplicated_product_id

        response = requests.post(
            f'{base_url}/products/{duplicated_product_id}/variations',
            auth=(consumer_key, consumer_secret),
            data=json.dumps(variation),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 201:
            print(f'Failed to duplicate variation. Status code: {response.status_code}')

