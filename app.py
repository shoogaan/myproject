from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g
from data import Articles  # Import the function
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"
app.database = "myflaskapp.db"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

Articles = Articles()


def connect_db():
    return sqlite3.connect(app.database)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        g.db = connect_db()
        g.db.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))
        g.db.commit()
        g.db.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    # If method is GET, serve the form to be filled
    return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method==['POST']:
        username = request.form['username']
        #using candidate to validate the correct password from db
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("SELECT*FROM users WHERE username = %s", [username])

        if result>0:
            #gets the first user of multiple usernames
            data = cur.fetchone()
            password = data['password']

        else:
            error = 'Username Not Found'
            return render_template('login.html', error=error)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
