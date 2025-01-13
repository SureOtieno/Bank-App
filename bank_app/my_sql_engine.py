from sqlalchemy import create_engine
import pandas as pd
import oracledb
import os
from dotenv import load_dotenv

def my_engine():
    load_dotenv()
    oracle_conn_string = os.getenv('ORACLE_CONN_STRING')


    try:
        engine = create_engine(oracle_conn_string, echo=True)
        # engine = create_engine(f"{oracle_conn_string}")
        with engine.connect() as conn:
            print('Connected to Oracle DB successfully')
    except oracledb.DatabaseError as e:
        print(f'Could not make a connection to the database. {e}')

    return engine
