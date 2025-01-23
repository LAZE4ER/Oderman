from flask import Flask, render_template, redirect, flash, request, url_for
import sqlite3
import requests


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



if __name__ == '__main__':
    app.run(debug=True)
    



    





