import sqlalchemy as sa
import pandas as pd
import requests


api_url='https://us.api.blizzard.com/data/wow/connected-realm/3676/auctions?namespace=dynamic-us&locale=en_US&access_token=USrWWWXoWzxPsa30tENXiinHEg4eH4LniW'
response = requests.get(api_url)
data = response.json()['auctions']
last_modified = response.headers['last-modified']
df = pd.json_normalize(data)[['id', 'quantity', 'unit_price', 'time_left', 'item.id', 'buyout', 'bid']]
df['last_modified'] = last_modified
print(df.head())
print(last_modified)