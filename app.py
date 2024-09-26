from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    description = db.Column(db.String(200), nullable=True)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=True, nullable=False)
    limit = db.Column(db.Float, nullable=False)

# Routes
@app.route('/')
def index():
    transactions = Transaction.query.all()
    budgets = Budget.query.all()
    return render_template('index.html', transactions=transactions, budgets=budgets)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    category = request.form['category']
    type = request.form['type']
    description = request.form.get('description', '')
    
    new_transaction = Transaction(amount=amount, category=category, type=type, description=description)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_budget', methods=['POST'])
def add_budget():
    category = request.form['category']
    limit = float(request.form['limit'])
    
    new_budget = Budget(category=category, limit=limit)
    db.session.add(new_budget)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
