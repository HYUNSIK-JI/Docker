from django.db import models
from users.models import User
# Create your models here.

class Country(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) 
    title = models.CharField(max_length=50,blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    country_code = models.CharField(max_length=255)
    like_country = models.ManyToManyField(User, related_name="like_country")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)

    def __int__(self):
        return self.id
class Comment1(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=80)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_comment1 = models.ManyToManyField(User, related_name="like_comment1")