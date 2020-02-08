#encoding: utf-8

from flask import Flask,render_template,request
import config
app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')
def hello_world():
    return 'Hello World!'
@app.route('/login')
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
      pass
@app.route('/register')
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
      pass
if __name__ == '__main__':
    app.run()
