import os
import csv
import random
import shutil
from datetime import datetime, timedelta

def generate_fintech_datasets():
    random.seed(42)
    
    # Target directories
    data_dirs = ['data', os.path.join('investigate_pandas', 'data')]
    for d in data_dirs:
        os.makedirs(d, exist_ok=True)
        
    print("Generating comprehensive Fintech datasets...")

    # -------------------------------------------------------------
    # 1. Base Setup & Pools
    # -------------------------------------------------------------
    regions = ['North', 'East', 'South', 'West']
    card_types = ['Visa', 'MasterCard', 'Amex', 'Discover']
    statuses = ['Completed', 'Failed', 'Pending', 'Reversed']
    devices = ['Mobile', 'Desktop', 'ATM', 'POS']
    
    # 1500 core customers, 500 core merchants
    customer_ids = [f"C{random.randint(10000, 99999)}" for _ in range(1500)]
    merchant_ids = [f"M{random.randint(1000, 9999)}" for _ in range(500)]
    
    # Dedup while preserving order
    unique_cust_pool = list(dict.fromkeys(customer_ids))
    unique_merch_pool = list(dict.fromkeys(merchant_ids))
    
    # -------------------------------------------------------------
    # 2. Generate raw_transactions.csv (15,000 rows)
    # -------------------------------------------------------------
    start_date = datetime(2025, 1, 1)
    tx_rows = []
    num_duplicates = 100
    num_unique_tx = 15000 - num_duplicates
    
    tx_dict = {} # tx_id -> {cust_id, merch_id, amount, date, status}
    
    for i in range(num_unique_tx):
        tx_id = f"TX{100000 + i}"
        cust_id = random.choice(unique_cust_pool)
        merch_id = random.choice(unique_merch_pool)
        
        # Missing values (approx 5% chance)
        if random.random() < 0.05:
            amount_val = "NaN"
            numeric_amount = None
        else:
            numeric_amount = round(random.uniform(5.0, 2000.0), 2)
            amount_val = numeric_amount
            
        card = random.choice(card_types)
        status = random.choice(statuses)
        device = random.choice(devices)
        age = random.randint(0, 120)
        
        days_offset = random.randint(0, 500)
        date_val = start_date + timedelta(days=days_offset)
        
        # Realistic date string format variations
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
        if random.random() < 0.02:
            region = region.lower()
        elif random.random() < 0.02:
            region = f" {region} "
            
        is_fraud = 0
        if isinstance(numeric_amount, float):
            if numeric_amount > 1800.0 and random.random() < 0.8:
                is_fraud = 1
            elif status == 'Failed' and numeric_amount > 1500.0 and random.random() < 0.5:
                is_fraud = 1
        if random.random() < 0.01:
            is_fraud = 1
            
        tx_row = [tx_id, cust_id, merch_id, amount_val, card, status, device, age, date_str, region, is_fraud]
        tx_rows.append(tx_row)
        
        tx_dict[tx_id] = {
            'customer_id': cust_id,
            'merchant_id': merch_id,
            'amount': numeric_amount if numeric_amount is not None else 100.0,
            'date_val': date_val,
            'status': status,
            'card_type': card,
            'is_fraud': is_fraud
        }
        
    duplicate_rows = random.choices(tx_rows, k=num_duplicates)
    tx_rows.extend(duplicate_rows)
    random.shuffle(tx_rows)
    
    # -------------------------------------------------------------
    # 3. Generate customers.csv (5,000 rows)
    # -------------------------------------------------------------
    # Pool includes all active customers + additional registered users
    extra_customers = [f"C{random.randint(10000, 99999)}" for _ in range(3550)]
    all_customer_pool = list(dict.fromkeys(unique_cust_pool + extra_customers))[:5000]
    
    first_names = [
        'James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
        'David', 'Elizabeth', 'William', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
        'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
        'Aarav', 'Priya', 'Liam', 'Emma', 'Mateo', 'Sofia', 'Wei', 'Yuki', 'Amara', 'Carlos'
    ]
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
        'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Patel', 'Sharma', 'Tanaka', 'Muller', 'Dubois', 'Silva', 'Rossi', 'Kim', 'Chen'
    ]
    email_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'proton.me', 'fintechmail.io']
    countries = ['US', 'US', 'US', 'CA', 'GB', 'DE', 'FR', 'AU', 'SG', 'IN']
    us_states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI', 'NJ', 'VA', 'WA', 'AZ', 'MA']
    kyc_statuses = ['Verified', 'Verified', 'Verified', 'Pending', 'Under Review', 'Rejected']
    risk_tiers = ['Low', 'Low', 'Medium', 'Medium', 'High', 'Critical']
    tiers = ['Standard', 'Silver', 'Gold', 'Platinum', 'VIP']
    
    customer_rows = []
    for c_id in all_customer_pool:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        domain = random.choice(email_domains)
        email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 999)}@{domain}"
        country = random.choice(countries)
        state = random.choice(us_states) if country == 'US' else 'N/A'
        kyc = random.choice(kyc_statuses)
        risk = random.choice(risk_tiers)
        
        # Credit score: 300 to 850, ~3% missing (unbanked)
        if random.random() < 0.03:
            credit_score = ""
        else:
            credit_score = random.randint(350, 850)
            
        income = random.randint(22000, 320000)
        account_balance = round(random.uniform(50.0, 75000.0), 2)
        
        created_days_ago = random.randint(30, 2000)
        created_date = (datetime(2025, 1, 1) - timedelta(days=created_days_ago)).strftime('%Y-%m-%d')
        tier = random.choice(tiers)
        has_crypto = 1 if random.random() < 0.28 else 0
        is_pep = 1 if random.random() < 0.015 else 0
        
        customer_rows.append([
            c_id, fn, ln, email, country, state, kyc, risk,
            credit_score, income, account_balance, created_date, tier, has_crypto, is_pep
        ])

    # -------------------------------------------------------------
    # 4. Generate merchants.csv (2,000 rows)
    # -------------------------------------------------------------
    extra_merchants = [f"M{random.randint(1000, 9999)}" for _ in range(1600)]
    all_merchant_pool = list(dict.fromkeys(unique_merch_pool + extra_merchants))[:2000]
    
    categories = [
        ('E-Commerce & Marketplaces', 5311, 0.024, 'Moderate'),
        ('Food & Dining', 5812, 0.019, 'Low'),
        ('Travel & Airlines', 4511, 0.028, 'High'),
        ('Grocery & Supermarket', 5411, 0.015, 'Low'),
        ('Crypto & Digital Assets', 6051, 0.038, 'Extreme'),
        ('Gaming & Virtual Goods', 7995, 0.032, 'High'),
        ('Electronics & Computers', 5732, 0.022, 'Moderate'),
        ('Healthcare & Wellness', 8099, 0.018, 'Low'),
        ('Financial Services & SaaS', 5999, 0.025, 'Moderate')
    ]
    
    merchant_prefixes = [
        'Apex', 'Quantum', 'Nova', 'Cyber', 'Starlight', 'Hyper', 'Swift', 'Prime',
        'Vanguard', 'Alpha', 'Nexus', 'Vertex', 'Zenith', 'Summit', 'Global', 'Beacon',
        'Titan', 'Pulse', 'Aero', 'Horizon', 'BlueSky', 'SilverLine', 'Velocity', 'Pioneer'
    ]
    merchant_suffixes = [
        'Pay', 'Mart', 'Direct', 'Hub', 'Express', 'Holdings', 'Store', 'Ventures',
        'Cloud', 'Retail', 'Logistics', 'Tech', 'Solutions', 'Air', 'Foods', 'Cafe'
    ]
    
    merchant_rows = []
    for m_id in all_merchant_pool:
        cat_info = random.choice(categories)
        cat_name, mcc, base_fee, default_risk = cat_info
        
        name = f"{random.choice(merchant_prefixes)} {random.choice(merchant_suffixes)}"
        fee_pct = round(base_fee + random.uniform(-0.003, 0.005), 4)
        m_country = random.choice(countries)
        risk = default_risk if random.random() < 0.85 else random.choice(['Low', 'Moderate', 'High', 'Extreme'])
        
        onboard_days = random.randint(100, 1800)
        onboard_date = (datetime(2025, 1, 1) - timedelta(days=onboard_days)).strftime('%Y-%m-%d')
        settlement_days = random.choice([1, 1, 2, 2, 3, 7])
        chargeback_monitored = 1 if risk in ['High', 'Extreme'] and random.random() < 0.35 else 0
        monthly_volume_est = round(random.uniform(10000.0, 2500000.0), 2)
        
        merchant_rows.append([
            m_id, name, cat_name, mcc, m_country, fee_pct,
            risk, onboard_date, settlement_days, chargeback_monitored, monthly_volume_est
        ])

    # -------------------------------------------------------------
    # 5. Generate disputes.csv (10,000 rows)
    # -------------------------------------------------------------
    # Disputes linked to raw_transactions + some external dispute records
    dispute_reasons = [
        'Fraudulent Transaction',
        'Item Not Received',
        'Product Defective / Unacceptable',
        'Duplicate Processing',
        'Subscription Cancelled',
        'Credit Not Processed',
        'Friendly Fraud / Unrecognized'
    ]
    dispute_statuses = [
        'Won - Merchant',
        'Won - Customer',
        'Under Review',
        'Arbitration',
        'Chargeback Reversed',
        'Pending Evidence'
    ]
    liabilities = ['Merchant', 'Cardholder', 'Issuing Bank', 'Payment Processor']
    chargeback_fees = [15.00, 20.00, 25.00, 35.00, 50.00]
    
    dispute_rows = []
    tx_ids_list = list(tx_dict.keys())
    
    # 10,000 dispute records
    for d_idx in range(10000):
        dsp_id = f"DSP{200000 + d_idx}"
        
        # 70% of disputes link directly to existing raw_transactions, 30% are external historical
        if d_idx < 7000 and random.random() < 0.9:
            sampled_tx_id = random.choice(tx_ids_list)
            meta = tx_dict[sampled_tx_id]
            linked_tx_id = sampled_tx_id
            c_id = meta['customer_id']
            m_id = meta['merchant_id']
            tx_amt = meta['amount']
            tx_dt = meta['date_val']
            # If transaction had is_fraud=1, higher chance of Fraudulent Transaction reason
            if meta['is_fraud'] == 1 and random.random() < 0.75:
                reason = 'Fraudulent Transaction'
            else:
                reason = random.choice(dispute_reasons)
        else:
            linked_tx_id = f"TX{random.randint(200000, 299999)}"
            c_id = random.choice(all_customer_pool)
            m_id = random.choice(all_merchant_pool)
            tx_amt = round(random.uniform(20.0, 1500.0), 2)
            tx_dt = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 450))
            reason = random.choice(dispute_reasons)
            
        # Dispute filed between 2 to 45 days after transaction
        dispute_date_val = tx_dt + timedelta(days=random.randint(2, 45))
        dispute_date_str = dispute_date_val.strftime('%Y-%m-%d')
        
        # Disputed amount: partial (e.g. 50%) or full amount
        if random.random() < 0.15:
            disputed_amt = round(tx_amt * random.uniform(0.3, 0.9), 2)
        else:
            disputed_amt = round(tx_amt, 2)
            
        status = random.choice(dispute_statuses)
        evidence = 1 if status in ['Won - Merchant', 'Won - Customer', 'Arbitration'] or random.random() < 0.6 else 0
        cb_fee = random.choice(chargeback_fees)
        
        if status in ['Won - Merchant', 'Won - Customer', 'Arbitration', 'Chargeback Reversed']:
            res_days = random.randint(7, 60)
            res_date_str = (dispute_date_val + timedelta(days=res_days)).strftime('%Y-%m-%d')
            if status == 'Won - Merchant':
                liability = 'Cardholder' if random.random() < 0.8 else 'Issuing Bank'
            elif status == 'Won - Customer':
                liability = 'Merchant' if random.random() < 0.85 else 'Payment Processor'
            else:
                liability = random.choice(liabilities)
        else:
            res_date_str = "" # Still pending / open
            liability = "Pending"
            
        dispute_rows.append([
            dsp_id, linked_tx_id, c_id, m_id, dispute_date_str, reason,
            disputed_amt, status, evidence, cb_fee, res_date_str, liability
        ])

    # -------------------------------------------------------------
    # 6. Write all CSVs to both target folders
    # -------------------------------------------------------------
    for target_dir in data_dirs:
        # 1. raw_transactions.csv
        raw_tx_path = os.path.join(target_dir, 'raw_transactions.csv')
        with open(raw_tx_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'transaction_id', 'customer_id', 'merchant_id', 'transaction_amount',
                'card_type', 'transaction_status', 'device_type', 'account_age_months',
                'transaction_date', 'region', 'is_fraud'
            ])
            writer.writerows(tx_rows)
            
        # 2. customers.csv
        cust_path = os.path.join(target_dir, 'customers.csv')
        with open(cust_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'customer_id', 'first_name', 'last_name', 'email', 'country_code',
                'state_province', 'kyc_status', 'risk_tier', 'credit_score',
                'annual_income', 'account_balance', 'account_created_at',
                'account_tier', 'has_crypto_wallet', 'is_pep'
            ])
            writer.writerows(customer_rows)
            
        # 3. merchants.csv
        merch_path = os.path.join(target_dir, 'merchants.csv')
        with open(merch_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'merchant_id', 'merchant_name', 'category', 'mcc_code', 'country_code',
                'interchange_fee_pct', 'risk_rating', 'onboarding_date',
                'payout_settlement_days', 'is_chargeback_monitored', 'monthly_volume_est'
            ])
            writer.writerows(merchant_rows)
            
        # 4. disputes.csv
        disp_path = os.path.join(target_dir, 'disputes.csv')
        with open(disp_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'dispute_id', 'transaction_id', 'customer_id', 'merchant_id',
                'dispute_date', 'dispute_reason', 'disputed_amount', 'dispute_status',
                'evidence_submitted', 'chargeback_fee_usd', 'resolution_date', 'liability_assigned'
            ])
            writer.writerows(dispute_rows)
            
        print(f"-> Successfully generated in '{target_dir}':")
        print(f"   - raw_transactions.csv : {len(tx_rows)} rows")
        print(f"   - customers.csv        : {len(customer_rows)} rows")
        print(f"   - merchants.csv        : {len(merchant_rows)} rows")
        print(f"   - disputes.csv         : {len(dispute_rows)} rows")

if __name__ == '__main__':
    generate_fintech_datasets()
