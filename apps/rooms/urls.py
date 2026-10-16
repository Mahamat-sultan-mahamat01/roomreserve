from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
# The router automatically generates URLs for our ViewSet
router = DefaultRouter()
router.register(r"",views.RoomViewSet,basename = "room")
app_name = "rooms"
urlpatterns =[
  #olds views manually
  path('stats/',views.room_stat,name ="stats"),
  #all viewsets urls
  path("v2/",include(router.urls))
 ]




"""
apps_name = 'rooms'
from . import views
urlpatterns =[
    path('',views.room_list,name='list'),
    path('drf/',views.room_list_drf,name ='list_drf'),
    path('stats/',views.room_stat,name='stat'),
    path('<int:pk>/',views.room_detail,name='detail'),
]

"""
