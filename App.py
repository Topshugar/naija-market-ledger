from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'sales.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, item TEXT, amount INTEGER, date TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    init_db()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM sales ORDER BY id DESC')
    sales = c.fetchall()
    c.execute('SELECT SUM(amount) FROM sales')
    total = c.fetchone()[0] or 0
    conn.close()
    return render_template('index.html', sales=sales, total=total)

@app.route('/add', methods=['POST'])
def add():
    item = request.form['item']
    amount = request.form['amount']
    date = datetime.now().strftime("%d-%m-%Y %H:%M")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO sales (item, amount, date) VALUES (?,?,?)', (item, amount, date))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
