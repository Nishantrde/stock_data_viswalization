import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from collect_nse_data import get_companies_name, get_stock_data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kk'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall() 
    print(posts)
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/companies', methods=['GET'])
def get_companies_data():

    data = get_companies_name()

    return render_template("get_companies_data.html", nse_symbol = data)

# @app.route('/data/<symbol>')
# def get_companies_data(symbol):

#     return render_template("get_companies_data.html")

# @app.route('/summary/<symbol>')
# def get_summary_data(symbol):
    
#     symbol1 = request.args.get('symbol1')
#     symbol2 = request.args.get('symbol2')

#     return render_template("get_summary_data.html")



