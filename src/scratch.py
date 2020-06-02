import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt

engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT *
        FROM bliz_api_3676
        WHERE "item.id" = 152510

        ''')

df = pd.read_sql(query, engine_local).sort_values('unit_price')
df['unit_price'] = df['unit_price']/1000
grouped = df.groupby('unit_price').count()
print(grouped)