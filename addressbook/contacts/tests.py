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

    def test_create_delete_contact(self):
        """
        Ensure we can create a contact object and then delete it.
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

        contact_pk = Contact.objects.get().pk
        url_delete = reverse('contact-detail',args=[str(contact_pk)])
        response = self.client.delete(url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0) 
    
    def test_create_delete_contactlist(self):
        """
        Ensure we can create a new contact list object and then delete it.
        """
        url = reverse('contactlist-list')
        data = {
            'name' : 'Bcontact'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactList.objects.count(), 1)
        self.assertEqual(ContactList.objects.get().name, 'Bcontact')

        contactlist_pk = ContactList.objects.get().pk
        url_delete = reverse('contactlist-detail',args=[str(contactlist_pk)])
        response = self.client.delete(url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactList.objects.count(), 0)   

    def test_search_contactlist(self):
        """
        Ensure we can create a new contact list object and then search for it.
        """
        url = reverse('contactlist-list')
        data = {
            'name' : 'Bcontact'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactList.objects.count(), 1)
        self.assertEqual(ContactList.objects.get().name, 'Bcontact')

        url_search = reverse('contactlist-list') + '?search=Bcontact'
        response = self.client.get(url_search)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactList.objects.count(), 1)           
        self.assertEqual(ContactList.objects.first().name, 'Bcontact')           

    def test_add_remove_contact_to_contactlist(self):
        """
        Ensure we can create a new contact object 
        and then add it to a contact-list object
        and then remove it from the contact-list object.
        """
        url_create_contactlist = reverse('contactlist-list')
        data_contactlist = {
            'name' : 'Contact List A'
        }
        response = self.client.post(url_create_contactlist, data_contactlist, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactList.objects.count(), 1)
        self.assertEqual(ContactList.objects.get().name, 'Contact List A')
        
        url_create_contact = reverse('contact-list')
        data_contact = {
            'name' : 'Bcontact',
            'address' : 'A contact',
            'phone' : 'A contact',
            'email' : 'A contact'
        }
        response = self.client.post(url_create_contact, data_contact, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Bcontact')

        contactlist_pk = ContactList.objects.get().pk
        url_add_to_contactlist = reverse('contactlist-manage-contact',kwargs={'pk': contactlist_pk})
        contact_pk = Contact.objects.get().pk
        data_add_to_contactlist = {
            'contact_pk' : contact_pk
        }

        response = self.client.post(url_add_to_contactlist, data_add_to_contactlist, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactList.objects.get().name, 'Contact List A')
        self.assertEqual(ContactList.objects.get().contacts.count(), 1)
        self.assertEqual(ContactList.objects.get().contacts.first().name, 'Bcontact')

        url_remove_from_contaclist = reverse('contactlist-manage-contact',kwargs={'pk': contactlist_pk})
        data_remove_from_contactlist = {
            'contact_pk' : contact_pk
        }
        
        response = self.client.delete(url_remove_from_contaclist, data_remove_from_contactlist, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactList.objects.count(), 1)
        self.assertEqual(ContactList.objects.get().contacts.count(), 0)