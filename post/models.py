from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=255)  # Title of the article
    content = models.TextField()              # Content of the article
    date = models.DateField(default=timezone.now)  # Date of publication
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Author of the article

