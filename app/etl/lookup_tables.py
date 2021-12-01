import logging
from app.etl.extraction import extraction
import sqlalchemy as sqlalchemy
import os
import pandas as pd
from dotenv import load_dotenv
from app.utils.db_connectivity import db_connection
import json
import datetime as dt


load_dotenv()
energy_connection = db_connection()
meta = sqlalchemy.MetaData()
filters = os.getenv('REFERENCE').split(',')
folder_path = os.getenv('FOLDER_PATH')
data_path = os.path.join(folder_path + '//' + 'data_folder')


def field_table(filters):
    try:
        for filter in filters:
            field_table = sqlalchemy.Table('field_table', meta,
                                           sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                                           sqlalchemy.Column('field_name', sqlalchemy.String(15)),
                                           sqlalchemy.Column('date_created', sqlalchemy.DateTime(), default=dt.date.today())
                                           )
            meta.create_all(energy_connection)
            field = json.loads(os.getenv('FIELDS'))[filter]
            print(field)
            if field not in field_table.field_name.values:
                query = f"INSERT INTO field_table(field_name) VALUES ('{field}')"
                energy_connection.execute(query)
    except Exception as e:
        logging.error(e)


def well_table(filters):
    try:
        for filter in filters:
            field = json.loads(os.getenv('FIELDS'))[filter]
            for item in field:
                transform_path = extraction(data_path, item)
                well_data = pd.read_csv(transform_path, header=0, sep=',')
                well_list = sorted(list(set(well_data['Well Name'])))
                well_table = sqlalchemy.Table('well_table', meta,
                                              sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                                              sqlalchemy.Column('field_id', sqlalchemy.Integer),
                                              sqlalchemy.Column('well_name', sqlalchemy.String(20)),
                                              sqlalchemy.Column('date_created', sqlalchemy.DateTime(), default=dt.date.today()))
                meta.create_all(energy_connection)
                for i in well_list:
                    if i not in well_table.well_name.values:
                        query = f"INSERT INTO well_table(well_name) VALUES ('{i}')"
                        energy_connection.execute(query)
    except Exception as e:
        logging.error(e)