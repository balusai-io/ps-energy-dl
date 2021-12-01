import os
import sqlalchemy
from app.etl.Transforming_data import transforming_data
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


def db_connection(host, port, database, user, password):
    en_connection = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    return en_connection

energy_connection = db_connection(host, port, database, user, password)

energy_schema = [
    "well_name",
    "month",
    "Comodity",
    "Value",
    "energy",
    "units"
]
meta = sqlalchemy.MetaData()

energy_table = sqlalchemy.Table(
   'table', meta,
   sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
   sqlalchemy.Column('well_name', sqlalchemy.String),
   sqlalchemy.Column('month', sqlalchemy.DATE),
   sqlalchemy.Column('Comodity', sqlalchemy.String),
   sqlalchemy.Column('Value', sqlalchemy.FLOAT),
   sqlalchemy.Column('energy', sqlalchemy.String),
   sqlalchemy.Column('units', sqlalchemy.String)
)
meta.create_all(energy_connection)
units_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\units.csv', header=0, sep=',')
product_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\eneryproduct.csv', header=0, sep=',')
data = transforming_data(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\Sample data file - Sheet1.csv', units_data, product_data)
data.to_sql(energy_table, schema=energy_schema, con=energy_connection, index=False, if_exists='replace', method='multi')
# energy_table = sqlalchemy.Table('energy_table', meta, autoload=True, autoload_with=energy_connection)
print(data.columns.keys())