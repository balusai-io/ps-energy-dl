import sqlalchemy
import pandas as pd
import logging

energy_connection = sqlalchemy.create_engine(f"postgresql://user:password@host:port/database")


meta = sqlalchemy.MetaData()
energy_table = sqlalchemy.Table(
    'energy_table', meta,
    # sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('Well_Name', sqlalchemy.String),
    sqlalchemy.Column('Month', sqlalchemy.DATE),
    sqlalchemy.Column('Comodity', sqlalchemy.String),
    sqlalchemy.Column('Value', sqlalchemy.FLOAT),
    sqlalchemy.Column('energy_product_id', sqlalchemy.INT),
    sqlalchemy.Column('energy_unit_id', sqlalchemy.INT)
)


units_data = pd.read_csv(r'units.csv', header=0, sep=',')
product_data = pd.read_csv(r'energy.csv', header=0, sep=',')


transforming_data(r'csv_file.csv', product_data, units_data)


conn = energy_connection.connect()
meta.create_all(energy_connection)
db_data = energy_table.insert().values(pd.DataFrame(transforming_data(r'csv_file.csv', product_data, units_data)))

result = conn.execute(db_data)
print(result.inserted_primary_key)

query = 'SELECT * FROM energy_table'
df = pd.read_sql(query, energy_connection)
print(df)
