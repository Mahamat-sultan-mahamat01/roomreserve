
from django.urls import path,include
from rest_framework.routers import DefaultRouter 
from .import views
router =DefaultRouter()
router.register(r"",views.ReservationViewSet,basename= "reservations")
app_name ='reservations'
urlpatterns=[
    path("v2/",include(router.urls)),
    path('',views.reservation_list,name='list'),
    path('create/',views.reservation_create,name='create'),
]
