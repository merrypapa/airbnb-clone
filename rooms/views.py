# import math
from django.shortcuts import render, redirect
from django.urls import reverse

# from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView, View, UpdateView
from django.core.paginator import Paginator
from django_countries import countries
from users import mixins as user_mixins
from . import models, forms

# from django.http import HttpResponse
# this is for the HttpResponse


class HomeView(ListView):
    model = models.Room
    paginate_by = 8
    page_kwarg = "page"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", {"pk": pk, "room": room})
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class SearchView(View):
    """ SearchView Definition"""

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                filter_args["country"] = country

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests_gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms_gte"] = bedrooms

                if beds is not None:
                    filter_args["beds_gte"] = beds

                if baths is not None:
                    filter_args["baths_gte"] = baths

                if instant_book == True:
                    filter_args["instant_book"] = True

                if superhost == True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("created")
                paginator = Paginator(qs, 4)
                page = request.GET.get("page", 1)
                page_kwarg = "page"
                rooms = paginator.get_page(page)
                request_copy = request.GET.copy()
                ordering = "created"
                if request.GET.get("page") is not None:
                    request_copy.pop("page")
                urls = request_copy.urlencode()
                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms, "urls": urls},
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

    # ""Search hard coding definition""
    # city = str.capitalize(request.GET.get("city","Anywhere"))
    # s_country = request.GET.get("country","KR")
    # s_room_type = int(request.GET.get("room_type",0))
    # s_facilities = request.GET.getlist("facilities")
    # s_amenities = request.GET.getlist("amenities")
    # instant_book = bool(request.GET.get("instant_book",False))
    # superhost = bool(request.GET.get("superhost",False))
    # price = int(request.GET.get("price",0))
    # guests = int(request.GET.get("guests",0))
    # bedrooms = int(request.GET.get("bedrooms",0))
    # beds = int(request.GET.get("beds",0))
    # baths = int(request.GET.get("baths",0))

    # form = {
    # "city":city,
    # "s_room_type":s_room_type,
    # "s_country":s_country,
    # "price": price,
    # "guests": guests,
    # "bedrooms": bedrooms,
    # "beds": beds,
    # "baths": baths,
    # "s_amenities":s_amenities,
    # "s_facilities":s_facilities,
    # "instant_book":instant_book,
    # "superhost":superhost,
    # }

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()
    # choices = {"countries":countries,"room_types":room_types, "amenities":amenities,"facilities":facilities}

    # rooms = models.Room.objects.all()

    # filter_args = {}
    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city
    # filter_args["country"] = s_country

    # if s_room_type != 0:
    #     filter_args["room_type__pk"] = s_room_type

    # if price != 0:
    #     filter_args["price__lte"] = price

    # if guests != 0:
    #     filter_args["guests_gte"] = guests

    # if bedrooms != 0:
    #     filter_args["bedrooms_gte"] = bedrooms

    # if beds != 0:
    #     filter_args["beds_gte"] = beds

    # if baths != 0:
    #     filter_args["baths_gte"] = baths

    # if instant_book == True:
    #     filter_args["instant_book"] = True

    # if superhost == True:
    #     filter_args["host__superhost"] = True

    # if len(s_amenities) >0 :
    #     for s_amenity in s_amenities:
    #         rooms = rooms.filter(amenities__pk=int(s_amenity))

    # if len(s_facilities) >0 :
    #     for s_facility in s_facilities:
    #         rooms = rooms.filter(facilities__pk=int(s_facility))

    # # rooms = models.Room.objects.filter(**filter_args)
    # rooms = rooms.filter(**filter_args)

    # return render(request, "rooms/search.html",{**form,**choices, "rooms":rooms})


# class RoomDetail(DetailView):
# "" Room Detail View Definition ""
#     model = models.Room

# "USING PAGINATOR METHOD"
# def all_rooms(request):
#     page = request.GET.get("page",1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list,5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html",{"rooms":rooms})
#     except EmptyPage:
#         return redirect("/")


# "Paginator hard coding"
# page = int(page or 1)
# page_size = 5
# offset = (page-1)*page_size
# limit = page_size*page
# all_rooms = models.Room.objects.all()[offset:limit]
# page_count = math.ceil(models.Room.objects.count()/page_size)
# print(page_count)
# return render(request, "rooms/home.html", context={"rooms": all_rooms, "page":page, "page_count":page_count, "page_range": range(1, page_count+1)})
