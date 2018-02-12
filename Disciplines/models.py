# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Discipline(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Idea(models.Model):
    subject = models.CharField(max_length=4000)
    last_updated = models.DateTimeField(auto_now_add=True)
    discipline = models.ForeignKey(Discipline,on_delete=models.CASCADE, related_name='ideas')
    starter = models.ForeignKey(User, related_name='ideas',on_delete=models.CASCADE,)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    idea = models.ForeignKey(Idea, related_name='posts',on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,)
    updated_by = models.ForeignKey(User, null=True,related_name='+',on_delete=models.CASCADE,)   
