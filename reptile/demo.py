import pymysql

def up():
    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "UPDATE team SET gymnasium=%s WHERE E_name=%s"
            cursor.execute(sql, ('asldkj', 'nuggets'))
            connection.commit()
            print('okey')
    finally:
        connection.close()
        
up()