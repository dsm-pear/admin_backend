from django.urls import path
from . import views

urlpatterns = [
    path('request', views.request_list),
    path('request/<int:pk>', views.request_detail),
    path('list', views.list_list),
    path('list/<int:pk>', views.list_detail),
]