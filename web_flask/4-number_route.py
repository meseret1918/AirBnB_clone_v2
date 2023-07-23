#!/usr/bin/python3
""" Starts a Flash Web Application C is FUN"""
from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c(text):
    return 'C {}'.format(text.replace('_', ' '))

@app.route('/c/<int:n>', strict_slashes=False)
def c_number(n):
    return 'C {}'.format(n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

