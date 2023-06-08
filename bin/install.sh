#!/bin/bash

# Installs the dependencies of the project:
# - clickhouse
# - kafka
#
# Also installs the Python project.

set -euo pipefail

install::clickhouse() {
    [ -d db ] && rm -r db
    mkdir db
    curl https://clickhouse.com/ | sh
    mv clickhouse db/clickhouse
}

install::kafka() {
    readonly name=kafka_2.13-3.4.0.tgz

    curl -fsSLO https://dlcdn.apache.org/kafka/3.4.0/$name
    tar -xzf $name
    rm $name
    mv ${name%.tgz} kafka
}

install::app() {
    poetry install
}

install::clickhouse \
  && install::app \
  && install::kafka
