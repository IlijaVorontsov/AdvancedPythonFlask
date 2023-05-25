from flask import Flask, url_for, render_template, request, redirect
from markupsafe import escape
from mail import *

app = Flask(__name__)

class User:
    def __init__(self, username, email, send = False):
        self.username = username
        self.email = email
        self.__password = generate_password()
        if send:
            send_register_mail(self.email, self.username, self.__password)
    
    def check_password(self, password):
        return self.__password == password
    
    def reset_password(self):
        self.__password = generate_password()
        send_reset_mail(self.email, self.username, self.__password)

users = {}
users['ali'] = User('ali', 'ali@hotmail.com')
users['hans'] = User('hans', 'hans@gmail.com')
users['peter'] = User('peter', 'peter@gmx.at')
users['max'] = User('max', 'max@a1.at')


    
@app.route('/')
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']

        if username in users:
            return render_template('register.html', error='User already exists!')
        else:
            users[username] = User(username, email)
            return render_template('register.html', success=f'User {username} created!')
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

@app.route('/reset', methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        username = request.form['uname']
        if username in users and users[username].email == request.form['email']:
            user = users[username]
            user.reset_password()
            return redirect(url_for('login'))
        else:
            return render_template('reset.html', error='User not found or email wrong!')
    return render_template('reset.html')

@app.route('/list_users')
def list_users():
    return render_template('users.html', users=users)



if __name__ == "__main__":
    app.run(port=8000, debug=True)