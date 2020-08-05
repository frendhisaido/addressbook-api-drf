# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from contacts.models import Contact, ContactList

class ContactTests(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_contact(self):
        """
        Ensure we can create a new contact object.
        """
        url = reverse('contact-list')
        data = {
            'name' : 'Bcontact',
            'address' : 'A contact',
            'phone' : 'A contact',
            'email' : 'A contact'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Bcontact')

    def test_create_contact_list(self):
        """
        Ensure we can create a new contact list object.
        """
        url = reverse('contactlist-list')
        data = {
            'name' : 'Contact List A'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactList.objects.count(), 1)
        self.assertEqual(ContactList.objects.get().name, 'Contact List A')        