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

#update these drop? so that the daylight savings records are not dropped 
dls = [
    '03-11-07', '11-04-07',
    '03-09-08', '11-02-08',
    '03-08-09', '11-01-09',
    '03-14-10', '11-07-10',
    '03-13-11', '11-06-11',
    '03-11-12', '11-04-12',
    '03-10-13', '11-03-13',
    '03-09-14', '11-02-14',
    '03-08-15', '11-01-15',
    '03-13-16', '11-06-16',
    '03-12-17', '11-05-17',
    '03-11-18', '11-04-18',
    '03-10-19', '11-03-19',
    '03-08-20', '11-01-20',
    '03-14-21', '11-07-21',
    '03-13-22', '11-06-22'
]

date_std.loc[date_std['Date'].isin(dls), 'drop?'] = 'N'

# drop records with drop? value of N
filtered_df = date_std[date_std['drop?'] != 'Y']

filtered_df.to_csv('clean_power_data.csv', index=True)