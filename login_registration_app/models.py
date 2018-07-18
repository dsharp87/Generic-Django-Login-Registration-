# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name_length"] = "First Name must be at least two characters"
        if not postData['first_name'].isalpha():
            errors["first_name_alpha"] = "Your First Name can be only letters(no numbers, spaces, or symbols)"
        if len(postData['last_name']) < 2:
            errors["last_name_length"] = "First Name must be at least two characters"
        if not postData['last_name'].isalpha():
            errors["last_name__alpha"] = "Your First Name can be only letters(no numbers, spaces, or symbols)"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be of valid format 'xxx@xxx.xxx'"
        if User.objects.filter(email = postData['email']):
            errors['email_exists'] = "We haz one already"
        upper_count = 0
        num_count = 0
        for char in range(0, len(postData['password'])):
            if postData['password'][char].isupper():
                upper_count += 1
            if postData['password'][char].isdigit():
                num_count += 1
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters" 
        elif upper_count == 0 or num_count == 0:
            errors["password_chars"] = 'Password must contain at least one upper case letter and one number'
        if not postData['password'] == postData['password_comfirmation']:
            errors['email_confirmation'] = "Password Confirmation must match Password"
        
        if len(errors):
            print "i failed"
            return (False, errors)
        else:
            print "i passed"
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hash_pw)
            return (True, user)

    def login_validator(self, postData):
        errors = {}
        attempt_user = User.objects.filter(email = postData['email'])
        if len(attempt_user) == 0:
            errors['not_found'] = 'we do not have a user with this email on reccord'
            return (False, errors)
        elif len(attempt_user) > 1:
            errors['dupes'] = 'we have multiple accounts with this email....HOW DO??!?!'
            return (False, errors)
        else:
            print attempt_user[0].password
            print bcrypt.checkpw(postData['password'].encode(),attempt_user[0].password.encode())
            if bcrypt.checkpw(postData['password'].encode(), attempt_user[0].password.encode()):
                return (True, attempt_user[0])
            else:
                errors['pw_fail'] = 'your password is incorrect NOOB'
                return(False, errors)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


