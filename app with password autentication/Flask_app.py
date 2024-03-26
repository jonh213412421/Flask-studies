from flask import Flask, render_template, request, redirect, url_for, session
import socket
from flask_autoindex import AutoIndex
from functools import wraps

path = ''
app = Flask(__name__)
with open("secret.txt", "r") as f:
    app.secret_key = f.read()

#wraps other functions and force login autentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        with open("users.txt", "r") as f:
            for line in f:
                stored_user, stored_password = line.strip().split(':')
                if user == stored_user and password == stored_password:
                    session['user'] = user
                    return redirect(url_for('index'))

        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/ipconfig')
@login_required
def ipconfig():
    ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[2][4][0]
    print(f"ipv6 solicitado: {ipv6}")
    return ipv6

@app.route('/storage')
@login_required
@app.route('/storage/<path:path>')
def storage(path='.'):
    http = AutoIndex(app)
    return http.render_autoindex(path)

def app_run(host, port):
    app.run(host=host, port=port, debug=True)
