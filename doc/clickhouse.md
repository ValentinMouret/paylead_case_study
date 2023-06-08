# ClickHouse
ClickHouse is the data warehouse.
It’s a columnar database which has nice functionalities for analytics.

It natively supports TTLs, materialized views, and replication.

## Getting started
```sh
# if needed, install clickhouse
./bin/install.sh

# Run clickhouse
./bin/run_clickhouse.sh

# In another shell
# Initialize clickhouse
./bin/init_clickhouse.sh

# If needed, cleanup the database
./bin/cleanup_clickhouse.sh

# To connect to the database
(cd db && ./clickhouse client)
```

## Improvements
* Add monitoring
* Design a way to «reprocess» materialized views which are created after records were inserted.
* Connect it directly to PostgreSQL for entities.

[Index](./index.md)