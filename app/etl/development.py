import os
import pandas as pd

from app.etl import lookup_tables
from app.etl.Downloading_the_data_files import providing_path, data_path, filters
from app.etl.extraction import extraction
from app.etl.transform_data import transforming_data, transform_path
from app.utils.logging_init import init_logger
import json
import logging

init_logger()


def data_insert():
    try:
        providing_path(filters, data_path)
        for filter in filters:
            fields = list(json.loads(os.getenv('FIELDS'))[filter])
            for field in fields:
                extraction(data_path)
                extraction['Field Name'] = field
                lookup_tables.update_fields_table(field)
                well_df = extraction[['Well Name', 'Field Name']]

                lookup_tables.update_well_lookup_table(well_df, field)
                transformed_data = transforming_data(transform_path)
                production_table_data.production_update_table(transformed_data)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    data_insert()












