import pandas as pd
import requests
import time
import sqlalchemy as sa
import pickle

class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://us.api.blizzard.com/data/wow/connected-realm/3676/auctions?namespace=dynamic-us&locale=en_US&access_token=USrWWWXoWzxPsa30tENXiinHEg4eH4LniW',
                 db=None):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.last_modified = ''


    def save_to_database(self, data, engine):
        """Save a data row to the database."""
        df = pd.json_normalize(data)[['id', 'quantity', 'unit_price', 'time_left', 'item.id', 'buyout', 'bid']]
        df['last_modified'] = self.last_modified
        df.to_sql('bliz_api_3676', engine, if_exists='append')

    def get_data(self):
        """Fetch data from the API."""
        response = requests.get(self.api_url)
        data = response.json()
        self.last_modified = response.headers['last-modified']
        print(f"Received data at {self.last_modified}")
        return data['auctions']

    def collect(self, interval=3600):
        """Check for new data from the API periodically."""
        engine = sa.create_engine('postgresql://o:password@localhost:5432/wow')
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                self.save_to_database(data, engine)
            else:
                print("No new data received.")
            print("Waiting seconds...")
            time.sleep(interval)


# Usage Example

client = EventAPIClient()
client.collect()