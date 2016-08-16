from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
from .models import RestaurantFinder

# Create your views here.
def index(request):
    hidden = "hidden"
    return render(request, 'home/index.html', {'hidden': hidden})


def result(request):
    restaurant_finder = RestaurantFinder()
    result = restaurant_finder.search(request)
    name = result.name
    if not name:
        return render(request, 'home/index.html', {'no_results': 'Sorry, there are no results using this search criteria!'})
    # TODO: error message for missing location
    else:
        rating = result.rating
        rating_stars = result.rating_stars
        rating_stars = "<img src=" + rating_stars + " />"
        poweredByYelpImg = "/static/home/assets/images/yelp_powered_btn_dark.png"
        poweredByYelpImg = "<img src=" + poweredByYelpImg + " />"
        restaurant_photo_url = result.image_url # defaults to 100x100
        restaurant_photo_url = restaurant_photo_url.replace("/ms.jpg", "/l.jpg")  # resize to large
        restaurant_photo_url = "<img src=" + restaurant_photo_url + ">"
        restaurant_yelp_url = result.url
        restaurant_yelp_url = "<a href=" + restaurant_yelp_url + ">"
        return render(request, 'home/index.html', {
            'name': 'How about trying out ' + name + '?', 'rating' : rating,
            'rating_stars' : rating_stars,
            'yelp_powered': poweredByYelpImg,
            'restaurant_photo_url': restaurant_photo_url,
            'restaurant_yelp_url': restaurant_yelp_url})

def clear(request):
    hidden = "hidden"
    return render(request, 'home/index.html', {'hidden': hidden})