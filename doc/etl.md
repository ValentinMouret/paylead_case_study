# ETL
## Architecture
Our application is layed out the following way:
```
|- src
|  |- clickhouse # schema and utils for dealing with ClickHouse
|  |- etls       # module for our ETL(s)
|  |- model      # domain model, should be readable for most people in the company
|  |- tasks      # runnables which are not directly ETLs (e.g. to simulate the data)
|  |- fuzzer.py  # introduces random errors in the data
|  |- transaction_generator.py # generates random transactions
|  |- utils.py   # general utils for the project
|- tests         # Tests
```

The ETL will check a series of conditions before inserting the data in ClickHouse.
If one is unmet, the record will be written in the `rejected_events` table.

## Getting started
To test the project:
```sh
poetry run pytest tests
```

To run the project:
```sh
# Run the stream ETL
poetry run python -m src.etls.stream_transactions

# In another shell
# Run the simulator
poetry run python -m src.tasks.simulate

# After that, open a ClickHouse client and check the data
```

## Improvements
* Add monitoring
* Regroup infrastructure code to avoid some light duplication
* Add more business logic

[Index](./index.md)