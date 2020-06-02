import sqlalchemy as sa
import pandas as pd
from src.plot_helpers import *

engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id

        ''')

df = pd.read_sql(query, engine_local)
df = df.sort_values(by='when')

print(df.groupby('name_enus').count() )

# to_sell = 'Greater Flask of the Currents'
# recipe1 = {'Zin\'anthid':25,
#           'Anchor Weed':10,
#           'Sea Stalk':8,
#           'Greater Flask of the Currents':1
#           }
# recipe2 = {'Zin\'anthid':20,
#           'Anchor Weed':5,
#           'Sea Stalk':5,
#           'Greater Flask of the Currents':1
#           }
# recipe3 = {'Zin\'anthid':20,
#           'Anchor Weed':5,
#           'Sea Stalk':5,
#           'Greater Flask of the Currents':1
#           }
# plot_recipe(df, recipe1, to_sell, all=False, proc=1)
# plot_recipe(df, recipe2, to_sell, all=False, proc=1.25)
# plot_recipe(df, recipe3, to_sell, all=False, proc=1.5)

