from psycopg2 import connect, extensions


class PostgresDB:
    def __init__(self, user, password, database):
        self.cnx = connect(user=user, password=password, host='localhost', database=database)
        self.cnx.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.cnx.cursor()

    def close(self):
        self.cur.close()
        self.cnx.close()

    def execute(self, s):
        return self.cur.execute(s)
