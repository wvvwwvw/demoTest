import mysql.connector

connect_db = mysql.connector.connect(
    host="MySQL-8.2",
    user="root",
    password="root",
    database="DemoTest"
)