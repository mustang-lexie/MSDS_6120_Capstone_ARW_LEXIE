#import libraries
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

file_path = 'transposed_power_data.csv'

data = pd.read_csv(file_path)


date_std = data.replace(to_replace='/', value='-', regex=True)


# Convert 'Date' column to datetime objects
date_std['Date'] = pd.to_datetime(date_std['Date'])

# Convert back to the desired string format 'mm-dd-yy'
date_std['Date'] = date_std['Date'].dt.strftime('%m-%d-%y')

#get the number of rows
n = len(date_std)

#count to 101 then repeat
count_column = [(i % 101) + 1 for i in range(n)]

#create a new column for the count
date_std['Day_Count'] = count_column

#need to drop 97 - 101

#label records that need to be dropped
date_std['drop?'] = np.where(date_std['Day_Count'] > 96, 'Y', 'N')

# drop records with drop? value of N
filtered_df = date_std[date_std['drop?'] != 'Y']

# make names uniform
filtered_df["Fuel"] = filtered_df["Fuel"].replace(' Coal', 'Coal')
filtered_df["Fuel"] = filtered_df["Fuel"].replace(' Gas', 'Gas')
filtered_df["Fuel"] = filtered_df["Fuel"].replace(' Hydro', 'Hydro')
filtered_df["Fuel"] = filtered_df["Fuel"].replace(' Nuclear', 'Nuclear')
filtered_df["Fuel"] = filtered_df["Fuel"].replace(' Wnd', 'Wind')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Oth', 'Other')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Wnd', 'Wind')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Gas_CC', 'Gas')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Gas_GT', 'Gas')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Sun', 'Solar')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('Gas-CC', 'Gas')
filtered_df["Fuel"] = filtered_df["Fuel"].replace('WSL', 'Wind')

# Specify the path for the weather data
excel_file_path = 'data/Capstone_Weather_Data_Long_Format.xlsx'

# Specify the sheet name
sheet_name = 'Combined'

# Use pandas to read the Excel file and create a DataFrame from a specific sheet
df_weather = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Conver the date fields to a common format
df_weather['Date'] = pd.to_datetime(df_weather['Date'], format = '%m/%d/%y')

# Assuming df is your DataFrame with a date column 'Date'
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')

# Perform the join on the common date field
merged_df = pd.merge(filtered_df, df_weather, on='Date')

#Lets remove these records before proceeding
mask = merged_df['Demand'] == '1-0-1900 0:00'
imp_df = merged_df[-mask]

#Make Demand back to a float character
imp_df['Demand'] = imp_df['Demand'].astype(float)

#drop null values
imp_df = imp_df.dropna()

imp_df = imp_df.drop(columns=['drop?', 'Day_Count'])

#save clean data to csv
imp_df.to_csv('clean_data.csv', index=True)