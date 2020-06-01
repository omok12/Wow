import sqlalchemy as sa
import pandas as pd


def tuj_to_local(query_tuj, target_table):
    engine_tuj = sa.create_engine('mysql://@newswire.theunderminejournal.com/newsstand')
    df = pd.read_sql(query_tuj, engine_tuj)
    engine_local = sa.create_engine('postgres://o:password@localhost/wow')
    df.to_sql(target_table, engine_local)