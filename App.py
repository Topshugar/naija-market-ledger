from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB = 'sales.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY, item TEXT, price REAL, qty INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        item = request.form.get('item')
        price = float(request.form.get('price', 0))
        qty = int(request.form.get('qty', 1))
        c.execute("INSERT INTO sales (item, price, qty) VALUES (?,?,?)", (item, price, qty))
        conn.commit()
    c.execute("SELECT * FROM sales ORDER BY id DESC")
    sales = c.fetchall()
    total = sum(row[2] * row[3] for row in sales)
    conn.close()
    return render_template('index.html', sales=sales, total=total)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM sales WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
