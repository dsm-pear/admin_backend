from django.urls import path
from . import views

app_name = 'Notice'

urlpatterns = [
    path('notice', views.notice_list, name='list'),
    path('notice/<int:pk>', views.notice_detail, name='detail'),
]
