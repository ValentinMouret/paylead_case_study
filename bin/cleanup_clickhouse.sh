#!/bin/bash

# Drops the ClickHouse databases.
# Useful in development, a bit less on production. :)

set -euo pipefail

(cd db \
  && ./clickhouse client -q 'drop database entities;' \
  && ./clickhouse client -q 'drop database events;' \
  && ./clickhouse client -q 'drop database rejected_events;' \
  && ./clickhouse client -q 'drop database analytics;')
