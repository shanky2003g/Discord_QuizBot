from django.urls import path
from .import views 
urlpatterns = [
    path("", views.dashboard, name= 'dashboard'),
    path("add_sets", views.add_sets, name='add_sets'),
    path("delete/<str:pk>",views.delete,name="delete_set"),
    path("update/<str:pk>",views.update,name="update"),
    path("view/<str:pk>",views.view_questions,name="view"),
]
