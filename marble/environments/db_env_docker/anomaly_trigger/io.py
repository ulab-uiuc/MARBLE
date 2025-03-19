import datetime
import os


#print the current time
def print_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)

if __name__ == "__main__":
    print_time()
    command = (
    "su - root -c 'cd /sysbench-tpcc-master; "
    "./tpcc.lua --db-driver=pgsql --tables=2 --scale=3 --threads=50 --events=0 "
    "--pgsql-host=localhost --pgsql-user=test --pgsql-password=Test123_456 "
    "--pgsql-port=5432 --pgsql-db=sysbench --time=90 --rand-type=uniform --report-interval=10 run'"
    )

    os.system(command)
    print_time()
