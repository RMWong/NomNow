from django.db import models

# Create your models here.
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
import random
import os

class RestaurantFinder(models.Model):

    name = ''
    rating = ''
    rating_stars = ''
    image_url = ''
    url = ''

    def search(self, request):
        result = ''
        if request.method=='POST':
            # with io.open('config_secret.json') as cred:
            #     creds = json.load(cred)
            #     auth = Oauth1Authenticator(**creds)
            #     client = Client(auth)

            consumer_key = os.environ['YELP_CONSUMER_KEY']
            consumer_secret =  os.environ['YELP_CONSUMER_SECRET']
            token = os.environ['YELP_TOKEN']
            token_secret = os.environ['YELP_TOKEN_SECRET']

            auth = Oauth1Authenticator(consumer_key, consumer_secret, token, token_secret)
            client = Client(auth)

            keywords = request.POST.getlist("tags", [])

            input_rating = request.POST.get("rating")
            location = request.POST.get("location")

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
                    'sort' : 2, #had to turn off this sort to yield more results
                    'category_filter': 'restaurants'
                    # category_filter only has some supported filters
                    # https://www.yelp.com/developers/documentation/v2/all_category_list
                    # if an unsupported category_filter is used, yelp throws an
                    # inavlid_parameter exception
                    # category_filter to restrict to restaurants
                }

                response = client.search_by_bounding_box(49.213687, -123.22197, 49.293288, -123.038464, **params)
                businesses += response.businesses

            restaurants = {}

            restaurant_index = 0
            for index in range(len(businesses)):
                response_rating = businesses[index].rating
                print(businesses[index].name)
                if self.hasMinimumRating(input_rating, response_rating):
                    # can random.choice choose a value where it uses an
                    # index that is skipped at this point?
                    restaurants[restaurant_index] = businesses[index]
                    restaurant_index += 1

            if not restaurants:
                self.name = ''
                self.rating = ''
                self.rating_stars = ''
                self.image_url = ''
                self.url = ''
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