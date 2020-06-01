import mysql.connector
import sqlalchemy as sa
import pandas as pd
from src.import_helpers import *
# conn = mysql.connector.connect(user='', password='', host='newswire.theunderminejournal.com', database='newsstand')
# cur = conn.cursor()
#
# query = ("SELECT * FROM tblWowToken")
# cur.execute(query)
# print(cur.fetchone())


query_tuj = ('''SELECT *
            FROM tblItemHistoryDaily
            WHERE house = 15 AND 'when' >= '2018-08-14'
        ''')

target_table = 'area52_daily'

# area-52 house = 15
tuj_to_local(query_tuj, target_table)