from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Count,Avg
from django.shortcuts import render,redirect
from account.models import *
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic import TemplateView,ListView,DetailView,DeleteView,View
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from user.forms import ReviewForm




class HomeView(View):
    def get(self, request):
        amenetities_obj=Amentities.objects.all()
        hotel_obj=Hotel.objects.all()
        hotels=hotel_obj

        sort_by=request.GET.get('sort_by')
        search=request.GET.get('search')
        amenetities=request.GET.getlist('amenities')
        

        if sort_by:
            if sort_by=="ASC":
                hotel_obj=hotel_obj.order_by('hotel_price')
            # elif sort_by=="DSC":
            #     hotel_obj=hotel_obj.order_by('-hotel_price')
            else:
                hotel_obj=hotel_obj.order_by('-hotel_price')

           

        if search:
            hotel_obj=hotel_obj.filter(
            Q(adress__icontains=search) | Q(name__icontains=search) )
        
        # if len(amenetities):
        if amenetities:
            hotel_obj=hotel_obj.filter(amentities__amentites_name__in=amenetities).distinct()

        
            
        context={
            "amenetities_obj" : amenetities_obj,
            'hotel_obj':hotel_obj,
            'sort_by':sort_by,
            'search':search,
            'amenetities':amenetities,
            'recommended':hotels
            }
        return render(request,'home.html',context,)
    

class HotelDetailView(DetailView):
    template_name='roomview.html'
    queryset=HotelGallery.objects.all()
    pk_url_kwarg='hid'
    context_object_name='hotel_details'

    def get_context_data(self, **kwargs: Any):
        context=super().get_context_data(**kwargs)
        hid=self.kwargs.get('hid')
        hotel=Hotel.objects.get(id=hid)
        rev=Review.objects.filter(hotel=hotel).order_by("-date")

        ave_rev=Review.objects.filter(hotel=hotel).aggregate(rating=Avg('rating'))

        # review_form=ReviewForm()

        context["reviews"]=rev
        context["avg_rating"]=ave_rev

        # context["review_form"]=review_form

        print(context)
        return context

    


# class HotelDetailView(View):
#     def get(self, request, *args, **kwargs):
#         hid=kwargs.get('hid')
#         hotel_details=HotelGallery.objects.get(id=hid)
#         print(hotel_details)
#         # Review
#         hotel=Hotel.objects.get(id=hid)
#         reviews=Review.objects.filter(hotel=hotel).order_by("-date")
#         # review_form=ReviewForm()
#         return render(request,'roomview.html',{"hotel_details":hotel_details,'reviews':reviews})

    def post(self, request,*args, **kwargs):
            
        # Handle POST request for booking

        hid=kwargs.get('hid')
        hotel=Hotel.objects.get(id=hid)
        user=request.user
        check_in_date = request.POST.get('checkin')
        check_out_date = request.POST.get('checkout')
        num_adults = request.POST.get('num_adults')
        num_children = request.POST.get('num_children')
        HotelBooking.objects.create(hotel=hotel,user=user, check_in_date=check_in_date, check_out_date=check_out_date, num_adults=num_adults, num_children=num_children)
        HotelBooking.booking_typ="Confirmed"
        messages.success(request,"Appoinment Requsted Successfully")

        # return redirect('booking_det')
        return render(request, 'booking_det.html')
    

class ProfileView(ListView):
    template_name="profile.html"
    queryset = HotelBooking.objects.all()
    context_object_name="mybooking"

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset=queryset.filter(user=self.request.user)
        return queryset
    
# def cancelorder(request,**kwargs):
#     bid=kwargs.get('bid') 
#     bookinng=HotelBooking.objects.get(id=bid)
#     bookinng.booking_typ="Cancelled"
#     bookinng.save()

from django.http import HttpResponseNotFound
def cancelorder(request, **kwargs):
    bid = kwargs.get('bid')

    try:
        booking = HotelBooking.objects.get(id=bid)
        booking.booking_typ = "Cancelled"
        booking.save()
        message = "Booking cancelled successfully!"
        return redirect('myprofile')  # Replace with your success URL name

    except HotelBooking.DoesNotExist:
        message = "Booking not found!"
        return HttpResponseNotFound(message) 
    


# class Addreeview(View):
#     def get(self,request):
#         review_form=ReviewForm()
#         return render(request,'roomview.html',{"review_form":review_form})
#     def post(self,request, **kwargs):
#         form_data=ReviewForm(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success.success(request,"reviwe added succesfull")
#             messages.error(request,"error")
#             return redirect ('hotelDetail')
#         else:
#             messages.error(request,"error")
#             return render(request,'roomview.html',{"review_form":form_data})
            


# def addreview(request,**kwargs):
#     review=request.POST.get('rev')
#     hid=kwargs.get('hid')
#     hotel=Hotel.objects.get(id=hid)
#     user=request.user
#     # print(review,hid)

#     # # rating=request.POST.get('rating')
#     Review.objects.create(user=user, review=review, hotel=hotel)
#     messages.success(request,"review added")
#     return redirect('hotelDetail')



# def Addreview(requset,**kwargs):
#     review=requset.POST.get('rev')
#     # print(review)
#     product_id=kwargs.get('pid')
#     product=Products.objects.get(id=product_id)
#     user=requset.user
#     print(review,product_id)
#     Review.objects.create(review=review,user=user, product=product)
#     messages.success(requset,"review added")
#     return redirect('uhome')


def serch_hotel(request):
    hotel=Hotel.objects.all()
    search_q=request.GET.get('search')

    if search_q:
        hotel=hotel.filter(name__icontains=search_q).order_by("-date")

    context={
        "hotel": hotel,
        "search_q": search_q
    }
    
    return render(request,"home.html",context)




# class BookingDetView(View):
#     def get(self,request,*args,**kwargs):
#         rid=kwargs.get('rid')
#         review=Review.objects.get(id=rid)
#         return render(request,"booking_det.html",{"review":review})

class BookingDetView(TemplateView):
    template_name="booking_det.html"
    def get(self,request,*args,**kwargs):
        bbid=kwargs.get('bid')
        BookingDet=HotelBooking.objects.get(id=bbid)
        print(BookingDet)
        return render(request,"booking_det.html",{"BookingDet":BookingDet})
    