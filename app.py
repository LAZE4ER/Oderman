from flask import Flask, render_template, redirect, flash, request, url_for
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pizza_app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html', title = ' Oderman Pizzeria!', a = 'Our Menu', head_title = 'Odrman Italiano')



@app.route('/menu')
def menu():
   
    conn = get_db_connection()
    pizzas = conn.execute('SELECT * FROM pizzas').fetchall()
    conn.close()
    return render_template('menu.html.',pizzas=pizzas)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        if not name:
            flash('Name not found')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO pizzas (name, description, price) VALUES (?, ?, ?)', 
             (name, description, price))
            conn.commit()
            conn.close()
            return redirect(url_for('menu'))
    return render_template('add.html')  





if __name__ == '__main__':
    app.run(debug=True)
    



    





