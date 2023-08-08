from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('random', views.random, name='random'),
    path('wiki/<str:entry>/', views.entry, name='entry'),
    path('search', views.search, name='search'),
    path('new_entry', views.create, name='new_entry'),
    path('edit/<str:entry>', views.edit, name = 'edit')
]
