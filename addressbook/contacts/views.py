from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from django.core import serializers
from rest_framework import status
from contacts.models import Contact, ContactList
from .serializers import ContactSerializer, ContactListSerializer
from rest_framework.decorators import action


class ContactViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions. - DRF Docs

    override get_queryset and perform_create to add user context
    """
    queryset = Contact.objects.filter()
    serializer_class = ContactSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContactListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions. - DRF Docs

    override get_queryset and perform_create to add user context
    """
    queryset = ContactList.objects.filter()
    serializer_class = ContactListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter] # allow add search query to GET list URL ?search=keyword
    search_fields = ['name'] # fields that will be search against
    
    # Add contact to ContactList URL: ~/contact-lists/2/contacts/
    @action(methods=['POST','DELETE'], detail=True, url_path='contacts')
    def manage_contact(self, request, *args, **kwargs):
        contact_list = self.get_object() # get current contact-list model object 
        contact_pk = request.data['contact_pk'] 
        contact = Contact.objects.get(pk=contact_pk)
        response_status = status.HTTP_201_CREATED
        if request.method == 'POST':
            contact_list.contacts.add(contact)
        else: # method == DELETE
            contact_list.contacts.remove(contact)
            response_status = status.HTTP_200_OK
        serializer = ContactListSerializer(instance=contact_list) # serialize for response
        return Response(data=serializer.data, status=response_status)    

    def get_queryset(self, *args, **kwargs):
        return ContactList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
