from django.db import models
from django.db import models
import re, datetime
import bcrypt
# Create your models here.

class UsersManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"

        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Please enter a valid email address!"
        elif len(Users.objects.filter(email=postData['email'])) > 0:
            errors['used'] = "Email address is already in use"

        if len(postData['password']) < 8:           
            errors['password'] = "Password should be at least 8 characters"

        if postData['password'] != postData['conf_pass']:
            errors['mismatch'] = "Passwords should match"

        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postData['email']):            
            errors['login_email'] = "Please enter a valid email address!"

        if len(Users.objects.filter(email = postData['email'])) == 0:
            errors['email'] = "Email or password is incorrect"
        else:
            user = Users.objects.filter(email = postData['email'])
            user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['email'] = "Email or password is incorrect"

        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()


class TripsManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        
        if len(postData['dest']) < 3:
            errors['dest'] = "A trip destination must be at least 3 characters"
        if len(postData['st_date']) < 1:
            errors['st_date'] = "A start date must be provided"
        elif postData['st_date']:
            st_date = datetime.datetime.strptime(postData['st_date'], "%Y-%m-%d")
            en_date = datetime.datetime.strptime(postData['en_date'], "%Y-%m-%d")
            if datetime.datetime.today() > st_date:
                errors['date_less'] = "date must be in the future"
            if st_date > en_date:
                errors['date_err'] = " end date must be after the start date"
            
        if len(postData['plan']) < 2:
            errors['plan'] = "A plan must be at least 2 characters"

        
        return errors


class Trips(models.Model):
    destnation = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    plan = models.TextField()
    created_by = models.ForeignKey(Users, related_name="trip", on_delete = models.CASCADE)
    on_trip = models.ManyToManyField(Users, related_name="trips")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripsManager()