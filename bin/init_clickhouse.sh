#!/bin/bash

# Initialize ClickHouse with its schema.

set -euo pipefail

(cd db && ./clickhouse client --queries-file ../src/clickhouse/schema.sql)
