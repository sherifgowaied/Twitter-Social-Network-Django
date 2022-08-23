from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
import json
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    image = models.ImageField(upload_to="images",default="/images/np.jpeg", blank=True,null=True)

    def __str__(self):
        return f"{self.username}"
    




class Followers(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(User , on_delete=models.CASCADE , related_name="following")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} follow {self.following}"

class Post(models.Model):
    owner =models.ForeignKey(User,  on_delete=models.CASCADE ,related_name="posts_have")
    content = models.CharField(max_length=400)
    likes = models.ManyToManyField(User,related_name="liked_posts")
    time = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(blank=True,null=True,upload_to="images")

    def __str__(self):
        return f"{self.owner} says '{self.content}' has {self.likes}"

class LikedPost(models.Model):
    post_owner = models.ForeignKey(User,related_name="post_owner" ,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name="liked_post",on_delete=models.CASCADE)
    liker = models.ForeignKey(User,related_name="liked",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.liker} is liked {self.post}"

class Comment(models.Model):
    comment_owner = models.ForeignKey(User , on_delete=models.CASCADE , related_name="comment_have")
    post_comment = models.ForeignKey(Post,on_delete=models.CASCADE ,  related_name="post_of_comments")
    content_of_comment = models.CharField(max_length=280)
    date_of_comment = models.DateTimeField(auto_now_add=True)



class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name="from_this", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User , related_name="to_this" , on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    read = models.BooleanField(default=False)


    def serialize(self):
        return {
            "id":self.id ,
            "sender":self.sender.username,
            "receiver":self.receiver.username,
            "sender_image":self.sender.image.url,
            "content":self.content ,
            "sender_email":self.sender.email,
            "timestamp":self.timestamp.strftime( "%H:%M:%S , %d,%Y"), # to format date 

            "read":self.read 
        }

    def __str__(self):
        return   f"{self.sender.username} send {self.receiver.username}"  

