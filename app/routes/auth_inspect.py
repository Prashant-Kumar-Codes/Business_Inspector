from extensions import *

conn = dbConn()
print(conn)
cursor = conn.cursor(dict=True)
print(cursor)