import mysql.connector

Database = mysql.connector.Connect(
    host = 'localhost',
    user = 'root',
    passwd = '2303',
    auth_plugin ='mysql_native_password',
)

cursorObject = Database.cursor()

cursorObject.execute("CREATE DATABASE eumel_db")

print('ALL DONE')
