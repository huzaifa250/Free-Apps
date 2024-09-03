import phonenumbers
import opencage
import folium
from my_phone import number

# first from this phonenumbers extract country name
from phonenumbers import geocoder

pepnumber = phonenumbers.parse(number)
location = geocoder.description_for_number(pepnumber, "en")
print("country Location : ", location)
# find service provider
from phonenumbers import carrier

service_pro = phonenumbers.parse(number)
print("Service Provider : ", carrier.name_for_number(service_pro, "en"))
# install opencage package for location
from opencage.geocoder import OpenCageGeocode

api_key = "b2de386e1e614fc48a061a8803f3c2e9"
geo_coder = OpenCageGeocode(api_key)
query = str(location)
results = geo_coder.geocode(query)
# print("Use lat and lng in google map", results)
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']

print(lat, lng)

my_map = folium.Map(location=[lat, lng])
folium.Marker([lat, lng], popup=location).add_to(my_map)
my_map.save("victim_R.html")
