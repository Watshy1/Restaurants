from flask import Flask, request
import json
import requests
import overpy
import math

app = Flask(__name__)
app.url_map.strict_slashes = False

api = overpy.Overpass()

@app.route("/")
def Home():
    return json.dumps({"restaurants": "/restaurants/"}, sort_keys = True, indent = 4)


@app.route("/restaurants")
def Restaurants():

    def round_decimals_up(number:float, decimals:int):
        factor = 10 ** decimals
        return math.ceil(number * factor) / factor


    restaurantName = request.args.get('q')

    lat = request.args.get('lat')
    lon = request.args.get('lon')

    test = 0
    test2 = 0

    if (lat):
        floatLat = float(lat)
        n = str(floatLat).split(".")[-1]

        for i in n:
            test += 1

    if (lon):
        floatLon = float(lon)
        a = str(floatLon).split(".")[-1]

        for z in a:
            test2 += 1

    city = 'Paris'

    if (restaurantName):

        response = requests.post(
            "https://lz4.overpass-api.de/api/interpreter",
            f"""[out:json];area[name="{city}"];node["amenity"="restaurant"]["name"~"{restaurantName}"](area);out meta;""".encode("UTF-8")
        ).json()

        return response

    elif (lat and lon):

        response = requests.post(
            "https://lz4.overpass-api.de/api/interpreter",
            f"""[out:json];area[name="{city}"];node({lon}, {lat}, {round_decimals_up(floatLon, test2)}, {round_decimals_up(floatLat, test)})["amenity"="restaurant"](area);out meta;""".encode("UTF-8")
        ).json()

        return response

    else:
        
        response = requests.post(
            "https://lz4.overpass-api.de/api/interpreter",
            f"""[out:json];area[name="{city}"];node["amenity"="restaurant"](area);out meta;""".encode("UTF-8")
        ).json()

        return response