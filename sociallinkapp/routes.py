from flask import render_template, url_for, redirect, flash, request, abort
from sociallinkapp import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')