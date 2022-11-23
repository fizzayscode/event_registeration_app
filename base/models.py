from contextlib import nullcontext
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

# i dont want my id generate from one it can easy be tracked and guessed by other users i want uuid
# to override the default id django thats starts from 1
import uuid

# Create your models here.
##one to one relationship between the user and the profile connect the two with django signals 

#django has a built-in user model and we can customize that to our liking 
class User(AbstractUser):
    #setting the null attribute to true because i already have a user in my db
    name= models.CharField(max_length=100,null=True)
    # email overriding from the parent class
    email= models.EmailField(unique=True,null=True)
    bio= models.TextField(null=True,blank=True)
    is_participant=models.BooleanField(default=True, null=True)
    avatar=models.ImageField(default='profile.png')

    # for resizing a picture maybe you dont want to uplaod a heavy picture in your s3 bucket
    # avatar=models.ResizedImageField(size=[10,10],default='profile.png')
    # uuid4 is a random creator of hex values
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    # tell django use the email field as the username, i want user to log in with email instead of username 
    USERNAME_FIELD= 'email'

    # creatsuperuser command is going to prompt and ask for a
    #  username before i am able to create a superuser
    REQUIRED_FIELDS=['username']


class Event(models.Model):
    name= models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    # we want multiple users to be able to register for multiple events 
    # i can use related names incase i want to get some events a user is in with a keyword 
    # but _set uses the same 
    participants=models.ManyToManyField(User,blank=True,related_name='events')
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)
    reg_deadline=models.DateTimeField(null=True)
    
    # auto_now whenever this field gets updated or modified it gets a timestamp
    updated=models.DateTimeField(auto_now=True)

    # auto_now_add take the timestamp when the event was first created 
    created=models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self):
        return self.name

# we want both a user and a event to keep track of a submisson
class Submission(models.Model):
    # if a user is deleted we dont want to delete the user thats why its set null
    #  we still want a record for that submission
    # says hey the submissin is still here but doesnt have a parent 
    participant=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event= models.ForeignKey(Event,on_delete=models.SET_NULL, null=True )
    description=models.TextField(null=True, blank=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        # we want it to be a string value  so we will get the paricipant thats the user and the event
        return str(self.event) + ' -----------'+ str(self.participant)