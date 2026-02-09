import pandas as pd

#Reads the csv file
file_name = file_name = r'c:/Users/isaac/OneDrive/Desktop/SE-Project/subsurfer/tests/test-csv/test-Statement.csv'
df = pd.read_csv(file_name)

#this sorts throught the data and breaks it up by months 
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.strftime('%B %Y')
grouped = df.groupby('Month', sort=False)

#Print out the sorted data
for month, group in grouped:
    print(f"\n--- {month} ---")
    print(group.drop(columns=['Month']).to_string(index=False))