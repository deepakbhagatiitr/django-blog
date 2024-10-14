from post.models import Post  # Adjust this import based on your project structure
from django.contrib.auth.models import User
from datetime import datetime
import random

# Replace 'your_user' with the username of the user you want to create posts for
username = 'deepak'
author = User.objects.get(username=username)

# Sample titles and content for posts
titles = [
    "The Journey of Django Development",
    "Understanding Python Decorators",
    "Building RESTful APIs with Django REST Framework",
    "A Guide to Django Models",
    "Optimizing Queries in Django",
    "Django Authentication: A Deep Dive",
    "Creating Forms in Django",
    "Django Signals: What You Need to Know",
    "Testing Django Applications",
    "Deploying Django Applications on Heroku"
]

# Create 10 posts for the specified author
for i in range(10):
    post = Post(
        title=titles[i],
        content=f"This is the content for the post titled '{titles[i]}'. Here you can discuss various aspects of the topic.",
        author=author,
        date=datetime.now()  # Set the current date and time
    )
    post.save()  # Save the post to the database
    print(f"Post '{titles[i]}' created successfully.")

# Exit the shell
exit()
