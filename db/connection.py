import pymysql

connection = pymysql.connect(
    host='localhost',
    password='',
    user='root',
    port=3307,
    database='dbpendaftaransiswa'
)

cursor = connection.cursor()