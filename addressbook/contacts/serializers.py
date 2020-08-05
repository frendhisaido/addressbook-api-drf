from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from contacts.models import Contact, ContactList

# In serializer we convert data to JSON and do data validations


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'pk',
            'name',
            'address',
            'phone',
            'email'
        ]


class ContactListSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = ContactList
        fields = [
            'pk',
            'name',
            'contacts'
        ]
