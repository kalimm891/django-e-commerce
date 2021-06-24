
from django.urls import path
from . import  views

urlpatterns = [
    path("", views.index, name="shophome"),

    path("about/", views.about, name="aboutus"),
    path("contact/", views.contact, name="contactus"),
    path("tracker/", views.tracker, name="track status"),
    path("search/", views.search, name="search"),
    path("products/<int:myid>", views.productView, name="product details"),
    path("checkout/", views.checkout, name="checkout"),
    path('signup/', views.handleSignup, name= "handleSignup"),
    path('login/', views.handleLogin, name= "handleLogin"),
    path('logout/', views.handleLogout, name= "handleLogout")

   # path("handlerequest/", views.handlerequest, name="HandleRequest")




]