from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# https://www.django-rest-framework.org/tutorial/1-serialization/
# https://dbdiagram.io/d/5f2198b97543d301bf5d2eb2


class Contact(models.Model):
    # 'pk' is like id and created by default
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User',related_name='user_contacts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ContactList(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.ManyToManyField(Contact)
    user = models.ForeignKey('auth.User',related_name='user_lists', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']