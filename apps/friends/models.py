from __future__ import unicode_literals
import bcrypt
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, pass_conf, birthday):
        errors = {}
        if (len(name) < 2):
            errors['name'] = "Name must be at least two characters long"

        if (len(alias) < 2):
            errors['alias'] = "Alias must be at least two characters long"

        if (len(password) < 8):
            errors['password'] = "Password must be at least eight characters long"

        if (password != pass_conf):
            errors['password'] = "Passwords do not match"
        try:
            existingUser = self.get(email__iexact=email)
        except:
            existingUser = None
        if (existingUser):
            errors['email'] = 'Email already exists'

        if (not EMAIL_REGEX.match(email)):
            errors['email'] = 'Invalid email'

        if (birthday == None):
            error['birthday'] = 'Please enter date of birth'

        if (errors):
            return (False, errors)
        else:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            self.create(email=email, name=name, alias=alias, password=password, birthday=birthday)

            return (True, self.get(email=email))

    def login(self, email, password):
        try:
            user = self.get(email__iexact=email)
        except:
            user = None
        if user and bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            return (True, user)

        return(False, "login failed")

    def addFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        Friend.objects.create(user_friend=user, friend_2=friend)
        Friend.objects.create(user_friend=friend, friend_2=user)

    def removeFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        friendship1 = Friend.objects.get(user_friend=user, friend_2=friend)
        friendship2 = Friend.objects.get(user_friend=friend, friend_2=user)
        friendship1.delete()
        friendship2.delete()

class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
    objects = models.Manager()

class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester')
    friend_2 = models.ForeignKey(User, related_name='accepter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
