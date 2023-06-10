from flask import Flask, render_template, request, redirect, url_for, flash
import pyrebase
import binascii
from datetime import datetime
import json
app = Flask(__name__)
app.secret_key = '1234'

config = {
    "apiKey": "AIzaSyDJYCcDXmQcSTO6YLtqlKcPD6-UwUc68bs",
    "authDomain": "blog-5b8b5.firebaseapp.com",
    "databaseURL": "https://blog-5b8b5-default-rtdb.firebaseio.com",
    "projectId": "blog-5b8b5",
    "storageBucket": "blog-5b8b5.appspot.com",
    "messagingSenderId": "663128229985",
    "appId": "1:663128229985:web:e1a057fb66b845bad2c220",
    "measurementId": "G-8ZNYK8W1LJ"
}


@app.route('/')
def index():
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    # blog_posts = db.child('blog_posts').get()
    blog_posts = db.child('blog_posts').order_by_child(
        'time').limit_to_last(5).get()

    # Render the template with the newest_posts data
    return render_template('index.html', newest_posts=blog_posts)


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/api/posts/<string:post_id>')
def postid(post_id):
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    # Retrieve the data based on the postid
    blog_data = db.child("blog_posts").order_by_child(
        "blog_id").equal_to(post_id).get()

    # Extract the data from the snapshot
    # blog_data_dict = blog_data.val()
    print(blog_data)
    # Render the template with the newest_posts data
    return render_template('posts_complete.html', newest_posts=blog_data)


@app.route('/api/posts')
def posts():
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    blog_posts = db.child('blog_posts').get()

    # Render the template with the newest_posts data
    return render_template('posts.html', newest_posts=blog_posts)


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        blog = request.form['blog']
        author = request.form['author']
        current_date = datetime.now()
        date = current_date.date()
        time = current_date.time()
        category = request.form['category']
        combined_string = f"{title}{subtitle}{blog}{author}{str(date)}{category}{time}"

        crc32_hash = binascii.crc32(category.encode('utf-8'))

        # Convert the hash to a positive integer
        crc32_hash = crc32_hash & 0xffffffff

        # Convert the hash to a 5-character hexadecimal string
        category_id = format(crc32_hash, 'x')[:5]

        crc32_hash = binascii.crc32(combined_string.encode('utf-8'))

        # Convert the hash to a positive integer
        crc32_hash = crc32_hash & 0xffffffff

        # Convert the hash to a 5-character hexadecimal string
        blog_id = format(crc32_hash, 'x')[:5]

        data = {
            'title': title,
            'subtitle': subtitle,
            'blog': blog,
            'author': author,
            'date': str(date),
            'category': category,
            'category_id': category_id,
            'blog_id': blog_id,
            'time': str(time)    # Convert the date object to a string
        }
        # Push the data to Firebase
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        db.child('blog_posts').push(data)

    flash("Blog added successfully")
    return redirect('/')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        phone = request.form['phone']
        flash('Thanks for submitting your details')
        firebase = pyrebase.initialize_app(config)

        # Get a reference to the database service
        db = firebase.database()

        # Create a dictionary with the data
        data = {"name": name, "email": email,
                "phone": phone, "message": message}

        # Store the data in a child node of the database
        db.child("contacts").push(data)
    return render_template('index.html')


@app.route('/api/categories/<string:category_id>/posts')
def category_posts(category_id):
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    blog_data = db.child("blog_posts").order_by_child(
        "category_id").equal_to(category_id).get()

    # Render the template with the newest_posts data
    return render_template('posts.html', newest_posts=blog_data)


@app.route('/api/categories')
def categories():
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    blog_posts = db.child('categories').get()
    blog_data = db.child("blog_posts").order_by_child(
        "category").get()
    # Render the template with the newest_posts data
    return render_template('category.html', newest_posts=blog_data)


@app.route('/api/categories/<string:category_id>')
def category(category_id):
    # Get a reference to the Firebase database
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    blog_data = db.child("blog_posts").order_by_child(
        "category_id").equal_to(category_id).get()

    # Render the template with the newest_posts data
    return render_template('category.html', newest_posts=blog_data)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post')
def post():
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    # Retrieve the blog posts data from Firebase
    blog_posts = db.child('blog_posts').get()

    # Render the template with the newest_posts data
    return render_template('post.html', newest_posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)
