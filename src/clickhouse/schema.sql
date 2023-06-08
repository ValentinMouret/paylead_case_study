-- Contains the schema of the ClickHouse Data Warehouse.
-- Columns with a default value are considered optional.
-- Regarding ClickHouse’s performance, it is better to avoid nullable columns and provide a default.

-- ========================================
-- Database: entities
-- ------------------
-- Keeps track of the business entities like merchants, consumers, and banks.
-- They would come from a Postgres database, possibly with a materialized view.
--
-- They are useful for analytics to enrich results.
-- ========================================
create database entities;


create table entities.merchants (
    id       UInt32,
    name     String,
    primary key (id)
)
engine = MergeTree();


create table entities.consumers (
    id                  UInt32,
    name                String,
    preferred_merchants Array(UInt32), -- references a merchant’s ID.
    primary key (id)
)
engine = MergeTree();


-- This table will probably be quite small.
-- Therefore, we can keep a simple primary key and do full table scans on zip_code.
create table entities.banks (
    id       UInt32,
    name     String,
    zip_code String,

    primary key (id)
)
engine = MergeTree();


-- ========================================
-- Database: events
-- ----------------
-- Keeps track of the valid events, like transactions.
-- An analyst can safely query this database.
-- 
-- The only think which can happen is partial results in case of a bug as
-- invalid events are recorded in the `rejected_events` database.
-- ========================================
create database events;


create table events.transactions (
    creation_date  DateTime('UTC'),
    execution_date DateTime('UTC'),

    id             String, -- UUID
    consumer_id    UInt32,
    bank_id        UInt32,
    merchant_id    UInt32 default 0,

    amount         UInt64,
    label          String default '',
    country_code   String default '',

    primary key (creation_date, consumer_id)
)
engine = MergeTree()
-- To comply with RGPD, we delete records after 2 years.
ttl creation_date + interval 2 year delete;


-- ========================================
-- Database: rejected_events
-- --------------------------
-- Keeps track of the invalid events, like transactions.
-- We keep the raw events to debug issues and easily reprocess them by piping them
-- back into Kafka once they are fixed.
-- ========================================

create database rejected_events;


create table rejected_events.transactions (
    creation_date DateTime('UTC') materialized now(),
    -- Since the payload can be corrupted, we record the full string for debugging.
    message String,
    reason String default '',

    primary key (creation_date, reason)
)
engine = ReplacingMergeTree()
ttl creation_date + interval 2 month delete;


-- ========================================
-- Database: analytics
-- -------------------
-- Materialized views to compute analytics.
-- They speed up query times by pre-aggregating the results.
-- ========================================
create database analytics;


create table analytics.hourly_transactions (
    date        DateTime('UTC'), -- Hour granularity.

    consumer_id String,
    bank_id     String,
    merchant_id String,

    amount       AggregateFunction(sum, UInt64),
    transactions AggregateFunction(count, UInt64)
)
engine = AggregatingMergeTree()
order by (date, consumer_id, bank_id, merchant_id);


create materialized view analytics.hourly_transactions_mv
    to analytics.hourly_transactions
    as
select toStartOfHour(creation_date) as date,
       consumer_id,
       bank_id,
       merchant_id,
       sumState(amount) as amount,
       countState(*) as transactions
  from events.transactions
group by date,
         consumer_id,
         bank_id,
         merchant_id;


create table analytics.daily_transactions (
    date        DateTime('UTC'), -- Day granularity.

    consumer_id String,
    bank_id     String,
    merchant_id String,

    amount       AggregateFunction(sum, UInt64),
    transactions AggregateFunction(count, UInt64)
)
engine = AggregatingMergeTree()
order by (date, consumer_id, bank_id, merchant_id);


create materialized view analytics.daily_transactions_mv
    to analytics.daily_transactions
    as
select toStartOfDay(creation_date) as date,
       consumer_id,
       bank_id,
       merchant_id,
       sumState(amount) as amount,
       countState(*) as transactions
  from events.transactions
group by date,
         consumer_id,
         bank_id,
         merchant_id;
