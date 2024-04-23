from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime,date
import uuid
# Create your models here.

# class Bsaemodel(models.Model):
#     uuid=models.UUIDField(default=uuid.uuid4, editable=False ,primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)


class Amentities(models.Model):
    amentites_name=models.CharField(max_length=100)

    def __str__(self):
        return (self.amentites_name)
    

class Hotel(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    discription=models.TextField(null=True, blank=True)
    image=models.FileField(upload_to='hotel_images')
    image1=models.FileField(upload_to='hotel_images')
    adress=models.CharField(max_length=250)
    mobile=models.CharField(max_length=100)
    emails=models.CharField(max_length=100)
    amentities=models.ManyToManyField(Amentities)
    hotel_price=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    
    rating=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return (self.name)
    
class HotelGallery(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    image1=models.FileField(upload_to='hotel_images')
    image2=models.FileField(upload_to='hotel_images')
    image3=models.FileField(upload_to='hotel_images')
    image4=models.FileField(upload_to='hotel_images',default=None)

    def __str__(self):
        return (self.hotel.name)

ROOM_TYPE=(
    ("Classic","classic"),
    ("Deluxe","Deluxe"),
    ("Saver Single","Saver Single"),
    ("Premium Room With Balcony","Premium Room With Balcony"),
    ("Superior","Superior"),
)
class RoomType(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    type=models.CharField(max_length=100,choices=ROOM_TYPE)
    # price=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    number_beds=models.PositiveIntegerField(default=0)
    room_capacity=models.PositiveIntegerField(default=0)
    # date=models.DateField(auto_now_add=True)
      
    def __str__(self):
        return f'{self.type} , {self.hotel.name}'
    
class Room(models.Model):
    hotel_gallery=models.ForeignKey(HotelGallery,on_delete=models.CASCADE,default=None)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    room_type=models.ForeignKey(RoomType,on_delete=models.CASCADE )
    room_number=models.CharField(max_length=1000)
    is_available=models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room_type.type}, {self.room_number} , {self.hotel.name}' 



BOOKING_TYPE=(
    ('Confirmed', 'Confirmed'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    
)   
    
def present_or_future_date(value):
    # if value < datetime.date.today():
    if value < date.today():
        raise ValueError ("The date cannot be in the past!")
    return value

class HotelBooking(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    check_in_date = models.DateField(default=datetime.now, validators=[present_or_future_date],null=True,blank=True)
    check_out_date = models.DateField(default=datetime.now, validators=[present_or_future_date],null=True,blank=True)
    # check_in_date=models.DateField()
    # check_out_date=models.DateField()
    booking_typ=models.CharField(max_length=100,choices=BOOKING_TYPE,default='Pending')
    num_adults=models.PositiveIntegerField(default=1,null=True,blank=True)
    num_children=models.PositiveIntegerField(default=0,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Booking for {self.user} at {self.hotel} (check-in: {self.check_in_date}, check-out: {self.check_out_date})"
    
RATING=(
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),

)

class Review(models.Model):
    review=models.TextField()
    date=models.DateField(auto_now_add=True)
    hotel=models.ForeignKey(Hotel,on_delete=models.SET_NULL, null=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    # status=models.CharField(max_length=100,default="added")
    rating=models.IntegerField(choices=RATING,default=None)
    

    def __str__(self):
        return f"Review of {self.hotel.name} and Rating{self.rating}"