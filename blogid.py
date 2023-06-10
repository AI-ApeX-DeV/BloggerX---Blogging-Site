import pyrebase


def get_blog_data(blog_id):
    # Configure Firebase credentials
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

    # Initialize Firebase
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database
    db = firebase.database()
    blog_posts = db.child('blog_posts').get()
    print(blog_posts.val())
    # Retrieve blog data based on the provided blog_id
    blog_data = db.child("blog_posts").order_by_child(
        "blog_id").equal_to(blog_id).get()

    # Extract the data from the snapshot
    blog_data_dict = blog_data.val()

    # Return the blog data
    return blog_data_dict


# Usage example
blog_id = "e878a"
result = get_blog_data(blog_id)
# print(result)
