from django.urls import path
apps_name = 'rooms'
from . import views
urlpatterns =[
    path('',views.room_list,name='list'),
    path('<int:pk>/',views.room_detail,name='detail'),
]