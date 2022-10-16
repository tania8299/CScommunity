from datetime import datetime
import email
from email.policy import default
from pyexpat import model
import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
       user = models.ForeignKey(User,on_delete = models.CASCADE,)
     
       id_user = models.IntegerField()
       bio = models.TextField(blank=True)
       name=models.CharField(max_length=100,blank=True)
       profileimg = models.ImageField(upload_to ='profile_images',default ='black-profile-picture.png')
       location = models.CharField(max_length=100,blank=True)
       contact=models.TextField(blank=True)
       batch =models.CharField(max_length=100,blank=True)
       working=models.TextField()
       techinal_experiance=models.TextField()
       isverified=models.BooleanField(default=False)

       def __str__(self):
                     return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='post_images')
    post_title = models.TextField()
    post_data=models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
           post_id = models.CharField(max_length=500)
           username = models.CharField(max_length=100)
           def __str__(self):
               return self.username

class Commnent(models.Model):
           user = models.CharField(max_length=100)
           comment_data=models.TextField()
           def __str__(self):
               return self.username               


        
               
