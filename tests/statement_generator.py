import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from dateutil.relativedelta import relativedelta

fake = Faker()

def add_subscription(data, name, frequecy, start_date, end_date, base_amount, category, service):
    curr = start_date + timedelta(days=random.randint(0, 6))
    hike = False
    sub = {"name": name, "amt": base_amount, "cat": category, "srv": service}

    while curr <= end_date:
        # 5% chance of a price hike each week, but only once per subscription
        if not hike and random.random() < 0.05:
            sub["amt"] = round(sub["amt"] * random.uniform(1.05, 1.15), 2)
            hike = True
        bill_date = curr
        bill_amt = round(sub["amt"] * random.uniform(0.98, 1.02), 2)
        
        data.append({
            "Date": bill_date.strftime("%Y-%m-%d"),
            "Amount": bill_amt,
            "Merchant Name": f"{sub['name']}*{fake.hexify(text='^^^^', upper=True)}",
            "Service": sub["srv"],
            "Category": sub["cat"],
        })
        # Add variance of up to 1 day to simulate real-life billing fluctuations
        if frequecy == "Weekly":
            curr += timedelta(weeks=1) + timedelta(days=random.choice([-1, 0, 0, 0, 1]))
        elif frequecy == "Monthly":
            curr += relativedelta(months=1) + timedelta(days=random.choice([-1, 0, 0, 0, 1]))
        else: # Yearly
            curr += relativedelta(years=1) + timedelta(days=random.choice([-1, 0, 0, 0, 1]))

