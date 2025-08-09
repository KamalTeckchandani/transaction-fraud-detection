from faker import Faker
import random
from geopy.geocoders import Nominatim
import time

fake = Faker()
geolocator = Nominatim(user_agent="fraud_detection_system")

# Cache for storing previously looked-up lat/lon by location name
geocode_cache = {}

def geocode_location(location_name):
    if location_name in geocode_cache:
        return geocode_cache[location_name]
    try:
        loc = geolocator.geocode(location_name)
        if loc:
            lat_lon = (loc.latitude, loc.longitude)
            geocode_cache[location_name] = lat_lon
            # Sleep to respect Nominatim's rate limit (~1 request per second)
            time.sleep(1)
            return lat_lon
    except Exception as e:
        print(f"Geocoding error for {location_name}: {e}")
    return (None, None)

def generate_transaction():
    location = fake.country()
    lat, lon = geocode_location(location)
    
    return {
        "transaction_id": fake.uuid4(),
        "user_id": fake.uuid4(),
        "amount": random.randint(10, 10000),
        "timestamp": fake.date_time_this_year(),
        "ip_address": fake.ipv4(),
        "location": location,
        "lat": lat,
        "lon": lon,
        "device_id": fake.uuid4(),
    }

if __name__ == "__main__":
    for _ in range(5):
        print(generate_transaction())
