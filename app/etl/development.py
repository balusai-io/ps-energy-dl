import os
import pandas as pd
from app.etl.Downloading_the_data_files import providing_path
from app.etl.extraction import extraction
from app.etl.transform_data import transforming_data
from app.utils.logging_init import init_logger
import json
import logging

filters = os.getenv('REFERENCE').split(',')
folder_path = os.getenv('FOLDER_PATH')
data_path = os.path.join(folder_path + '//' + 'data_folder')
init_logger()
units_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\units.csv', header=0, sep=',')
product_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\energy.csv', header=0, sep=',')


def data_inserted():
    try:
        providing_path(filters, data_path)
        for filter in filters:
            field = json.loads(os.getenv('FIELDS'))[filter]
            for item in field:
                transform_path = extraction(data_path)
                transforming_data(transform_path, product_data, units_data)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    data_inserted()
