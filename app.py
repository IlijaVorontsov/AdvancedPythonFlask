from flask import Flask, url_for, render_template, request, redirect, session
from markupsafe import escape
from mail import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # 'postgresql://128.0.0.41:5432/users'

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    __password = db.Column(db.String(120), nullable = False)
    def __init__(self, username, email, send = False):
        self.username = username
        self.email = email
        self.__password = generate_password()
        print(f'User {username} created with password {self.__password}')
        if send:
            send_register_mail(self.email, self.username, self.__password)
    def check_password(self, password):
        return self.__password == password
    def reset_password(self):
        self.__password = generate_password()
        send_reset_mail(self.email, self.username, self.__password)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    price = db.Column(db.Float, nullable = False)
    text = db.Column(db.String(120), nullable = False)
    def __init__(self, name, price, text):
        self.name = name
        self.price = price
        self.text = text
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    products = db.session.execute(db.select(Products)).scalars().all()
    return render_template('products.html', products=products)

@app.route('/products/<int:product_id>')
def product(product_id):
    product = db.session.execute(db.select(Products).where(Products.id == product_id)).scalar()
    return render_template('product.html', product=product)

@app.route('/add_product', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        text = request.form['text']

        product = db.session.execute(db.select(Products).where(Products.name == name)).scalar()

        if product is not None:
            return render_template('add_product.html', error='Product already exists!')
        else:
            product = Products(name, price, text)
            db.session.add(product)
            db.session.commit()
            return render_template('add_product.html', success=f'Product {name} created!')
    return render_template('add_product.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']

        user = db.session.execute(db.select(User).where(User.username == username)).scalar()

        if user is not None:
            return render_template('register.html', error='User already exists!')
        else:
            user = User(username, email, send=True)
            db.session.add(user)
            db.session.commit()
            return render_template('register.html', success=f'User {username} created!')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        
        user = db.session.execute(db.select(User).where(User.username == username)).scalar()
        if user is not None:
            if user.check_password(password):
                print(f'User logged in!')
                return redirect(url_for('list_users'))
            else:
                return render_template('login.html', error='Wrong password!')
        else:
            return render_template('login.html', error='User not found!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/reset', methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        username = request.form['uname']
        user = db.session.execute(db.select(User).where(User.username == username)).first()
        if user is not None and user.email == request.form['email']:

            user.reset_password()
            return redirect(url_for('login'))
        else:
            return render_template('reset.html', error='User not found or email wrong!')
    return render_template('reset.html')

@app.route('/list_users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)