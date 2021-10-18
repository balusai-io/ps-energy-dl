import pandas as pd

def unpivoting_data(sample_path):
    sample_data = pd.read_csv(sample_path, header=0, sep=',').head(28)
    s_data = sample_data.rename(
        columns={'Oil (m3)': 'crude_oil (m3)', 'Gas (103m3)': 'natural_gas (km3)', 'Water (m3)': 'other (m3)',
                 'value': 'Value'}, inplace=False)
    s_data.drop(['Unnamed: 5'], axis='columns', inplace=True)
    transpose_data = s_data.melt(['well_name', 'month'], var_name='Comodity', value_name='Value').head(84)
    transpose_data.sort_values(by=["well_name", "month"], inplace=True)
    transpose_data['energy'] = transpose_data['Comodity'].str.split(' ', 0).str[0]
    transpose_data['units'] = transpose_data['Comodity'].str.split(' ', 1).str[1]
    return print(transpose_data)


unpivoting_data(r"../../Sample data file - hib_oil_2005-page-1-table-2.csv")
