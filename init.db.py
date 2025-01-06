import sqlite3



connection = sqlite3.connect('pizza_app.db')

with open('schema.sql') as f:
    connection.execute(f.read())

cur = connection.cursor()



cur.execute("INSERT INTO pizzas (name, description,price) VALUES(?, ?, ?)",
('Margherita', 'tomato sauce, mozzarella, basil','$3.15')
)

cur.execute("INSERT INTO pizzas (name, description,price) VALUES(?, ?, ?)",
('Pepperoni', 'tomato sauce, mozzarella, pepperoni','$3.95')
)
cur.execute("INSERT INTO pizzas (name, description,price) VALUES(?, ?, ?)",
('Hawaiian', 'tomato sauce, mozzarella, pineapple, chicken','$3.70')
)

connection.commit()
connection.close()