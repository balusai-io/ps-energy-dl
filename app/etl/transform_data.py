from app.utils.logging_init import init_logger
import pandas as pd
import logging
import datetime as dt

init_logger()
units_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\units.csv', header=0, sep=',')
product_data = pd.read_csv(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\energy.csv', header=0, sep=',')


def transforming_data(transform_path, product_data, units_data):
    try:
        sample_data = pd.read_csv(transform_path, header=0, sep=',')
        sample_data.columns = ['ID', 'Well_Name', 'Month', 'crude_oil(m3)', 'natural_gas(km3)', 'other(m3)']
        transpose_data = pd.melt(sample_data, id_vars=['Well_Name', 'Month'],
                                 value_vars=['crude_oil(m3)', 'natural_gas(km3)', 'other(m3)'], var_name='Comodity',
                                 value_name='Value')
        transpose_data[['energy', 'units']] = transpose_data['Comodity'].str.split('(', expand=True)
        transpose_data['units'] = transpose_data['units'].str.replace('[)]', '', regex=True)
        transpose_data['energy_product_id'] = transpose_data.energy.str.lower().map(
            product_data.set_index('energy_product')['ID'])
        transpose_data['energy_unit_id'] = transpose_data.units.str.lower().map(
            units_data.set_index('uom')['unit_of_measure_id'])
        transpose_data['date_created'] = dt.date.today()
        transpose_data = transpose_data.drop('energy', axis=1)
        transpose_data = transpose_data.drop('units', axis=1)
        return transpose_data
    except Exception as e:
        logging.error(e)


transforming_data(r'C:\Users\siri sagi\PycharmProjects\ps-energy-dl\data_folder\csv_file.csv', product_data, units_data)
