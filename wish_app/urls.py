from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wishes', views.wishes),
    path('wishes/new', views.wish),
    path('post/wish', views.create_wish),
    path('wishes/<int:wish_id>/delete', views.delete_item),
    path('wishes/<int:wish_id>/edit', views.edit_item),
    path('edit/<int:wish_id>/update', views.edit_update),
    path('wishes/<int:wish_id>/granted', views.granted_item),
    path('wishes/<int:wish_id>/like', views.granted_like),
]
