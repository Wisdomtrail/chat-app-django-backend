from django.urls import path

from chat_app import views

urlpatterns = [
    path('SignUp/', views.signUp),
    path('Login/', views.login),
    path('confirmCode/', views.confirmCode, name='confirm_code'),
]
