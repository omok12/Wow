import sqlalchemy as sa
from src.fbp_helpers import *


engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, area52_daily.quantityavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id
        ''')
item = 'Shal\'dorei Silk'
p = ProphetProfit(engine_local, query, item)

# p.make_profit('2020-05-24')
# p.cross_val()
#
# p.plot()
p.make_lists('2020-05-27')

print(p.mabp_random())
print(p.mapb_ucb())
