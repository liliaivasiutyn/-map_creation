from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import pandas
import geopy
import folium
geolocator = geopy.geocoders.Nominatim(
        user_agent="specify_your_app_name_here", timeout=1)
geocode = geopy.extra.rate_limiter.RateLimiter(
        geolocator.geocode, min_delay_seconds=0.01)


def read_file(year):
    """
    (str)-> list
    Read file and and return list of lists 
    which name of the film and its location, starred in given year
    """
    data = pandas.read_csv(
        "locations.csv", error_bad_lines=False, warn_bad_lines=False)
    movie = data['movie']
    years = data['year']
    locations = data['location']
    ans = []
    for m, y, l in zip(movie, years, locations):
        try:
            if year in y:
                ans.append(list((m, l)))
        except:
            pass
    return ans


def find_cordinates(lst):
    """
    (lst)->(lst)
    Find cordinates of locations and return list
    of lists with name of film and its location
    """
    ans = []
    counter = 0
    for l in lst:
        try:
            location = geolocator.geocode(l[1])
            ans.append([l[0], list((location.latitude, location.longitude))])
            counter += 1
        except:
            pass
        if counter == 300:
            break
    return ans


def keys(lst):
    """
    (list)->(str)
    Return the last element of the list
    """
    return lst[-1]


def ten_near_locations(loc, lst):
    """
    (list, list)->(list)
    Return ten the nearest locations to the given cordinates
    """
    for l in lst:
        dis = distance.distance(loc, l[1]).km
        l.append(dis)
    lst = sorted(lst, key=keys)
    return lst[:10]


def map_creation():
    year = input('Please enter a year you would like to have a map for: ')
    cordinates = input('Please enter your location (format: lat, long): ')
    cor = cordinates.replace(' ', '').split(',')
    print('Map is generating...')
    print('Please wait...')
    res_cor = list(map(float, cor))
    res = ten_near_locations(res_cor, find_cordinates(read_file(year)))
    user_map = folium.Map(location=res_cor, zoom_start=4)
    films_layer = folium.FeatureGroup("Movie locations")
    for l in res:
        films_layer.add_child(folium.Marker(
            location=l[1], popup=l[0], icon=folium.Icon()))

    new_layer = folium.FeatureGroup("User cordinates")
    new_layer.add_child(folium.Marker(location=res_cor,
                                      popup="Your cordinates",
                                      icon=folium.Icon(color='green')))

    user_map.add_child(films_layer)
    user_map.add_child(new_layer)
    user_map.add_child(folium.LayerControl())
    user_map.save("Map.html")

    print("Finished. Please have look at the map Map.html")


if __name__ == "__main__":
    map_creation()
