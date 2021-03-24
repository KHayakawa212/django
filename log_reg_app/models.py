from django.db import models
import datetime
import re

# validations
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['fName']) < 2:
            errors['fName'] = "First name must be greater than 2 characters!"
        if len(postData['lName']) < 2:
            errors['lName'] = "Last name must be greater than 2 characters!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address format"
        for user in User.objects.all():
            if postData['email'] == user.email_address:
                errors['emailused'] = "This email is already in use, please try again."
        if len(postData['password']) < 9:
            errors['password'] = "Passwords must be greater than 8 characters!"
        if postData['password'] != postData['confirmPW']:
            errors['checkpassword'] = "Passwords do not match!"
        if not postData['birthday']:
            return errors
        date_time_obj = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
        if date_time_obj > datetime.datetime.today():
            errors["birthday"]= "Birthday must be in the past"
        return errors

# models
class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birthday = models.DateField(null=True, blank=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()