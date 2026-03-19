import pandas as pd
import numpy as np

def sort_by_month(file):
    df = pd.read_csv(file)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B %Y')
    df['Merchant Name'] = df['Merchant Name'].str.split('*').str[0]

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

SUBSCRIPTION_KEYWORDS = ['MEMBERSHIP', 'SUBSCRIPTION', 'ANNUAL', 'PREMIUM', 'PLUS']

def is_blacklisted(name):
    name_upper = name.upper()
    
    # If it looks like a subscription, never blacklist it
    if any(keyword in name_upper for keyword in SUBSCRIPTION_KEYWORDS):
        return False

    blacklist = [
        'SHELL', 'EXXON', 'CHEVRON', 'BP', 'MOBIL', '7-ELEVEN', 'WAWA', 'SPEEDWAY',
        'WALMART', 'TARGET', 'KROGER', 'PUBLIX', 'SAFEWAY', 'ALDI', 'WHOLEFOODS', 'COSTCO',
        'STARBUCKS', 'DUNKIN', 'MCDONALD', 'CHIPOTLE', 'SUBWAY', 'PANERA',
        'UBER', 'LYFT', 'MTA', 'WMATA', 'CLIPPER', 'VENTRA', 'PARKMOBILE',
        'VENMO', 'CASH APP', 'ZELLE', 'PAYPAL', 'ATM', 'OVERDRAFT', 'DMV', 'USPS'
    ]
    return any(word in name_upper for word in blacklist)

def subscription_by_service(service_map):
    subscriptions = {}
    pending_trackers = {} 
    history = {} 
    habits = []

    all_tx = [tx for transactions in service_map.values() for tx in transactions]
    start_date = min(tx['Date'] for tx in all_tx)
    end_date = max(tx['Date'] for tx in all_tx)

    # Search through all transactions
    for tx in all_tx:
        name = tx["Merchant Name"]
        date = tx["Date"]
        amount = tx["Amount"]

        # Skip blacklisted merchants
        if is_blacklisted(name):
            habits.append(name)
            continue
        
        if name in habits:
            continue

        # If we haven't seen this merchant before, start tracking it
        if name not in history:
            history[name] = [{"Date": date, "Amount": amount}]
            continue

        # Check against previous transactions for this merchant
        for prev_tx in reversed(history[name]):
            days_diff = (date - prev_tx["Date"]).days
            
            is_weekly = (6 <= days_diff <= 8)
            is_monthly = (27 <= days_diff <= 33)
            is_yearly = (360 <= days_diff <= 370)

            if is_weekly or is_monthly or is_yearly:
                interval = "Monthly" if is_monthly else "Weekly" if is_weekly else "Yearly"
                
                if name not in pending_trackers and name not in habits:
                    pending_trackers[name] = {
                        "Payment": amount,
                        "Base_Amount": prev_tx["Amount"], # The original price
                        "Hike_Detected": False,
                        "Total": round(prev_tx["Amount"] + amount, 2),
                        "Streak": 2,
                        "Interval": interval,
                        "Streak_Start": prev_tx["Date"],
                        "Last_Date": date,
                        "Amount_History": [prev_tx["Amount"], amount],
                        "Interval_History": [days_diff]
                    }
                else:
                    tracker = pending_trackers[name]
                    
                    # Check for price hikes
                    if amount > (tracker["Base_Amount"] * 1.05): 
                        if not tracker["Hike_Detected"]:
                            tracker["Hike_Detected"] = True
                            tracker["Base_Amount"] = amount # Update base to the new price
                        else:
                            is_habit = True
                            continue
                    
                    tracker["Streak"] += 1
                    tracker["Total"] = round(tracker["Total"] + amount, 2)
                    tracker["Payment"] = amount
                    tracker["Amount_History"].append(amount)
                    tracker["Interval_History"].append(days_diff)
                    tracker["Last_Date"] = date

                tracker = pending_trackers[name]
                if (interval == 'Yearly' or tracker["Streak"] >= 3):
                    amt_history = tracker["Amount_History"]
                    int_history = tracker["Interval_History"]
                    
                    amt_std = np.std(amt_history)
                    int_std = np.std(int_history)
                    amt_mean = np.mean(amt_history)
                    amt_ratio_std = amt_std / amt_mean if amt_mean > 0 else 0
                    
                    # Frequency check
                    days_total = (date - history[name][0]["Date"]).days
                    is_habit = (len(history[name]) / (max(days_total, 1) / 30) > 6)
                    
                    # Variance Check: 
                    # If a Hike was detected, we allow higher amt_ratio_std 
                    # because a price jump naturally inflates the standard deviation.
                    variance_threshold = 0.20 if tracker["Hike_Detected"] else 0.10
                    
                    if not is_habit:
                        total_tx_count = len(history[name]) + 1  # +1 for the current tx
                        if total_tx_count >= tracker["Streak"] * 1.5:
                            is_habit = True

                    if not is_habit:
                        # If there's a large gap before the streak, the pattern is likely coincidental
                        interval_days = 7 if interval == "Weekly" else 30 if interval == "Monthly" else 365
                        days_before_streak = (tracker["Streak_Start"] - history[name][0]["Date"]).days
                        if days_before_streak > interval_days * 2:
                            is_habit = True

                    if not is_habit:
                        if interval == "Weekly":
                            is_habit = (amt_ratio_std > variance_threshold or int_std > 3.0)
                        elif interval == "Monthly":
                            is_habit = (amt_ratio_std > variance_threshold or int_std > 3.0)
                        elif interval == "Yearly":
                            is_habit = (amt_ratio_std > variance_threshold or int_std > 3.0)

                    if not is_habit:
                        subscriptions[name] = tracker
                    else:
                        subscriptions.pop(name, None)
                        print(f"Excluded {name}")
                        habits.append(name)
                
                break
        
        history[name].append({"Date": date, "Amount": amount})
    
    # Final cleanup
    for name, data in list(subscriptions.items()):
        data.pop('Amount_History', None)
        data.pop('Interval_History', None)
        data.pop('Streak', None)
        data.pop('Base_Amount', None)
        data.pop('Hike_Detected', None)
        data.pop('Streak_Start', None)

        last_date = data['Last_Date']
        if data['Interval'] == 'Weekly':
            next_date = last_date + pd.Timedelta(days=7)
        elif data['Interval'] == 'Monthly':
            next_date = last_date + pd.DateOffset(months=1)
        else:
            next_date = last_date + pd.DateOffset(years=1)
            
        data['Next_Payment'] = next_date.strftime('%Y-%m-%d')
        data['Last_Date'] = last_date.strftime('%Y-%m-%d')
            
    return subscriptions, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')