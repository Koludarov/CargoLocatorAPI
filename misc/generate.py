import random
import string

from geopy.distance import geodesic

from models.locations import Location


def generate_unique_id() -> str:
    number = random.randint(1000, 9999)
    letter = random.choice(string.ascii_uppercase)
    unique_id = str(number) + letter
    return unique_id


async def calculate_distance(location1: Location, location2: Location) -> float:
    point1 = (location1.latitude, location1.longitude)
    point2 = (location2.latitude, location2.longitude)
    distance = round(geodesic(point1, point2).miles, 1)
    return distance
