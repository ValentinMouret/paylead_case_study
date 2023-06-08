#!/bin/bash

# Runs the ClickHouse server.

set -euo pipefail

(cd db && ./clickhouse server)
