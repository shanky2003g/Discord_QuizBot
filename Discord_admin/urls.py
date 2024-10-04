from django.urls import path
from .import views 
urlpatterns = [
    path("", views.dashboard, name= 'dashboard'),
    path("add_sets", views.add_sets, name='add_sets')
]
