import pandas as pd

def sort_by_month(file):
    df = pd.read_csv(file)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B %Y')

    monthly_data = {}

    for month, group in df.groupby('Month', sort=False):
        # Convert each month’s transactions to dictionaries
        monthly_data[month] = group.drop(columns=['Month']).to_dict(orient='records')

    return monthly_data

def group_by_category(monthly_data):
    service_map = {}

    for month, transactions in monthly_data.items():
        for tx in transactions:
            if tx["Category"] == "Withdrawal":
                service = tx["Service"]
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(tx)

    return service_map
