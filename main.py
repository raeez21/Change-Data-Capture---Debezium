import faker
import psycopg2
import random
from datetime import datetime
fake = faker.Faker()

def generate_transaction():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "userId": user['username'],
        "timestamp": datetime.utcnow().timestamp(),
        "amount": round(random.uniform(10,1000),2),
        "currency": random.choice(['USD', 'GBP']),
        "city": fake.city(),
        "country": fake.country(),
        "merchantName": fake.company(),
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer']),
        "ipAddress": fake.ipv4(),
        "voucherCode": random.choice(['','DISCOUNT10','SPRING20']),
        "affiliateId": fake.uuid4()
        }

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            timestamp TIMESTAMP,
            amount DECIMAL,
            currency VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            merchant_name VARCHAR(255),
            payment_method VARCHAR(255),
            ip_address VARCHAR(255),
            voucher_code VARCHAR(255),
            affiliateId VARCHAR(255)
        )
        """)
    cursor.close()
    conn.commit()



if __name__ == "__main__":
    conn = psycopg2.connect(
        host = "localhost",
        database = "financial_db",
        user = "postgres",
        password = "postgres",
        port = 5433,
        connect_timeout=10
    )
    create_table(conn)
    txn = generate_transaction()
    cur = conn.cursor()
    print(txn)

    cur.execute(
        """
        INSERT INTO transactions(transaction_id, user_id, timestamp, amount, currency, city, country, merchant_name, payment_method, ip_address, voucher_code, affiliateId)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (txn["transactionId"], txn["userId"], datetime.fromtimestamp(txn["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'), txn["amount"], txn["currency"], \
              txn["city"], txn["country"], txn["merchantName"], txn["paymentMethod"], txn["ipAddress"], txn["voucherCode"], txn["affiliateId"])
    )

    cur.close()
    conn.commit()