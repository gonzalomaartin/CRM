from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save


class User(AbstractUser): 
    is_organizer = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = False)

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self): 
        return self.user.username

class Lead(models.Model): 
    SOURCE_CHOICES = [
        ("Youtube", "Youtube"),  #the first value is the one stored in the database, the second is the one displayed for the user
        ("Google", "Google"), 
        ("Newsletter", "Newsletter"), 
    ]

    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    age = models.IntegerField(default = 0)
    agent = models.ForeignKey("Agent", on_delete = models.SET_NULL, null = True, blank = True) #You need to put it in "" as the class is not defined at that point 
    category = models.ForeignKey("Category", related_name = "leads", on_delete = models.SET_NULL, null = True, blank = True)

    phoned = models.BooleanField(default = False)
    source = models.CharField(max_length = 100, choices = SOURCE_CHOICES, null = True, blank = True) 
    organization = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)

    profile_picture = models.ImageField(blank = True, null = True) 
    special_files = models.FileField(blank = True, null = True)

    def __str__(self): 
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model): #The agent is a person who is charge of communicating and supervising a set of leads 
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    organization = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self): 
        return self.user.email



class Category(models.Model): 
    name = models.CharField(max_length = 30) #New, Contacted, Converted, Unconverted 
    organization = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self): 
        return self.name 


def post_user_created_signal(sender, instance, created, **kwargs): 
    if created: 
        UserProfile.objects.create(user = instance)


post_save.connect(post_user_created_signal, sender = User)
