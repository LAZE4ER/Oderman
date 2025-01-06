import sqlite3

try:
    sql_connection = sqlite3.connect('pizza.db')
    create_table_exequte = '''CREATE TABLE developers(
        id INTEGER PRIMARY KEY,
        name NOT NULL,
        description NOT NULL,
        price NOT NULL);
    '''
    cursor = sql_connection.cursor()
    cursor.execute(create_table_exequte)
    print('table created')
    sql_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print('Connection error')

finally:
    sql_connection.close()
    print('Connection closed')