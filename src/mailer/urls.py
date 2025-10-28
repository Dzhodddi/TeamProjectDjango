from django.urls import path

from mailer import views

urlpatterns = [
    path('email/', views.EmailSender.as_view(), name='email'),
]
