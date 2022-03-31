from flask import Flask, render_template, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/wad'
mongo = PyMongo(app)

@app.route('/')
def home_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if mongo.db.users.count_documents({'username':username}) != 0:
            flash('Username exists!')
            return redirect('/signup')
        
        else:
            mongo.db.users.insert_one({
                'username': username,
                'password': generate_password_hash(password)
            })
            flash('Signed up!')
            return redirect('/auth')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            return render_template('login.html')


@app.route('/story', methods=(["GET","POST"]))
@loggin_required
def post():
    if request.method == "GET":
        return render_template("create_post.html")
    else:
        message = request.form.get('text')
        if not message:
            flash('Post can not be empty')
            return redirect(request.url)
        else : 
            mongo.db.posts.insert_one({"post" : message, "blogger": session ['user']['username']})
            post = mongo.db.posts.find()
            return render_template("story.html", posts = post)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)