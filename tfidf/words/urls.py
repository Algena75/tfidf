from django.urls import path

from . import views

app_name = 'words'

urlpatterns = [
    path('', views.index, name='index'),
    path('files/<int:pk>/', views.file_details, name='file_details'),
    path('add_file/', views.add_file, name='add_file'),
]
