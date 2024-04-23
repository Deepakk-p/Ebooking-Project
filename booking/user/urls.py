from django.urls import path
from .views import *


urlpatterns =[
    path('hotel',HomeView.as_view(),name='home'),
    path('hotelDetail/<int:hid>',HotelDetailView.as_view(),name='hotelDetail'),
    path("Myprofile",ProfileView.as_view(),name='myprofile'),
    path('cancel/<int:bid>',cancelorder,name='cancel'),
    # path('addreview/<int:hid>',addreview,name='addreview'),
    path('Search_q',serch_hotel,name='search_q'),
    # path('review',Addreeview.as_view(),name='review'),
    path('booking_det/<int:bid>',BookingDetView.as_view(),name="booking_det")

    
]