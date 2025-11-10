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
def get_companies():

    data = get_companies_name()

    return render_template("get_companies_name.html", nse_symbol = data)

@app.route('/data/<symbol>')
def get_companies_data(symbol):

    companies = get_companies_name()
    data = get_stock_data(symbol)

    return render_template("get_companies_data.html", stock_data = data, symbols = companies)

@app.route('/summary/<symbol>')
def get_companies_summary(symbol):

    companies = get_companies_name()
    data = get_stock_data(symbol, days=364)

    return render_template("get_companies_summary.html", stock_data=data, symbols=companies)
    
@app.route('/compare')
def get_compare_companies():

    # http://127.0.0.1:5000/compare?symbol1=RELIANCE&symbol2=TCS

    
    sym1 = request.args.get("symbol1")
    sym2 = request.args.get("symbol2")
    print(sym1, sym2)

    sym1_data_month = get_stock_data(sym1)
    sym1_data_yr = get_stock_data(sym1)

    sym2_data_month = get_stock_data(sym2)
    sym2_data_yr = get_stock_data(sym2, days=364)



    return render_template("comapre_companies_summary.html", 
        sym1=sym1,
        sym2=sym2,
        sym1_data_month=sym1_data_month,
        sym2_data_month=sym2_data_month,
        sym1_data_yr=sym1_data_yr,
        sym2_data_yr=sym2_data_yr)



# @app.route('/summary/<symbol>')
# def get_summary_data(symbol):
    
#     symbol1 = request.args.get('symbol1')
#     symbol2 = request.args.get('symbol2')

#     return render_template("get_summary_data.html")



