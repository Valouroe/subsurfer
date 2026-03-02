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
                tx['Amount'] = abs(tx['Amount'])
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(tx)

    return service_map

def subscription_by_service(service_map):
    subscriptions = {}
    pending_trackers = {} 
    history = {} 

    all_tx = [tx for transactions in service_map.values() for tx in transactions]
    start_date = min(tx['Date'] for tx in all_tx)
    end_date = max(tx['Date'] for tx in all_tx)

    # Loop through all transactions
    for tx in all_tx:
        name = tx["Merchant Name"]
        date = tx["Date"]
        amount = tx["Amount"]

        # If service not seen before, start tracking it
        if name not in history:
            history[name] = [{"Date": date, "Amount": amount}]
            continue
        
        # Check against previous transactions for this service
        for prev_tx in reversed(history[name]):
            prev_amt = prev_tx["Amount"]
            days_diff = (date - prev_tx["Date"]).days

            same_amount = (amount >= prev_amt * 0.90 and amount <= prev_amt * 1.10) # Allow 10% variance in amount
            
            is_weekly = (6 <= days_diff <= 8) # Allow 1 day off for weekly
            is_monthly = (27 <= days_diff <= 33) # Allow 3 days off for monthly
            is_yearly = (360 <= days_diff <= 370) # Allow 10 days off for yearly

            # If we see a potential subscription pattern, start or update the pending tracker
            if (is_monthly or is_weekly or is_yearly) and same_amount:
                interval = "Monthly" if is_monthly else "Weekly" if is_weekly else "Yearly"
                
                if name not in pending_trackers:
                    pending_trackers[name] = {
                        "Payment": amount,
                        "Total": prev_amt + amount,
                        "Streak": 2, 
                        "Interval": interval,
                        "Last_Date": date # Store this for the next payment calc
                    }
                else:
                    pending_trackers[name]["Streak"] += 1
                    pending_trackers[name]["Total"] += amount
                    pending_trackers[name]['Total'] = round(pending_trackers[name]['Total'], 2) # Round to 2 decimals
                    pending_trackers[name]["Payment"] = amount
                    pending_trackers[name]["Last_Date"] = date

                # Confirmation Logic
                if is_yearly or pending_trackers[name]["Streak"] >= 3:
                    subscriptions[name] = pending_trackers[name]
                
                break
        
        history[name].append({"Date": date, "Amount": amount})
    
    # Loop through subscriptions to calculate next payment date and clean up data
    for name, data in subscriptions.items():
        del data['Streak'] # Remove streak count from final output

        last_date = data['Last_Date'] # Get the last payment date for next payment calculation
        
        # Calculate next payment date based on interval
        if data['Interval'] == 'Weekly':
            next_date = last_date + pd.Timedelta(days=7)
        elif data['Interval'] == 'Monthly':
            next_date = last_date + pd.DateOffset(months=1)
        elif data['Interval'] == 'Yearly':
            next_date = last_date + pd.DateOffset(years=1)
            
        data['Next_Payment'] = next_date.strftime('%Y-%m-%d')
        data['Last_Date'] = last_date.strftime('%Y-%m-%d')
            
    return subscriptions, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')