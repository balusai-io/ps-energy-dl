import sqlalchemy as sqlalchemy
from app.etl.transform_data import transforming_data
from dotenv import load_dotenv
import pandas as pd
from app.utils.db_connectivity import db_connection

load_dotenv()

energy_connection = db_connection()

meta = sqlalchemy.MetaData()
energy_table = sqlalchemy.Table(
    'energy_table', meta,
    # sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('Well_Name', sqlalchemy.String),
    sqlalchemy.Column('Month', sqlalchemy.DATE),
    sqlalchemy.Column('Value', sqlalchemy.FLOAT),
    sqlalchemy.Column('energy_product_id', sqlalchemy.INT),
    sqlalchemy.Column('energy_unit_id', sqlalchemy.INT)
)

meta.create_all(energy_connection)
units_data = pd.read_csv(r'units.csv', header=0, sep=',')
product_data = pd.read_csv(r'energy.csv', header=0, sep=',')

db_data = transforming_data(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\data_folder\csv_file.csv', product_data,
                            units_data)
print(type(db_data))

db_data.to_sql(name='energy_table', schema=meta, con=energy_connection, index=False, if_exists='append',
               dtype={'Well_Name': sqlalchemy.types.String,
                      'Month': sqlalchemy.types.Date,
                      'Value': sqlalchemy.types.FLOAT,
                      'energy_product_id': sqlalchemy.types.Integer,
                      'energy_unit_id': sqlalchemy.types.Integer})

query = 'SELECT * FROM energy_table'
df = pd.read_sql(query, energy_connection)
print(df)
