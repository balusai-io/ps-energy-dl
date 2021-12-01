import os
import sqlalchemy as sqlalchemy
from dotenv import load_dotenv
import logging

load_dotenv()


def db_connection():
    try:
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        database = os.getenv('DATABASE')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        en_connection = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
        return en_connection
    except Exception as e:
        logging.error(e)


db_connection()
