import os
import csv
import random
from datetime import datetime, timedelta

def main():
    # Set seed for reproducibility
    random.seed(42)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Standard lists
    regions = ['North', 'East', 'South', 'West']
    card_types = ['Visa', 'MasterCard', 'Amex', 'Discover']
    statuses = ['Completed', 'Failed', 'Pending', 'Reversed']
    devices = ['Mobile', 'Desktop', 'ATM', 'POS']
    
    # Generate customer and merchant pools
    customer_ids = [f"C{random.randint(10000, 99999)}" for _ in range(1500)]
    merchant_ids = [f"M{random.randint(1000, 9999)}" for _ in range(500)]
    
    start_date = datetime(2025, 1, 1)
    
    rows = []
    num_duplicates = 100
    num_unique = 15000 - num_duplicates
    
    for i in range(num_unique):
        tx_id = f"TX{100000 + i}"
        cust_id = random.choice(customer_ids)
        merch_id = random.choice(merchant_ids)
        
        # 1. Missing values (NaNs) in transaction_amount (approx. 5% chance)
        if random.random() < 0.05:
            amount = random.choice(["NaN", ""])
        else:
            amount = round(random.uniform(5.0, 2000.0), 2)
            
        card = random.choice(card_types)
        status = random.choice(statuses)
        device = random.choice(devices)
        age = random.randint(0, 120)
        
        # transaction_date: randomized dates
        days_offset = random.randint(0, 500)
        date_val = start_date + timedelta(days=days_offset)
        
        # Inconsistent date string formats
        fmt_choice = random.choice(['YYYY-MM-DD', 'DD/MM/YYYY', 'MM-DD-YYYY', 'DD-MMM-YYYY', 'ISO-TS'])
        if fmt_choice == 'YYYY-MM-DD':
            date_str = date_val.strftime('%Y-%m-%d')
        elif fmt_choice == 'DD/MM/YYYY':
            date_str = date_val.strftime('%d/%m/%Y')
        elif fmt_choice == 'MM-DD-YYYY':
            date_str = date_val.strftime('%m-%d-%Y')
        elif fmt_choice == 'DD-MMM-YYYY':
            date_str = date_val.strftime('%d-%b-%Y')
        else:
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            date_val_with_time = date_val.replace(hour=hour, minute=minute, second=second)
            date_str = date_val_with_time.strftime('%Y-%m-%d %H:%M:%S')
            
        region = random.choice(regions)
        
        # Add slight messiness to regions (casing/whitespace)
        if random.random() < 0.02:
            region = region.lower()
        elif random.random() < 0.02:
            region = f" {region} "
            
        # Fraud flag: 1 if high amount, failed status, or random noise
        is_fraud = 0
        if isinstance(amount, float):
            if amount > 1800.0 and random.random() < 0.8:
                is_fraud = 1
            elif status == 'Failed' and amount > 1500.0 and random.random() < 0.5:
                is_fraud = 1
        if random.random() < 0.01:
            is_fraud = 1
            
        rows.append([tx_id, cust_id, merch_id, amount, card, status, device, age, date_str, region, is_fraud])
        
    # Duplicate rows (exact duplicate transactions)
    duplicate_rows = random.choices(rows, k=num_duplicates)
    rows.extend(duplicate_rows)
    
    # Shuffle rows to distribute duplicates throughout the dataset
    random.shuffle(rows)
    
    # Write to CSV
    output_path = os.path.join('data', 'raw_transactions.csv')
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'transaction_id', 'customer_id', 'merchant_id', 'transaction_amount',
            'card_type', 'transaction_status', 'device_type', 'account_age_months',
            'transaction_date', 'region', 'is_fraud'
        ])
        writer.writerows(rows)
        
    print(f"Successfully generated messy dataset with {len(rows)} rows at {output_path}")

if __name__ == '__main__':
    main()
