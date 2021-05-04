from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path("login", views.login),
    path('trips', views.trips),
    path('logout', views.logout),
    path('add', views.add_trip),
    path('create_trip', views.create_trip),
    path('remove/<int:id>', views.remove_trip),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('show/<int:id>', views.showTrip),
    path('join/<int:id>', views.join),
    path('cancel/<int:id>', views.cancel),
]