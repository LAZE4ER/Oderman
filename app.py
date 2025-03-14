from flask import Flask, render_template, redirect, flash, request, url_for
import sqlite3
import requests
from werkzeug.exceptions import abort

app = Flask(__name__)

filename = 'data.txt'

poll_data = {
    'question': 'Which pizza is the best?',
    'fields': ['Peperoni', 'Gawaian', 'Margherita'],
}


def get_db_connection():
    conn = sqlite3.connect('pizza_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_pizza(pizza_id):
    conn = get_db_connection()
    pizza = conn.execute('SELECT * FROM pizzas WHERE id = ?', (pizza_id,)).fetchone()
    conn.close()
    if pizza is None:
        abort(404)
    return pizza

@app.route('/')
def index():
    return render_template('base.html', title='Oderman Pizzeria!', a='Our Menu', head_title='Odrman Italiano')

@app.route('/menu')
def menu():
    conn = get_db_connection()
    pizzas = conn.execute('SELECT * FROM pizzas').fetchall()
    conn.close()
    return render_template('menu.html', pizzas=pizzas)

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

@app.route('/<int:pizza_id>/edit', methods=['GET', 'POST'])
def edit(pizza_id):
    pizza = get_pizza(pizza_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        if not name:
            flash('Pizza not found')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE pizzas SET name = ?, description = ?, price = ? WHERE id = ?',
                         (name, description, price, pizza_id))
            conn.commit()
            conn.close()
            return redirect(url_for('menu'))
    return render_template('edit.html', pizza=pizza)

@app.route('/<int:pizza_id>/delete', methods=['POST'])
def delete(pizza_id):
    pizza = get_pizza(pizza_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM pizzas WHERE id = ?', (pizza_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('menu'))

API_KEY = 'd154bb34f3ddc1f4fa6c4edec6a4a777'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                error = f"City '{city}' not found. Please try again."
    return render_template('weather.html', weather_data=weather_data, error=error)



@app.route('/poll')
def poll():
    vote = request.args.get("field")
    with open(filename, 'a') as f:
        f.write(str(vote) + '\n')
    return render_template('poll.html', data=poll_data)
@app.route('/result')
def result():
    with open(filename, 'r') as f:
        votes = f.read().strip().split('\n')
    last_vote = votes[-1].split(':')[-1].strip() if votes else None
    return render_template('result.html', data=poll_data, vote=last_vote)

    








if __name__ == '__main__':
    app.run(debug=True)

    





