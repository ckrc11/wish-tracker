from __future__ import unicode_literals
from django.db import models
import re
from datetime import date, datetime
from time import strptime
Name_Regex = re.compile(r'^[A-Za-z ]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if len(postData['first']) < 2:
            errors.append("First Name needs to be more than 1 letter")
        if not Name_Regex.match(postData['first']):
            errors.append("name can only be letters")
        if len(postData['last']) < 2:
            errors.append("Last Name needs to be more than 1 letter")
        if not Name_Regex.match(postData['first']):
            errors.append("name can only be letters")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Username already exists")
        if len(postData["email"])==0:
            errors.append("Please provide an email address")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Please provide a valid email address")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")
        if len(errors) == 0:
            #create the user
            new_user = User.objects.create(first_name = postData['first'], last_name=postData['last'], email= postData['email'], password= postData['password'])
            return (True, new_user)
        else:
            return (False, errors)

    def login(self, postData):
        errors = []
        if 'email' in postData and 'password' in postData:
            try:
                user = User.objects.get(email = postData['email'])#userManage acceses the database using .get (finds that one user's object)
            except User.DoesNotExist: #if the user doesnt exist from the .get(.get returns nothin, this 'except' prevents an error message)
                errors.append("Sorry, this user doesn not exist")
                return (False, errors)
        #password field/check
        if postData['password'] == user.password:
            return (True, user)
        else:
            errors.append("Email or username is incorrect.")
            return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    email= models.CharField(max_length=50)
    objects = userManager()

class wishManager(models.Manager):
    def createwish(self, postData, id):
        curr_user = User.objects.get(id=id)
        errors=[]
        if len(postData['wish']) == 0:
            errors.append("A wish must be provided")
        elif len(postData['wish']) < 2:
            errors.append("A wish must consist of at least 3 characters")
        if len(postData['description']) == 0:
            errors.append("A description must be provided")
        elif len(postData['description']) < 2:
            errors.append("A description must consist of at least 3 characters")
        
        if errors:
            return [False, errors]
        
        wishes = Wish.objects.create(item=postData['wish'], description=postData['description'], wisher=curr_user)
        return [True]
    
    def editthewish(self, wishId, postData):
        errors=[]
        if len(postData['wish']) == 0:
            errors.append("A wish must be provided")
        elif len(postData['wish']) < 2:
            errors.append("A wish must consist of at least 3 characters")
        if len(postData['description']) == 0:
            errors.append("A description must be provided")
        elif len(postData['description']) < 2:
            errors.append("A description must consist of at least 3 characters")
        if errors:
            return [False, errors]

        editwish = Wish.objects.get(id=wishId)
        editwish.item = postData['wish']
        editwish.description = postData['description']
        editwish.save()
        return [True]


    def grantwish(self, wishId):
        wish = Wish.objects.get(id=wishId)
        wish.date_granted = datetime.now
        wish.granted = True
        wish.save()

    def deletewish(self, wishId):
        wish = Wish.objects.get(id=wishId)
        wish.delete()

class Wish(models.Model):
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    date_granted = models.DateField(auto_now=True)
    granted = models.BooleanField(default=False)
    wisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "wisher")
    objects = wishManager()