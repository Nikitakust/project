from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'
db = SQLAlchemy(app)
app.secret_key = '736427652364578236458237465823465823765263485762349875696'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = LoginManager(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zag = db.Column(db.String(126), nullable=False)
    tex = db.Column(db.Text, nullable=False)


class User(db.Model, UserMixin):                                            # Пользователи
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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


@app.route('/view', login_required=True)

def view():
    a = News.query.order_by(News.id).all()
    return render_template('view.html', a=a)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('view'))

            else:
                flash('Неверный логин или пароль')
        else:
            flash('')
    return render_template("auto.html")


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next' + request.url)
    return response


def create_admin():
    hash_pwd = generate_password_hash('A')
    new_user = User(login='admin1212', password=hash_pwd)
    db.session.add(new_user)
    db.session.commit()


app.run(host='127.0.0.1', debug=True)