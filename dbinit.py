from datetime import timedelta

from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey, Numeric, select
from sqlalchemy.orm import sessionmaker

from db import Database
from faker import Faker


def init():
    # Define the metadata object
    db = Database()
    engine = db.engine
    metadata = MetaData()

    # Define the tables
    customer_table = Table(
        'Customer',
        metadata,
        Column('customer_id', Integer, primary_key=True),
        Column('customer_name', String(255), nullable=False),
        Column('country', String(255))
    )

    account_table = Table(
        'Account',
        metadata,
        Column('account_id', Integer, primary_key=True),
        Column('account_number', String(36), nullable=False),
        Column('account_type', String(50), nullable=False),
        Column('customer_id', Integer, ForeignKey('Customer.customer_id')),
        Column('account_open_date', Date, nullable=False)
    )

    transaction_table = Table(
        'Transactions',
        metadata,
        Column('transaction_id', Integer, primary_key=True),
        Column('action_date', Date, nullable=False),
        Column('value_date', Date, nullable=False),
        Column('account_id', Integer, ForeignKey('Account.account_id')),
        Column('amount', Numeric(16, 2), nullable=False),
        Column('transaction_type', String(50))
    )

    # Create the tables in the database
    metadata.create_all(bind=engine)

    print("Tables created successfully.")

    # Create a Faker instance
    fake = Faker()

    # Insert data into the tables
    conn = engine.connect()

    # Create SqlAlchemy session
    session_factory = sessionmaker(engine)

    # we can now construct a Session() without needing to pass the
    # engine each time
    with session_factory() as session:
        # Check if there are any existing records
        existing_records_count = session.query(customer_table).count()

        if existing_records_count > 0:
            print("There are already records in the customer_table.")
            conn.close()
            return

    customer_count = 1000
    account_count = 10000
    transaction_count = 100000

    # Generate and insert customers
    customers = []
    for _ in range(customer_count):
        customer_name = fake.company()
        country = fake.random_element(elements=('USA', 'Canada', 'UK', 'France', 'Italy', 'Netherlands', 'Spain',
                                                'Germany', 'Japan', 'China', 'India', 'Australia', 'Brazil', 'Mexico'))
        customers.append({
            'customer_name': customer_name,
            'country': country
        })

    conn.execute(customer_table.insert(), customers)

    conn.commit()

    print("Customer records inserted successfully.")

    ## Generate and insert Account table linking to Customer table
    accounts = []
    for _ in range(account_count):
        account_number = fake.iban()
        account_type = fake.random_element(elements=('Checking', 'Savings', 'Investment'))
        customer_id = fake.random_int(min=1, max=customer_count)
        account_open_date = fake.date_between(start_date='-5y', end_date='today')
        accounts.append({
            'account_number': account_number,
            'account_type': account_type,
            'customer_id': customer_id,
            'account_open_date': account_open_date
        })

    conn.execute(account_table.insert(), accounts)

    conn.commit()

    print("Account records inserted successfully.")

    ## Generate and insert Transaction table linking to Account table
    transactions = []
    for _ in range(transaction_count):
        account_id = fake.random_int(min=1, max=account_count)
        account = accounts[account_id - 1]
        action_date = fake.date_between(start_date=account['account_open_date'], end_date='today')
        value_date = fake.date_between(start_date=action_date - timedelta(days=1), end_date=action_date + timedelta(days=1))

        amount = fake.random_int(min=0, max=10000)
        transaction_type = fake.random_element(elements=('Deposit', 'Withdrawal'))
        transactions.append({
            'action_date': action_date,
            'value_date': value_date,
            'account_id': account_id,
            'amount': amount,
            'transaction_type': transaction_type
        })

    conn.execute(transaction_table.insert(), transactions)
    conn.commit()

    print("Transaction records inserted successfully.")

    conn.close()
