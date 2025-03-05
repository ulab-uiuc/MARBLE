import datetime
import os
import random
import time
from multiprocessing.pool import Pool

import promethues
import psycopg2
from utils.database import DB_CONFIG, Database, DBArgs


def init():
    # add the config
    # config_path = "/root/DB-GPT/config/tool_config.yaml"
    # with open(config_path, 'r') as config_file:
    #     config = yaml.safe_load(config_file)
    db_args = DBArgs("postgresql", DB_CONFIG, application_name="anomaly")
    return db_args


def restart_init():
    # add the config
    db_args = DBArgs("postgresql", DB_CONFIG, application_name="restart")
    return db_args

def restart():
    db=Database(restart_init())
    sql="SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.application_name = 'anomaly';"
    db.execute_sqls(sql)

def restart_postgresql():
    # Directly execute the restart command locally
    # print("PostgreSQL Service Reboot Disabled")
    # return
    try:
        os.chdir("..")
        os.system("sudo docker compose restart postgres_db")
        print("PostgreSQL Service Rebooted")
    except Exception as e:
        print(f"Local command exec error: {e}")

# create a table
def create_table(table_name,colsize, ncolumns):
    db=Database(init())
    column_definitions = ', '.join(f'name{i} varchar({colsize})' for i in range(ncolumns))
    creat_sql = f'CREATE TABLE {table_name} (id int, {column_definitions}, time timestamp);'
    db.execute_sqls(creat_sql)

# delete the table
def delete_table(table_name):
    db=Database(init())
    delete_sql=f'DROP TABLE if exists {table_name}'
    db.execute_sqls(delete_sql)

# print the current time
def print_start_time(cmd):
    log_file = open("dataset.txt", "a")
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()
    inttimestamp=int(timestamp)
    log_file.write(f"{cmd} started at {inttimestamp}\n")
    log_file.flush()
    # print(inttimestamp)
    print(current_time.strftime("%H:%M:%S"))

def print_end_time(cmd):
    log_file = open("dataset.txt", "a")
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()
    inttimestamp=int(timestamp)
    log_file.write(f"{cmd} ended at {inttimestamp}\n")
    log_file.flush()
    # print(inttimestamp)
    print(current_time.strftime("%H:%M:%S"))

def write_anomaly_sql_to_file(text):
    try:
        with open('badsql.txt', 'a') as file:
            file.write(f"{text}\n")
        print("Text written to badsql.txt")
    except Exception as e:
        print(f"Error writting to file: {e}")

def write_anomaly_sql_to_file_a_line(text):
    try:
        with open('badsql.txt', 'a') as file:
            file.write(f"{text}\t\t")
        print("Text written to badsql.txt")
    except Exception as e:
        print(f"Error writting to file: {e}")

def write_space():
    try:
        with open('badsql.txt', 'a') as file:
            file.write("\n")
    except Exception as e:
        print(f"Error writting to file: {e}")

'''insert_large_data'''
def insert_large_data(threads,duration,ncolumns,nrows,colsize,table_name='table1'):
    cmd=f"python main.py --anomaly INSERT_LARGE_DATA --threads {threads} --ncolumn {ncolumns} --nrow {nrows} --colsize {colsize}"
    #Delete undeleted tables
    delete_table(table_name)
    #create a new table
    create_table(table_name,colsize, ncolumns)
    db=Database(init())
    #insert the data
    #insert_definitions = ', '.join(f'repeat(round(random()*999)::text,{(colsize//3)})' for i in range(ncolumns))
    insert_definitions = ', '.join(f'(SELECT substr(md5(random()::text), 1, {colsize}))' for i in range(ncolumns))
    insert_data=f'INSERT INTO {table_name} SELECT generate_series(1,{nrows}),{insert_definitions}, NOW();'

    write_anomaly_sql_to_file(insert_data)
    time.sleep(10)
    print_start_time(cmd)
    db.concurrent_execute_sql(threads,duration,insert_data,commit_interval=1)
    print_end_time(cmd)
    time.sleep(10)
    #restaet the pg database
    restart()
    time.sleep(10)
    cpu,mem=promethues.restart_decision()
    if((cpu>50)|(mem>50)):
        restart_postgresql()

    #delete the table
    delete_table(table_name)


