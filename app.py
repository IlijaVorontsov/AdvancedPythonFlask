from flask import Flask, url_for, render_template, request, redirect
from markupsafe import escape

app = Flask(__name__)

users = {}

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.__password = password
    def check_password(self, password):
        return self.__password == password
    
@app.route('/')
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        email = request.form['email']
        if password != request.form['psw-repeat']:
            return render_template('register.html', error='Passwords do not match')

        if username in users:
            return render_template('register.html', error='User already exists')
        else:
            users[username] = User(username, password, email)
            return render_template('register.html', error=f'User {username} created')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        if username in users:
            user = users[username]
            if user.check_password(password):
                return f'User {username} logged in'
            else:
                return 'Wrong password'
        else:
            return 'User not found'
    return render_template('login.html')

@app.route('/users')
def list_users():
    return render_template('users.html', users=users)



if __name__ == "__main__":
    app.run(port=8000, debug=True)