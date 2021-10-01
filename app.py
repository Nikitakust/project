from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'
db = SQLAlchemy(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zag = db.Column(db.String(126), nullable=False)
    tex = db.Column(db.Text, nullable=False)


@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        a = 'Заголовок: ' + request.form.get('Tem')
        prob = 'Текст: '
        b = request.form.get('Mes')
        c = News(zag=a, tex=b)
        db.session.add(c)
        db.session.commit()
        return redirect('/view')
    return render_template('write.html')


@app.route('/view')
def view():
    a = News.query.order_by(News.id).all()
    return render_template('view.html', a=a)


app.run(host='127.0.0.1', debug=True)