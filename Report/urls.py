from django.urls import path
from . import views

app_name = 'Report'

urlpatterns = [
    path('request', views.request_list, name='request'),
    path('request/<int:pk>', views.request_detail, name='request-detail'),
    path('list', views.list_list, name='list'),
    path('list/<int:pk>', views.list_detail, name='list-detail'),
]
