from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "NOTF2O5ZHMONSZLNLDRAKFS0QWRUANMDKZ41UXIM5NNPFL2E"
foursquare_client_secret = "D4BH3KMFVXMH2QVM34HT53EDI0JAY0HXMFHKDG5UD54YEZRU"


def findARestaurant(mealType,location):
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    location = getGeocodeLocation(location)

    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = "https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v=20130815&ll={}&query={}".format(foursquare_client_id, foursquare_client_secret, str(location[0])+","+str(location[1]), mealType)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])

    #3. Grab the first restaurant
    first_rest = result['response']['venues'][0]
    first_rest_name = first_rest['name']
    venue_id = first_rest['id']
    venue_add = first_rest['location']['formattedAddress'][0]

    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    photo_url = "https://api.foursquare.com/v2/venues/{}/photos?oauth_token=KFXYJDSXSVDVTWAPYESG25B5PQC45KLXGTLN4IXD44A0ZBYF&v=20170815".format(venue_id)
    img_result = json.loads(h.request(photo_url,'GET')[1])
    #5. Grab the first image
    try:
        first_img = img_result['response']['photos']['items'][0]
        first_img_url = first_img['prefix']+'300x300'+first_img['suffix']
    #6. If no image is available, insert default a image url
    except IndexError:
        first_img_url = "No Photo Found"
    #7. Return a dictionary containing the restaurant name, address, and image url  
    restaurant = {"Name: ": first_rest_name, 'Address: ': venue_add, 'Photo: ': first_img_url}

    for item in restaurant:
        print item, restaurant[item] 
    print "\n"



if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")