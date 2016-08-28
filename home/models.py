from django.db import models

# Create your models here.
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
import random
import os

class RestaurantFinder(models.Model):

    def __init__(self):
        self.name = ''
        self.rating = ''
        self.rating_stars = ''
        self.image_url = ''
        self.url = ''

    def search(self, request):
        if request.method=='POST':
            consumer_key = os.environ['YELP_CONSUMER_KEY']
            consumer_secret =  os.environ['YELP_CONSUMER_SECRET']
            token = os.environ['YELP_TOKEN']
            token_secret = os.environ['YELP_TOKEN_SECRET']

            auth = Oauth1Authenticator(consumer_key, consumer_secret, token, token_secret)
            client = Client(auth)

            keywords = request.POST.getlist("tags", [])

            input_rating = request.POST.get("rating")

            lat = request.POST.get("lat")
            lng = request.POST.get("lng")

            keywords_filter = ""

            for keyword in keywords:
                keywords_filter += keyword + ","

            keywords_filter = keywords_filter[:-1]

            businesses = []
            # 3 iterations of offsets
            # from offset between 0 and 41
            # may consider searching for less because of the performance hit
            for offset in range(0,41,20):
                params = {
                    # we use the term field to search
                    'term' : keywords_filter,
                    'offset': offset,
                    'limit' : 20,
                    #'sort' : 2, had to turn off this sort to yield more results
                    'category_filter': 'restaurants'
                    # category_filter only has some supported filters
                    # https://www.yelp.com/developers/documentation/v2/all_category_list
                    # if an unsupported category_filter is used, yelp throws an
                    # inavlid_parameter exception
                    # category_filter to restrict to restaurants
                }
                # TODO: more robust error handling
                if (lat != "" and lng != ""):
                    response = client.search_by_coordinates(lat,lng, **params)
                else:
                    return self

                businesses += response.businesses

            restaurants = {}

            restaurant_index = 0
            for index in range(len(businesses)):
                response_rating = businesses[index].rating
                if self.hasMinimumRating(input_rating, response_rating):
                    restaurants[restaurant_index] = businesses[index]
                    restaurant_index += 1

            if not restaurants:
                return self

            chosen_restaurant = random.choice(restaurants)

            self.name = chosen_restaurant.name
            self.rating = chosen_restaurant.rating
            self.rating_stars = chosen_restaurant.rating_img_url_large
            self.image_url = chosen_restaurant.image_url
            self.url = chosen_restaurant.url

        return self

    def hasMinimumRating(self, input_rating, response_rating):
        return float(input_rating) <= float(response_rating)