'''missing_index'''
def missing_index(threads,duration,ncolumns,nrows,colsize,table_name='table1'):
    cmd=f"python main.py --anomaly MISSING_INDEXES --threads {threads} --ncolumn {ncolumns} --nrow {nrows} --colsize {colsize}"
    #create a new table

    db=Database(init())
    delete_table(table_name)
    create_table(table_name,colsize, ncolumns)

    # insert some data to be selected
    insert_definitions = ', '.join(f'(SELECT substr(md5(random()::text), 1, {colsize}))' for i in range(ncolumns))
    insert_data=f'insert into {table_name} select generate_series(1,{nrows}),{insert_definitions}, now();'
    db.execute_sqls(insert_data)

    #select without the index
    missing_index='select * from '+table_name+' where id='
    write_anomaly_sql_to_file(missing_index)
    time.sleep(10)
    print_start_time(cmd)
    db.concurrent_execute_sql(threads,duration,missing_index,nrows)
    print_end_time(cmd)
    time.sleep(10)
    restart()
    time.sleep(10)
    #restaet the pg database
    cpu,mem=promethues.restart_decision()
    if((cpu>50)|(mem>50)):
        restart_postgresql()

    #delete the table
    delete_table(table_name)
    #print the end time


'''lock_contention'''
def lock_contention(threads,duration,ncolumns,nrows,colsize,table_name='table1'):
    cmd=f"python main.py --anomaly LOCK_CONTENTION --threads {threads} --ncolumn {ncolumns} --nrow {nrows} --colsize {colsize}"
    #create a new table
    delete_table(table_name)
    create_table(table_name,colsize, ncolumns)
    db=Database(init())
    # insert some data to be updated
    insert_definitions = ', '.join(f'(SELECT substr(md5(random()::text), 1, {colsize}))' for i in range(ncolumns))
    insert_data=f'insert into {table_name} select generate_series(1,{nrows}),{insert_definitions}, now();'
    db.execute_sqls(insert_data)
    pool = Pool(threads)
    time.sleep(10)
    print_start_time(cmd)
    for _ in range(threads):
        pool.apply_async(
            lock, (table_name, ncolumns, colsize, duration, nrows))
    pool.close()
    pool.join()
    print_end_time(cmd)
    write_space()
    time.sleep(10)
    restart()
    time.sleep(10)
    #restaet the pg database
    cpu,mem=promethues.restart_decision()
    if((cpu>50)|(mem>50)):
        restart_postgresql()

    #delete the table
    delete_table(table_name)


