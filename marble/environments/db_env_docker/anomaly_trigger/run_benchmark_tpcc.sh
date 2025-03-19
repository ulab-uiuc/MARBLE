#!/usr/bin/env sh

nohup su - root -c "cd /sysbench-tpcc-master; ./tpcc.lua --db-driver=pgsql --tables=2 --scale=3 --threads=50 --events=0 --pgsql-host=localhost --pgsql-user=test --pgsql-password=Test123_456 --pgsql-port=5432 --pgsql-db=sysbench --time=36000 --rand-type=uniform --report-interval=10 run" > tpcc.log 2>&1 &
