from simple_salesforce import Salesforce
import requests
import os

# Salesforce OAuth2 configuration
CLIENT_ID = os.environ.get('ROUND_2_SALESFORCE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('ROUND_2_SALESFORCE_CLIENT_SECRET')
USERNAME = os.environ.get('ROUND_2_SALESFORCE_USERNAME')
PASSWORD = os.environ.get('ROUND_2_SALESFORCE_PASSWORD')
SECURITY_TOKEN = os.environ.get('ROUND_2_SALESFORCE_SECURITY_TOKEN')
AUTH_URL = os.environ.get('ROUND_2_SALESFORCE_AUTH_URL')


# Function to obtain the access token
def get_salesforce_token():
    try:
        data = {
            'grant_type': 'password',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'username': USERNAME,
            'password': PASSWORD + SECURITY_TOKEN,
        }
        response = requests.post(AUTH_URL, data=data)
        response.raise_for_status()
        auth_response = response.json()
        return auth_response['access_token'], auth_response['instance_url']
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain access token: {str(e)}")
        return None, None


# Function to create or update a contact
def create_or_update_contact(first_name, last_name, email):
    access_token, instance_url = get_salesforce_token()
    if not access_token:
        print("Unable to authenticate with Salesforce")
        return None

    try:
        # Initialize Salesforce connection with the access token
        sf = Salesforce(instance_url=instance_url, session_id=access_token)

        # Query to check if the contact exists based on the email
        existing_contact = sf.query(f"SELECT Id FROM Contact WHERE Email = '{email}'")

        if existing_contact['totalSize'] > 0:
            # Contact exists, update it
            contact_id = existing_contact['records'][0]['Id']
            sf.Contact.update(contact_id, {
                'FirstName': first_name,
                'LastName': last_name
            })
            print(f"Contact updated with ID: {contact_id}")
            return contact_id
        else:
            # Contact does not exist, create it
            new_contact = sf.Contact.create({
                'FirstName': first_name,
                'LastName': last_name,
                'Email': email
            })
            print(f"Contact created with ID: {new_contact['id']}")
            return new_contact['id']

    except Exception as e:
        print(f"Failed to create or update contact: {str(e)}")
        return None
