from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("listing/<str:title>/", views.listing, name = "listing"),
    path("<str:name>/", views.category, name = "category"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path('close_listing/<str:title>/', views.close_listing, name='close_listing'),
]
