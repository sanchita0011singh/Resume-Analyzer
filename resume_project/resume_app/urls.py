from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg, name='regpage'),     #  Registration Page
    path('home/', views.homepage, name='homepage'),            # Home Page
    path('upload/', views.upload_resume, name='uploadpage'), #  Upload Page
    path('result/', views.result, name='resultpage'),     #  Result Page
    path('Login/', views.Login, name='Loginpage'),     #  Login Page
    path('logout/', views.Logout, name='logoutpage'),   #logoutpage

]