from django.urls import path
from . import views

app_name = 'Question'

urlpatterns = [
    path('question', views.questions, name='list'),
]
