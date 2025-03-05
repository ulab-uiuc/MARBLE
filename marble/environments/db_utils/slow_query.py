import psycopg2
from psycopg2.extras import RealDictCursor


def obtain_slow_queries(server_address="localhost",
                        username="test",
                        password="Test123_456",
                        database="sysbench",
                        port="5432",
                        top_k=10):
    try:
        connection = psycopg2.connect(
            user=username,
            password=password,
            database=database,
            host=server_address,
            port=port
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        slow_queries_query = f"""
            CREATE EXTENSION pg_stat_statements;
            SELECT
                query,
                total_exec_time
            FROM pg_stat_statements
            ORDER BY total_exec_time DESC
            LIMIT {top_k};
        """

        cursor.execute(slow_queries_query)
        slow_queries = cursor.fetchall()
        slow_queries_str = ""

        for idx, record in enumerate(slow_queries, start=1):
            slow_queries_str += f"{idx}. Query: {record['query']}\n"
            slow_queries_str += f"   Total Execution Time: {record['total_exec_time']}\n"
            slow_queries_str += "-" * 10
            slow_queries_str += "\n"

        cursor.close()
        connection.close()

        return slow_queries_str

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    obtain_slow_queries()
