from flask import Flask, redirect, url_for, jsonify, request, session, flash, render_template
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JustDemonstrating'

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"],"HS256")
            return "Hello " + data["user"]
        except:
            return jsonify({'message': 'Invalid token'}), 403 
        return func(*args, **kwargs) 
    return wrapped             

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('login.html')
       


@app.route('/public')
def public():
    return 'Anyone can veiw this' 

@app.route('/auth')
@check_for_token
def authorised():
    return ' '

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password']:
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
         return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "login in'})
    return render_template("login.html")
                                

if __name__=="__main__":
    app.run(debug=True)              