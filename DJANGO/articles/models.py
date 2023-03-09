from django.db import models
from users.models import User
# Create your models here.

class Articles(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) 
    title = models.CharField(max_length=50,blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    like_articles = models.ManyToManyField(User, related_name="like_articles")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Photo(models.Model):
#     ariticles = models.ForeignKey(Articles, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="images/", blank=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=80)
    ariticles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_comment = models.ManyToManyField(User, related_name="like_comment")