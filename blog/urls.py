from django.urls import path
from .views import blog, contact,about


app_name = 'blog'

urlpatterns = [
    path('', blog, name='blog'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]