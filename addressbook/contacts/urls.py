from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from contacts import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet)
router.register(r'contact-lists', views.ContactListViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]