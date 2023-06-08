# Case study
This case study is about building a streaming pipeline for transactions into a data warehouse and
make them available for analytics.

## Architecture
### [Warehouse](./clickhouse.md)
The warehouse is a [ClickHouse](./clickhouse.md) database.
It is a columnar database that is optimized for analytics.

It’s schema looks like this:
```
|- events       # Database for raw events. Here, we only have transactions.
|  |- transactions
|- rejected_events # We want to keep track of the events that were rejected by the ETL.
|  |- transactions
|- analytics    # Materialized views deriving `events.transactions`.
|  |- transactions_hourly  # These materialize views help to speed up queries by pre-aggregating.
|  |- transactions_daily
|- entities
   |- banks
   |- merchants
   |- consumers
```

Any new record in `events.transactions` will propagate to the materialized views.
Deletions (in case of a reprocessing) need to be propagated as well; deleting records from
`events.transactions` will not delete them from the materialized views.

### [Kafka](./kafka.md)
Here, we only have one kafka topic: `transactions`.
In a production environment, it should be replicated and partitioned.

### [ETL](./etl.md)
We have one ETL which is responsible for ingesting the transactions into the warehouse.
It is a streaming ETL, which means that it is triggered by new records in the kafka topic.

## Situations
### Nominal conditions
In this case, events flow through the pipeline as expected.
Transactions which are invalid land in the `rejected_events.transactions` table, and they can be
reprocessed by an independent process by putting them back in the queue.

### Reprocessing
It can happen that a use case was not clearly defined, a bug occured, on our side or on our
partners’, and we need to reprocess events.

For this, we need to update our ETL to account for the new behaviour and reprocess Kafka events.
