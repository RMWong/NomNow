from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import os
import json
from .models import RestaurantFinder

def index(request):
    hidden = "hidden"
    google_places_library = "<script src='https://maps.googleapis.com/maps/api/js?key="+os.environ['GOOGLE_MAPS_KEY']+"&libraries=places&callback=initAutocomplete'async defer></script>"

    return render(request, 'home/index.html', {'google_places_library': google_places_library, 'hidden': hidden})

def result(request):
    # TODO: refactor and come up with a better way of rendering this library
    google_places_library = "<script src='https://maps.googleapis.com/maps/api/js?key="+os.environ['GOOGLE_MAPS_KEY']+"&libraries=places&callback=initAutocomplete'async defer></script>"
    hidden = 'hidden'

    # TODO: refactor this
    lat = ""
    lng = ""

    if request.method == 'POST':
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        if lat == '' or lng == '':
            return render(request, 'home/index.html', {'location_required': 'Please enter a location to proceed', 'hidden': hidden, 'google_places_library': google_places_library})

    restaurant_finder = RestaurantFinder()
    result = restaurant_finder.search(request)
    name = result.name

    # Keep keyword tags in the form
    keyword_tags = request.POST.getlist("tags", [])
    keywords = ""

    for keyword in keyword_tags:
        keywords += "<li>" + keyword + "</li>"

    # Keep the location in the form
    location = request.POST.get("location")

    # Keep the rating in the form
    rating = request.POST.get("rating")

    if not name:
        hidden = "hidden"
        return render(request, 'home/index.html', {'no_results': 'Sorry, there are no results using this search criteria!',
            'hidden': hidden, 'google_places_library': google_places_library,
            'keywords': keywords,
            'location': location,
            'lat': lat,
            'lng': lng})
    # TODO: error message for missing location
    else:
        rating_stars = result.rating_stars
        rating_stars = "<img src=" + rating_stars + " />"
        poweredByYelpImg = "/static/home/assets/images/yelp_powered_btn_dark.png"
        poweredByYelpImg = "<img src=" + poweredByYelpImg + " />"
        restaurant_photo_url = result.image_url # defaults to 100x100
        restaurant_photo_url = restaurant_photo_url.replace("/ms.jpg", "/l.jpg")  # resize to large
        restaurant_photo_url = "<img src=" + restaurant_photo_url + " class='img-responsive'>"
        restaurant_yelp_url = result.url
        restaurant_yelp_url = "<a href=" + restaurant_yelp_url + ">"

        return render(request, 'home/index.html', {
            'keywords': keywords,
            'location': location,
            'lat': lat,
            'lng': lng,
            'name': 'How about trying out ' + name + '?', 'rating' : rating,
            'rating_stars' : rating_stars,
            'yelp_powered': poweredByYelpImg,
            'restaurant_photo_url': restaurant_photo_url,
            'restaurant_yelp_url': restaurant_yelp_url,
            'google_places_library': google_places_library})

def clear(request):
    # TODO: refactor this. basically the same as the index function

    hidden = "hidden"
    google_places_library = "<script src='https://maps.googleapis.com/maps/api/js?key="+os.environ['GOOGLE_MAPS_KEY']+"&libraries=places&callback=initAutocomplete'async defer></script>"

    return render(request, 'home/index.html', {'google_places_library': google_places_library, 'hidden': hidden})