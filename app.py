from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import urllib
import json
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/amana/OneDrive/Desktop/Movie Library/database.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    

with app.app_context():
    db.create_all()
    

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    

@app.route('/',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            
    return render_template('login.html',form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    movieName = ["Avengers","Avatar"]
    myMovieName = random.choice(movieName)
    try:
        url =  f"http://www.omdbapi.com/?s={myMovieName}&apikey=3153a9ba"
        response = urllib.request.urlopen(url)
        data = response.read()
        jsonData = json.loads(data)["Search"]
        return render_template("dashboard.html" , page_name = "WHAT2WATCH" , movieList = jsonData)
    except Exception as e:
        
        return render_template("dashboard.html" , page_name = "WHAT2WATCH")


@app.route("/search",methods=['Get'])
def search_results():
    movieName = request.args.get("query")
    try:
        url =  f"http://www.omdbapi.com/?s={movieName}&apikey=3153a9ba"
        url = url.replace(" ", "%20")
        response = urllib.request.urlopen(url)
        data = response.read()
        jsonData = json.loads(data)["Search"]
        return render_template("dashboard.html" , page_name = "SEARCH RESULTS" , movieList = jsonData,myquery = movieName)
    except Exception as e:
        print(e)
        return f"NO INTERNET CONNECTION {e}"


'''
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
'''

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html',form = form)
