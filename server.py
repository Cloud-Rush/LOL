from flask import Flask, session, redirect, url_for, escape, render_template, request, send_file, jsonify
from riotwatcher import RiotWatcher
from twitch import *
import userManager
import os
import psycopg2
import psycopg2.extras
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.config['GOOGLE_ID'] = "190653571715-6ndr2gudj90tecbi7kv53rqd2joct19b.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "IjdvzoKaYUUE9kE5ZMysMVmo"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
google = oauth.remote_app('google',
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_method='POST',
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET')
)

@app.route('/', methods = ['GET', 'POST'])
def mainIndex():
	return redirect(url_for('register'))
	

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == "POST":
		username= request.form['username']
		pw= request.form['password']
		loginResult = userManager.checkLogin(username, pw)
		if loginResult != "check successful":
			return render_template('login.html', error=loginResult)
		else:
			session["username"] = username
			return render_template('memberIndex.html')
	return render_template('login.html')

@app.route('/loginOauth', methods = ['GET', 'POST'])
def loginOauth():
		return google.authorize(callback=url_for('authorized', _external=True))
	
@app.route('/loginOauth/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return render_template('memberIndex.html')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
    
@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == "POST":
		username= request.form['username']
		pw= request.form['password']
		confirm = request.form['confirm']
		if pw != confirm:
			return render_template('register.html', error="Your passwords do not match")
		result = userManager.registerLogin(username, pw)
		if result != "registration successful":
			return render_template('register.html', error=result)
		else:
			session["username"] = username
			return render_template('memberIndex.html', loggedIn = True)
	else:
		return render_template('register.html')
	

@app.route('/customs', methods = ['GET', 'POST'])
def customs():
	if request.method == "POST":
		return render_template("memberIndex.html")
	else:
		return render_template("customize.html")

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	if session['google_token'] != None:
		session.pop('google_token', None)
		return redirect(url_for("login"))
	else:
		session.pop('username', None)
		return render_template('login.html')
    
if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'AB9830923CJDH90TH32L/'
	app.run(host=os.getenv('IP', '0.0.0.0'), port=int(8080), debug=True)

