from django.contrib import admin
from .models import Hotel,Amentities,HotelGallery,RoomType,Room,HotelBooking,Review
# # Register your models here.

admin.site.register(Hotel)
admin.site.register(HotelGallery)
admin.site.register(Amentities)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(HotelBooking)
admin.site.register(Review)
