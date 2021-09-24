from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCNEMY_DATABASE_URI"] = 'sqlite:///resulte.db'
db = SQLAlchemy(app)


@app.route('/news')
def index():
    return render_template('index.html')


app.run(host='127.0.0.1', debug=True)
