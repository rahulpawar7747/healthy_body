from django.contrib import admin
from django.urls import path
from . import views
from .views import aiapp_view
urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.About, name='about'),
    path('Exercise/', views.Excercise, name='Exercise'),
    path('', views.SignuPage, name='signup'),
    path('signup/', views.SignuPage, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('BMI/', views.bmi, name='BMI'),
    path('weight-gain/', views.weight_gain, name='weight_gain'),
    path('contact/', views.contact, name='contact'),
    path('diet/', views.diet, name='diet'),
    path('help/', views.help, name='help'),
    path('Faq/', views.Faq, name='Faq'),
    path('Terms/', views.Terms, name='Terms'),
    path('Feedback/', views.Feedback, name='Feedback'),
    path('privacy/', views.privacy, name='privacy'),
    path('exercise/', views.exercise, name='exercise'),
    # path('Normal_ai/', views.Normal_ai, name='Normal_ai'),
    path('Underweight/', views.Underweight, name='Underweight'),
    path('Overweight/', views.Overweight, name='Overweight'),
    path('Obese/', views.Obese, name='Obese'),
    path("aiapp/", aiapp_view, name="aiapp"),
]