'''vacuum'''
def vacuum(threads,duration,ncolumns,nrows,colsize,table_name='table1'):
    cmd = f"python main.py --anomaly IMPROPER_VACUUM --threads {threads} --ncolumn {ncolumns} --nrow {nrows} --colsize {colsize}"
    db = Database(init())
    conn = psycopg2.connect(
        dbname="sysbench",
        user="test",
        password="Test123_456",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    # Create a new table
    delete_table(table_name)
    create_table(table_name, colsize, ncolumns)
    # set autovacuum to off on the table
    db.execute_sqls(f'ALTER TABLE {table_name} SET (autovacuum_enabled = false);')
    print(table_name)

    # Insert a large volume of data
    insert_definitions = ', '.join(f'(SELECT substr(md5(random()::text), 1, {colsize}))' for i in range(ncolumns))
    insert_data = f'insert into {table_name} select generate_series(1,{nrows}),{insert_definitions}, now();'
    db.execute_sqls(insert_data)
    time.sleep(10)
    print_start_time(cmd)

    # Delete a large portion of the rows to create dead tuples
    delete_nrows = int(nrows * 0.9)
    vacuum = f'delete from {table_name} where id < {delete_nrows};'
    write_anomaly_sql_to_file(vacuum)
    db.execute_sqls(vacuum)
    print_end_time(cmd)
    time.sleep(10)

    # Perform an improper VACUUM operation

    vacuum_cmd = 'VACUUM FULL;'  # Intentionally not using VERBOSE or ANALYZE
    # # write_anomaly_sql_to_file(vacuum_cmd)
    # # perform concurrent vacuum
    # db.execute_sql(vacuum_cmd)

    isolation_level = conn.isolation_level
    for _ in range(threads):
        conn.set_isolation_level(0)
        cur.execute(vacuum_cmd)

    conn.set_isolation_level(isolation_level)

    conn.commit()
    conn.close()
    # db.concurrent_execute_sql(threads, duration, vacuum_cmd, commit_interval=1)
    # db.execute_sql(vacuum_cmd)
    time.sleep(10)

    # Restart the PostgreSQL service if needed
    restart()
    time.sleep(10)
    cpu, mem = promethues.restart_decision()
    if cpu > 50 or mem > 50:
        restart_postgresql()

    # Delete the table
    delete_table(table_name)

'''redundent_index'''
def redundent_index(threads,duration,ncolumns,nrows,colsize,nindex,table_name='table1'):
    cmd=f"python main.py --anomaly REDUNDANT_INDEX --threads {threads} --ncolumn {ncolumns} --nrow {nrows} --colsize {colsize}"
    #create a new table
    delete_table(table_name)
    create_table(table_name,colsize, ncolumns)
    db=Database(init())
    # insert some data to be updated
    insert_definitions = ', '.join(f'(SELECT substr(md5(random()::text), 1, {colsize}))' for i in range(ncolumns))
    insert_data=f'INSERT into {table_name} SELECT generate_series(1,{nrows}),{insert_definitions}, NOW();'
    db.execute_sqls(insert_data)

    #initialization of the indexes
    nindex=int((nindex*ncolumns)/10)
    db.build_index(table_name,nindex)
    id_index='CREATE INDEX index_'+table_name+'_id ON '+table_name+'(id);'
    db.execute_sqls(id_index)
    time.sleep(10)
    #lock_contention
    print_start_time(cmd)
    pool = Pool(threads)
    for _ in range(threads):
        pool.apply_async(
            lock, (table_name, ncolumns, colsize, duration, nrows))
    pool.close()
    pool.join()
    print_end_time(cmd)
    time.sleep(10)
    #drop the index
    db.drop_index(table_name)
    restart()
    time.sleep(10)
    #restaet the pg database
    cpu,mem=promethues.restart_decision()
    if((cpu>50)|(mem>50)):
        restart_postgresql()

    #delete the table
    delete_table(table_name)


'''io_contention'''
def io_contention():
    raise NotImplementedError("Lua is still developing")
    cmd="python main.py --anomaly INSERT_LARGE_DATA,IO_CONTENTION"
    print_start_time(cmd)
    command = (
    "sudo -u root bash -c 'cd /sysbench-tpcc; "
    "./tpcc.lua --db-driver=pgsql --tables=2 --scale=3 --threads=50 --events=0 "
    "--pgsql-host=localhost --pgsql-user=test --pgsql-password=Test123_456 "
    "--pgsql-port=5432 --pgsql-db=sysbench --time=90 --rand-type=uniform --report-interval=10 run'"
    )
    write_anomaly_sql_to_file("sysbench-tpcc to INSERT_LARGE_DATA, IO_CONTENTION")
    os.system(command)
    print_end_time(cmd)
    time.sleep(10)
    restart()
    time.sleep(10)
    #restaet the pg database
    cpu,mem=promethues.restart_decision()
    if((cpu>50)|(mem>50)):
        restart_postgresql()


'''fetch_large_data'''
def fetch_large_data():
    cmd = "python main.py --anomaly FETCH_LARGE_DATA"

    # Log start time of the operation
    print_start_time(cmd)

    # Initialize the database connection
    db = Database(init())

    # Create required tables with large-scale data simulation
    db.execute_sqls("CREATE TABLE IF NOT EXISTS orders (o_orderkey int, o_orderpriority varchar(15), o_orderdate date);")
    db.execute_sqls("CREATE TABLE IF NOT EXISTS lineitem (l_orderkey int, l_commitdate date, l_receiptdate date);")

    # Insert a large volume of data into the tables using concurrent execution
    print("Inserting large datasets with concurrency...")
    orders_insert_query = """
        INSERT INTO orders
        SELECT generate_series(1, 10000),
               CASE WHEN random() > 0.5 THEN '1-URGENT' ELSE '5-LOW' END::varchar,
               (date '1996-03-01' + (random() * (date '1998-09-01' - date '1996-03-01'))::int)
        ON CONFLICT DO NOTHING;
    """

    db.concurrent_execute_sql(1, 3, orders_insert_query, commit_interval=1)
    # db.concurrent_execute_sql(1, 3, lineitem_insert_query, commit_interval=1)

    # Write an intensive SQL query to a file for anomaly testing
    anomaly_query = 'SELECT * FROM orders LIMIT 100;'

    print("Executing intensive query with concurrency...")
    # Simultaneously querying the same thing using multiple threads
    db.concurrent_execute_sql(1000, 3, anomaly_query, commit_interval=1)

    # Introduce an artificial delay to simulate prolonged system load
    time.sleep(15)

    # Restart the system to simulate recovery
    print("Restarting system to simulate recovery...")
    restart()

    # Pause to observe monitoring metrics during the restart
    time.sleep(15)

    # Decision-making based on Prometheus-monitored metrics
    cpu, mem = promethues.restart_decision()
    print(f"System Metrics - CPU: {cpu}%, Memory: {mem}%")

    if cpu > 80 or mem > 80:
        print("High resource usage detected. Restarting PostgreSQL...")
        restart_postgresql()

    # Log end time of the operation
    print_end_time(cmd)

'''cpu_contention'''
def cpu_contention():
    raise NotImplementedError("Database not configured for this anomaly")
    cmd="python main.py --anomaly POOR_JOIN_PERFORMANCE,CPU_CONTENTION"
    try:
        print_start_time(cmd)
        os.system("python benchmark_job.py")
        print_end_time(cmd)
        write_anomaly_sql_to_file('''SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title,MIN(t.production_year) AS movie_year FROM company_type AS ct,info_type AS it,movie_companies AS mc,movie_info_idx AS mi_idx,title AS WHERE ct.kind = 'production companies'AND it.info = 'top 250 rank'AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%' AND (mc.note LIKE '%(co-production)%'OR mc.note LIKE '%(presents)%') AND ct.id = mc.company_type_idAND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;''')
        time.sleep(10)
        restart()
        time.sleep(10)
        #restaet the pg database
        cpu,mem=promethues.restart_decision()
        if((cpu>50)|(mem>50)):
            restart_postgresql()

    except Exception as e:
        print(f"exception: {e}")


def lock(table_name, ncolumns, colsize, duration, nrows):
    args=init()
    start = time.time()
    #lock_contention
    while time.time()-start < duration:
        conn = psycopg2.connect(database=args.dbname, user=args.user, password=args.password,
                                        host=args.host, port=args.port)
        cur = conn.cursor()
        #write_anomaly_sql_to_file(lock_contention)
        while time.time()-start < duration:
            col_name = random.randint(0, ncolumns-1)
            row_name = random.randint(1, nrows-1)
            lock_contention = f'update {table_name} set name{col_name}=(SELECT substr(md5(random()::text), 1, {colsize})) where id ={row_name}'
            cur.execute(lock_contention)
            conn.commit()
        conn.commit()
        conn.close()
    write_anomaly_sql_to_file_a_line(lock_contention)
