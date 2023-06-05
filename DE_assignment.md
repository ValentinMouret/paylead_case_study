# PayLead Data Engineering assignment

## Goal

This project aims to demonstrate your Python and data engineering skills.
It will involve the understanding of an ETL process or your ability to work with a distributed streaming platform like Kafka.
You will build a system that simulates PayLead's business model, analyzing transactional data to provide personalized offers.

This code will be used as a basis for your upcoming technical interview: you will be asked to explain its design,
what your coding process was, etc.
Your interviewers will need the code at least one working day in advance, with whichever setup instructions you feel relevant.

## Expectations

The code must be compatible with a UNIX shell, running under `Python 3.10` or above; if external libraries are used, the list should be provided in the setup instructions — assume the user is running a ubuntu-like operating system.
It's best to have a solution as a git repository with a README.md for setup instruction and though process.

## Instructions

Data Generation:

Construct a Python based TransactionGenerator class to generate synthetic transaction data involving a specified group of customers, merchants, and banks.
This transaction data should incorporate fields such as `consumer_id`, `bank_id`, `amount`, `country_code`, `execution_date` and optionally a `merchant_id`.

ETL Process:

You have the flexibility to choose from one of the following scenarios.

Utilizing Kafka for Real-Time Data Streaming:
In your Python application, initiate a Kafka producer to transmit the synthesized transaction data to Kafka topics.
Then, construct an ETL pipeline using a Kafka consumer to load the data in DataWarehouse/DataLake.

Extracting Data from the Product Database:
Use the simulated transaction data stored in a PostgreSQL or MySQL Database. The extraction phase includes retrieving data from this operational database and transferring it in batches to the DataWarehouse/DataLake.

In both scenarios, the transformation phase should do some cleaning, filtering, and restructuring the data into a format that can be used effectively.

The loading phase should be loading this restructured data into a DataWarehouse/DataLake of your preference.

Data Retention:

Within the DataWarehouse/DataLake it should be possible to find all consumers transaction history and facilitate the construction of business KPIs or ML models by other team members.
To adhere to RGPD, transactional data older than two years should be systematically purged after two years in the Data Warehouse/DataLake

Bonus:

Banking errors: The system should accommodate and react where banking errors may update specific transactions records

## Hints & advice

The following third party libraries may prove interesting:

- [`kafka-python`](https://pypi.org/project/kafka-python/) or [`confluent-kafka`](https://pypi.org/project/confluent-kafka/) to work with kafka in python
- [`pytest`](https://pypi.org/project/pytest/) as an alternative to `unittest` for automated testing
- [`faker`](https://pypi.org/project/Faker/) to generate some fake python data
- [`psycopg2`](https://pypi.org/project/psycopg2/) if you need for a PostgreSQL or MySQL database

If using the existing database approach the schema could be the following:

```sql
CREATE TABLE consumers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    prefered_merchants INTEGER[]
);

CREATE TABLE merchants (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE banks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    zipcode TEXT UNIQUE NOT NULL
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    amount NUMERIC(10, 5),
    creation_date TIMESTAMP WITH TIME ZONE,
    execution_date TIMESTAMP WITH TIME ZONE,
    label TEXT,
    country_code TEXT,
    consumer_id INTEGER NOT NULL REFERENCES consumers (id),
    bank_id INTEGER NOT NULL REFERENCES banks (id),
    merchant_id INTEGER REFERENCES merchants (id)
);
```
