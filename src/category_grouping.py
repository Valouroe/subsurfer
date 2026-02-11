import pandas as pd

def group_by_category(monthly_data):
    service_map = {}

    for month, transactions in monthly_data.items():
        for tx in transactions:
            if tx["category"] == "withdrawal":
                service = tx["service"]
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(tx)

    return service_map

def sort_by_month(file):
    #Reads the csv file
    df = pd.read_csv(file)

    #this sorts throught the data and breaks it up by months 
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B %Y')
    grouped = df.groupby('Month', sort=False)

    #Print out the sorted data
    for month, group in grouped:
        print(f"\n--- {month} ---")
        print(group.drop(columns=['Month']).to_string(index=False))
    return grouped
