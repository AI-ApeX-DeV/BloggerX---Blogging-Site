import pyrebase
from datetime import datetime
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

firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()

title = "Nikola Tesla"
subtitle = "Great Inventor"
blog = "This blog is about a great inventor Nikola Tesla"
author = "Sharukhali Syed"
current_date = datetime.now()
date = current_date.date()

data = {
    'title': title,
    'subtitle': subtitle,
    'blog': blog,
    'author': author,
    'date': str(date)  # Convert the date object to a string
}
# Push the data to Firebase
db.child('blog_posts').push(data)
