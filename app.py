from flask import Flask, render_template



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html', title = ' Oderman Pizzeria!', a = 'Our Menu', head_title = 'Odrman Italiano')


@app.route('/menu')
def menu():
    pizzas = [
        {"name": "Margherita", "ingredients": "Tomato sauce, mozzarella, basil", "price": "$3.15"},
        {"name": "Pepperoni", "ingredients": "Tomato sauce, mozzarella, pepperoni", "price": "$3.95"},
        {"name": "Hawaiian", "ingredients": "Tomato sauce, mozzarella, pineapple, chicken", "price": "$3.70"}
    ]
    return render_template("menu.html", name_pizza = 'Name of pizza', ing = 'Ingridients',pizzas=pizzas)
    





if __name__ == '__main__':
    app.run(debug=True)