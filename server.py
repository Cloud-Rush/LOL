from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])


@app.route('/login', methods = ['GET', 'POST'])


@app.route('/register', methods = ['GET','POST'])


@app.route('/customs', methods = ['GET', 'POST'])


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 3000)

