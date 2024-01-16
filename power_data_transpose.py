#Load Libraries
import pandas as pd
import hashlib

# Define a hash function using hashlib.sha256
def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()


#load data into data frame
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = [2007, 2008, 2009, 2010, 2012, 2013, 2014, 2015,  2016, 2017, 2018, 2019, 2020, 2021, 2022]
fuel_year = pd.DataFrame()
for year in years:
    path = f'data/IntGenByFuel{year}.xls'

    if year < 2009 :
        for month in months :
            fuel_month = pd.read_excel(path, sheet_name=f'{month}{year}', index_col=0, header=None)
            fuel_month['Date'] = fuel_month.index.str.split('-', 1).str[0]
            fuel_month['Fuel'] = fuel_month.index.str.split('-', 1).str[1]
            fuel_year = fuel_year.append(fuel_month)

    elif year == 2009 or year == 2010:
        for month in months :
            fuel_month = pd.read_excel(path, sheet_name=f'{month}{str(year)[-2:]}', index_col=0, header=None)
            fuel_month['Date'] = fuel_month.index.str.split('-', 1).str[0]
            fuel_month['Fuel'] = fuel_month.index.str.split('-', 1).str[1]
            fuel_year = fuel_year.append(fuel_month)

    elif year == 2012:
        for month  in months:
            if month in ['Jan', 'Feb', 'Mar', 'Apr','Jun']:
                fuel_month = pd.read_excel(path, sheet_name=f'{month}{str(year)[-2:]}', index_col=0, header=None)
                fuel_month['Date'] = fuel_month.index.str.split('-', 1).str[0]
                fuel_month['Fuel'] = fuel_month.index.str.split('-', 1).str[1]
                fuel_year = fuel_year.append(fuel_month) 
            else :
                fuel_month = pd.read_excel(path, sheet_name=f'{month}{str(year)[-2:]}', index_col=0, header=None)
                fuel_month['Date'] = fuel_month.index.str.split('_', 1).str[0]
                fuel_month['Fuel'] = fuel_month.index.str.split('_', 1).str[1]
                fuel_year = fuel_year.append(fuel_month) 
        
    elif year == 2013 or year == 2014 or year == 2015:
        for month in months :
            fuel_month = pd.read_excel(path, sheet_name=f'{month}{str(year)[-2:]}', index_col=0, header=None)
            fuel_month['Date'] = fuel_month.index.str.split('_', 1).str[0]
            fuel_month['Fuel'] = fuel_month.index.str.split('_', 1).str[1]
            fuel_year = fuel_year.append(fuel_month) 
    
    elif year == 2016:
        path = f'data/IntGenByFuel{year}.xlsx'
        for month in months:
            fuel_month = pd.read_excel(path, sheet_name=f'{month}{str(year)[-2:]}', index_col=0, header=None)
            fuel_month['Date'] = fuel_month.index.str.split('_', 1).str[0]
            fuel_month['Fuel'] = fuel_month.index.str.split('_', 1).str[1]
            fuel_year = fuel_year.append(fuel_month) 

    elif year > 2016:
        path = f'data/IntGenByFuel{year}.xlsx'
        for month in months:
            fuel_month = pd.read_excel(path, sheet_name=f'{month}', index_col=0, header=None)
            fuel_month['Date'] = fuel_month.index
            fuel_month['Fuel'] = fuel_month.iloc[:, 0]
            fuel_month = fuel_month.drop(fuel_month[fuel_month['Date'] == 'Date'].index)
            fuel_month['Date'] = pd.to_datetime(fuel_month['Date']).dt.date
            fuel_month['Date'] = fuel_month['Date'].astype(str)
            fuel_month['Fuel'] = fuel_month['Fuel'].astype(str)
            # Concatenate 'Date' and 'Fuel' columns with an underscore between them
            fuel_month['New_Index'] = fuel_month['Date'] + '_' + fuel_month['Fuel']
            # Set this new column as the index
            fuel_month.set_index('New_Index', inplace=True)
            fuel_month.drop(fuel_month.columns[0], axis=1, inplace=True)
            fuel_month.drop(fuel_month.columns[0], axis=1, inplace=True)
            rename_dict = {i: i - 2 for i in range(3, 103)}  # Subtracting 2 from each column index
            # Rename the columns
            fuel_month.rename(columns=rename_dict, inplace=True)
            fuel_year = fuel_year.append(fuel_month) 
    
# Drop rows with the index 'DateFuel'
fuel_year = fuel_year.drop('DateFuel')
# Drop rows with the index 'Date - Fuel'
fuel_year = fuel_year.drop('Date - Fuel')
# Drop rows with the index 'Date-Fuel'
fuel_year = fuel_year.drop('Date-Fuel')

#Transpose the data
# Create an empty DataFrame to store transposed rows
full_data = pd.DataFrame()
# Iterate over each row in the original DataFrame
for index, row in fuel_year.iterrows():
    # Remove the current row from the original DataFrame
    if index != 'Date - Fuel' and index != 'DateFuel' :

        modified_df = fuel_year.drop(index)
        fuel_type = row['Fuel']
        fuel_date = row['Date']#.astype(str)
        # Transpose the row and convert it to a DataFrame
        transposed_row = row.transpose()
        transposed_df = pd.DataFrame(transposed_row)

        # Concatenate the transposed row with the modified DataFrame
        #transposed_df = pd.concat([full_data, transposed_row], ignore_index=False)
        transposed_df['Fuel'] = fuel_type
        transposed_df['Date'] = fuel_date
        #transposed_df['Date'] = transposed_df['Date'].astype(str)

        transposed_df = transposed_df.drop('Fuel', axis=0)
        transposed_df = transposed_df.drop('Date', axis=0)

        # Reset the index to ensure that index 0 is present in the columns
        transposed_df.reset_index(drop=True, inplace=True)
        transposed_df.rename(columns={transposed_df.columns[0]: 'Demand'}, inplace=True)
        MWH = transposed_df.loc[0, 'Demand']
        transposed_df['Daily MWH'] = MWH
        # Drop the first row of the DataFrame
        transposed_df.drop(transposed_df.index[0], inplace=True)

        # Reset the index after dropping the first row
        transposed_df.reset_index(drop=True, inplace=True)

        transposed_df['Time'] = pd.to_datetime(transposed_df['Date']) + pd.to_timedelta((transposed_df.groupby('Date').cumcount() * 15), unit='minutes')
        transposed_df['Time'] = transposed_df['Time'].dt.time


        # Combine 'Date', 'Time', and 'Fuel' columns to create a new column 'Combined'
        transposed_df['Combined'] = transposed_df['Date'].astype(str) + transposed_df['Time'].astype(str) + transposed_df['Fuel'].astype(str)
        # Apply the hash function to the 'Combined' column to create a new column 'HashedIndex'
        transposed_df['HashedIndex'] = transposed_df['Combined'].apply(hash_value)

        # Set the 'HashedIndex' column as the DataFrame index
        transposed_df.set_index('HashedIndex', inplace=True)

        full_data = full_data.append(transposed_df, ignore_index=False)

full_data.to_csv('transposed_power_data.csv', index=True)