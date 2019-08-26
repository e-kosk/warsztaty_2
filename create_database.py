from psycopg2 import connect, extensions

cnx = connect(user='postgres', password='coderslab', host='localhost', database='warsztaty_2')
cnx.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = cnx.cursor()

sql_users = """CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username VARCHAR(255), email VARCHAR(255) UNIQUE, hashed_password VARCHAR(80))"""
sql_messages = """CREATE TABLE IF NOT EXISTS messages (id serial PRIMARY KEY, from_id INT, to_id INT, text VARCHAR(255), creation_date DATE)"""

cur.execute(sql_users)
cur.execute(sql_messages)

cur.close()
cnx.close()
