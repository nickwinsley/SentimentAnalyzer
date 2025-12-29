from flask import Flask, render_template, request, redirect, url_for, Blueprint
import joblib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

auth = Blueprint('auth', __name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:////app/data/users.db',
    'records': 'sqlite:////app/data/records.db'
}

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

def queryRecord(idNum):
    data = Query.query.filter_by(user_id = idNum).with_entities(Query.message, Query.sentiment, Query.timestamp).all()
    
    results = [sql_to_dict(row) for row in data]

    return (results[-5:])

def sql_to_dict(row):
    return row._asdict()

class Query(db.Model):

    __bind_key__ = 'records'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    message = db.Column(db.Text, nullable = False)
    sentiment = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, unique = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)

class User(db.Model, UserMixin):

    __bind_key__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def PredictSentiment(input):
    model = joblib.load('sentiment.joblib')
        
    response = model.predict([input])
    
    res = "Negative" if response == 0 else "Positive"

    record = Query(message = input, sentiment = res, user_id = current_user.get_id())

    db.session.add(record)

    db.session.commit()

    return record

@app.route('/')
def start():
    return redirect(url_for('auth.signup'))

@app.route('/main')
def setUp():
    return render_template('form.html', result = queryRecord(idNum = current_user.get_id()))

@app.route('/process', methods = ['POST'])
def process():

    if request.method == 'POST':

        input = request.form.get('user_string', '')

        response = PredictSentiment(input)

        results = queryRecord(idNum = current_user.get_id())

        return render_template('results.html', result = response)

    return redirect(url_for('setUp'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods = ["POST"])
def login_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()

    if (not user):
        return redirect(url_for('auth.signup'))

    password_hash = user.password

    if (not check_password_hash(password_hash, password)):
        return redirect(url_for('auth.login'))

    return redirect(url_for('setUp'))

@auth.route('/signup', methods = ["POST"])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()

    if user:
        return redirect(url_for('auth.login'))

    new_user = User(email = email, name = name, password = generate_password_hash(password))

    db.session.add(new_user)

    db.session.commit()

    return redirect(url_for('setUp'))

if (__name__ == '__main__'):

    app.register_blueprint(auth)
    
    with app.app_context():
        db.create_all()

    app.run(host = "0.0.0.0", port = 8080)
