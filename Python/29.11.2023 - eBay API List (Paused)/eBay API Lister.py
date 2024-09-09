import requests
import base64
import json

# eBay API credentials
CLIENT_ID = 'CLIENT ID'
CLIENT_SECRET = 'CLIENT SECRET'
ACCESS_TOKEN_URL = 'ACCESS_TOKEN_URL'
DRAFT_LISTING_URL = 'ACCESS_TOKEN_URL'

# Function to get OAuth token
def get_oauth_token(client_id, client_secret):
    credentials = f'{client_id}:{client_secret}'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}',
    }
    body = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebay.com/oauth/api_scope',
    }
    response = requests.post(ACCESS_TOKEN_URL, headers=headers, data=body)
    print("OAuth Token Response:", response.json())  # Logging the response
    return response.json().get('access_token')

# Function to create a draft listing
def create_draft_listing(access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    # Example product details - modify according to your product
    product_details = {
        "product": {
            "title": "Example Product Title",
            "description": "Description of the example product.",
            "imageUrls": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
            "aspects": {
                "Brand": ["Example Brand"],
                "Size": ["Medium"]
            }
        },
        "condition": "NEW",
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        },
        "pricingSummary": {
            "price": {
                "currency": "USD",
                "value": "25.00"
            }
        }
    }
    response = requests.post(DRAFT_LISTING_URL, headers=headers, json=product_details)
    print("Draft Listing Response:", response.json())
    return response.json()

# Main function
def main():
    access_token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)
    if access_token:
        print("Successfully obtained access token.")
        create_draft_listing(access_token)
    else:
        print("Failed to obtain access token.")

if __name__ == '__main__':
    main()
