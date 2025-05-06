# This file was written by Lucas Black
import psycopg

# Class for handling DB connections and operations with psycopg
class db_utils:
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def read_data(self, query="", query_params=()):
        if not isinstance(query_params, tuple):
            query_params = (query_params,)

        if self.password is not None:
            conn = psycopg.Connection.connect(dbname=self.dbname,
                                              user=self.user,
                                              password=self.password,
                                              host=self.host,
                                              port=self.port,
                                              row_factory=psycopg.rows.dict_row)
        else:
            conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user),
                row_factory=psycopg.rows.dict_row)

        results = []
        with conn.cursor() as cur:
            # could add a database logger here
            cur.execute(query, query_params)
            results = cur.fetchall()

        conn.close()

        return results

    def mutate_data(self, query="", query_params=()):
        if not isinstance(query_params, tuple):
            query_params = (query_params,)

        if self.password is not None:
            conn = psycopg.Connection.connect(dbname=self.dbname,
                                              user=self.user,
                                              password=self.password,
                                              host=self.host,
                                              port=self.port)
        else:
            conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user))

        try:
            with conn.cursor() as cur:
                cur.execute(query, query_params)
                if cur.description:  # Check if the query returns data
                    result = cur.fetchall()  # Get any returned data
                else:
                    result = None
            conn.commit()  # Commit the transaction
            return result
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()  # Rollback on error
            raise e
        finally:
            conn.close()