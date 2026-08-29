import os
import csv
import random
from datetime import datetime, timedelta

def main():
    # Set seed for reproducibility
    random.seed(42)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Standard regions list
    regions = ['North', 'East', 'South', 'West']
    
    # Generate customer pool (e.g., 1000 unique customer IDs)
    customer_ids = [f"C{random.randint(10000, 99999)}" for _ in range(1000)]
    
    start_date = datetime(2025, 1, 1)
    
    rows = []
    num_duplicates = 50
    num_unique = 10000 - num_duplicates
    
    for i in range(num_unique):
        tx_id = f"TX{100000 + i}"
        cust_id = random.choice(customer_ids)
        
        # 1. Missing values (NaNs) in transaction_amount (approx. 5% chance)
        if random.random() < 0.05:
            # We will use "NaN" to represent NaNs explicitly, as well as some empty fields
            amount = random.choice(["NaN", ""])
        else:
            amount = round(random.uniform(5.0, 1500.0), 2)
            
        # account_age_months: random integer
        age = random.randint(0, 120)
        
        # transaction_date: randomized dates
        days_offset = random.randint(0, 500)
        date_val = start_date + timedelta(days=days_offset)
        
        # 2. Inconsistent date string formats
        fmt_choice = random.choice(['YYYY-MM-DD', 'DD/MM/YYYY', 'MM-DD-YYYY', 'DD-MMM-YYYY', 'ISO-TS'])
        if fmt_choice == 'YYYY-MM-DD':
            date_str = date_val.strftime('%Y-%m-%d')
        elif fmt_choice == 'DD/MM/YYYY':
            date_str = date_val.strftime('%d/%m/%Y')
        elif fmt_choice == 'MM-DD-YYYY':
            date_str = date_val.strftime('%m-%d-%Y')
        elif fmt_choice == 'DD-MMM-YYYY':
            date_str = date_val.strftime('%d-%b-%Y')
        else: # ISO-TS format with random time component
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            date_val_with_time = date_val.replace(hour=hour, minute=minute, second=second)
            date_str = date_val_with_time.strftime('%Y-%m-%d %H:%M:%S')
            
        region = random.choice(regions)
        
        # Add slight messiness to regions as well (casing/whitespace)
        if random.random() < 0.02:
            region = region.lower()
        elif random.random() < 0.02:
            region = f" {region} "
            
        rows.append([tx_id, cust_id, amount, age, date_str, region])
        
    # 3. Duplicate rows (exact duplicate transactions)
    duplicate_rows = random.choices(rows, k=num_duplicates)
    rows.extend(duplicate_rows)
    
    # Shuffle rows to distribute duplicates throughout the dataset
    random.shuffle(rows)
    
    # Write to CSV
    output_path = os.path.join('data', 'raw_transactions.csv')
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Columns: transaction_id, customer_id, transaction_amount, account_age_months, transaction_date, region
        writer.writerow(['transaction_id', 'customer_id', 'transaction_amount', 'account_age_months', 'transaction_date', 'region'])
        writer.writerows(rows)
        
    print(f"Successfully generated messy dataset with {len(rows)} rows at {output_path}")

if __name__ == '__main__':
    main()