def generate_clean_statement():
    folder_name = "tests/test-csv"
    file_path = os.path.join(folder_name, f"generated_account.csv")

    sub_names = []
    data = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 12, 31)

    # Subscriptions
    weekly_subs = [
        {"name": "HELLO FRESH", "amt": -30.00, "cat": "Withdrawal", "srv": "Food"},
        {"name": "NEW YORK TIMES", "amt": -17.00, "cat": "Withdrawal", "srv": "News"},
    ]

    monthly_subs = [
        {"name": "NETFLIX", "amt": -15.99, "cat": "Withdrawal", "srv": "Streaming"},
        {"name": "SPOTIFY", "amt": -10.99, "cat": "Withdrawal", "srv": "Music"},
        {"name": "WSJ", "amt": -38.00, "cat": "Withdrawal", "srv": "News"},
        {"name": "CHAT GPT PLUS", "amt": -20.00, "cat": "Withdrawal", "srv": "Software"},
        {"name": "CRUCNHYROLL", "amt": -9.99, "cat": "Withdrawal", "srv": "Streaming"},
        {"name": "DISNEY+", "amt": -7.99, "cat": "Withdrawal", "srv": "Streaming"},
        {"name": "HULU", "amt": -12.99, "cat": "Withdrawal", "srv": "Streaming"},
        {"name": "AUDIBLE", "amt": -14.95, "cat": "Withdrawal", "srv": "Books"}
    ]

    yearly_subs = [
        {"name": "AMAZON PRIME", "amt": -139.00, "cat": "Withdrawal", "srv": "E-commerce"},
        {"name": "ADOBE CC", "amt": -239.88, "cat": "Withdrawal", "srv": "Software"},
        {"name": "CHESS.COM", "amt": -99.00, "cat": "Withdrawal", "srv": "Gaming"},
        {'name': "COSTCO MEMBERSHIP", "amt": -60.00, "cat": "Withdrawal", "srv": "Retail"}
    ]

    # Randomly decide which subscriptions to include (33% chance each) to create variability in testing
    for sub in weekly_subs:
        if random.random() < 0.33:
            add_subscription(data, sub["name"], "Weekly", start_date, end_date, sub["amt"], sub["cat"], sub["srv"])
            sub_names.append(sub["name"])
    for sub in monthly_subs:
        if random.random() < 0.33:
            add_subscription(data, sub["name"], "Monthly", start_date, end_date, sub["amt"], sub["cat"], sub["srv"])
            sub_names.append(sub["name"])
    for sub in yearly_subs:
        if random.random() < 0.33:
            add_subscription(data, sub["name"], "Yearly", start_date, end_date, sub["amt"], sub["cat"], sub["srv"])
            sub_names.append(sub["name"])

    # Income and Rent
    curr = start_date
    while curr <= end_date:
        data.append({"Date": curr.strftime("%Y-%m-%d"), "Amount": 5000.00, "Category": "Deposit", "Service": "Income", "Merchant Name": "GLOBAL TECH SALARY"})
        data.append({"Date": curr.strftime("%Y-%m-%d"), "Amount": -1850.00, "Category": "Withdrawal", "Service": "Housing", "Merchant Name": "SKYLINE APTS RENT"})
        curr += timedelta(days=30)
    sub_names.append("SKYLINE APTS RENT")

    # Random Noise
    for _ in range(120):
        if random.random() < 0.05:
            # Random ATM deposits
            data.append({
                "Date": fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d"),
                "Amount": round(random.uniform(50.0, 2000.0), 2),
                "Category": "Deposit",
                "Service": "ATM Deposit",
                "Merchant Name": 'ATM'
            })
        else:
            data.append({
                "Date": fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d"),
                "Amount": -round(random.uniform(8.0, 120.0), 2),
                "Category": 'Withdrawal',
                "Service": "Point of Sale",
                "Merchant Name": fake.company().upper()
            })

    # Weekly Habits (Coffee & Groceries)
    curr = start_date
    while curr <= end_date:
        # 1. Target the next Monday (0)
        days_to_monday = (0 - curr.weekday() + 7) % 7
        target_day = curr + timedelta(days=days_to_monday)
        
        # 2. Add Daily Variance of up to 2 days (to simulate real-life behavior)
        variance = random.choice([-1, 0, 1]) + random.choice([-1, 0, 1])
        actual_date = target_day + timedelta(days=variance)
        
        if actual_date <= end_date:
            # 20% to miss the habit entirely
            if random.random() > 0.2:
                data.append({
                    "Date": actual_date.strftime("%Y-%m-%d"),
                    "Amount": -round(random.uniform(4.50, 11.00), 2),
                    "Category": "Withdrawal",
                    "Service": "Food & Drink",
                    "Merchant Name": "STARBUCKS COFFEE" if random.random() < 0.8 else random.choice(["DUNKIN DONUTS", "PEET'S COFFEE", "HUNGRY GHOST"])
                })
            if random.random() > 0.1:
                data.append({
                    "Date": actual_date.strftime("%Y-%m-%d"),
                    "Amount": -round(random.uniform(80.00, 150.00), 2),
                    "Category": "Withdrawal",
                    "Service": "Groceries",
                    "Merchant Name": "TRADER JOE'S" if random.random() < 0.75 else random.choice(["WHOLEFOODS", "SAFEWAY", "COSTCO"])
                })

        
        curr = target_day + timedelta(days=7) # Ensure we jump to the next week

    # Bi-Weekly Habits (Gas)
    curr = start_date
    is_gas_week = True
    while curr <= end_date:
        days_to_sunday = (6 - curr.weekday() + 7) % 7
        target_day = curr + timedelta(days=days_to_sunday)
        
        # Gas usually varies by 2 day based on when the tank hits empty
        variance = random.choice([-1, 0, 1]) + random.choice([-1, 0, 1])
        actual_date = target_day + timedelta(days=variance)
        
        if actual_date <= end_date and is_gas_week:
            # 10% chance to skip (maybe they used the other car)
            if random.random() > 0.10:
                data.append({
                    "Date": actual_date.strftime("%Y-%m-%d"),
                    "Amount": -round(random.uniform(45.00, 75.00), 2),
                    "Category": "Withdrawal",
                    "Service": "Transport",
                    "Merchant Name": "SHELL OIL" if random.random() > 0.5 else random.choice(["EXXONMOBIL", "BP", "CHEVRON"])
                })
            
        is_gas_week = not is_gas_week
        curr = target_day + timedelta(days=7)
    
    # MTA Commuter (Daily with Weekly Variance)
    curr = start_date
    while curr <= end_date:
        # 1. Determine probability based on day of week
        # 90% chance to commute on Weekdays (0-4), 20% on Weekends (5-6)
        commute_chance = 0.90 if curr.weekday() < 5 else 0.20
        
        if random.random() < commute_chance:
            # 2. Most commuters tap twice (Round Trip), some once (One-way/Walked)
            num_trips = 2 if random.random() < 0.85 else 1
            
            for _ in range(num_trips):
                data.append({
                    "Date": curr.strftime("%Y-%m-%d"),
                    "Amount": -3, # Standard MTA Fare
                    "Category": "Withdrawal",
                    "Service": "Transport",
                    "Merchant Name": "MTA*NYCT PAYGO"
                })
        
        curr += timedelta(days=1)

    # Export to generates_account.csv
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by="Date")
    df.to_csv(file_path, index=False)
    return df, sub_names

if __name__ == "__main__":
    generate_clean_statement()