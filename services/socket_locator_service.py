from math import radians, cos, sin, asin, sqrt
from db_context.models import TG_location as Socket

MAX_DISTANCE_KM = 200

async def find_closest_socket(user_lat, user_lon):
    # Rough degree difference for 200 km (~1.8 degrees latitude)
    degree_radius = 2.0  

    min_lat = user_lat - degree_radius
    max_lat = user_lat + degree_radius
    min_lon = user_lon - degree_radius
    max_lon = user_lon + degree_radius

    # First filter by simple bounding box (fast)
    nearby_sockets = await Socket.filter(
        latitude__gte=min_lat, latitude__lte=max_lat,
        longitude__gte=min_lon, longitude__lte=max_lon
    )

    closest_socket = None
    min_distance = float('inf')

    for socket in nearby_sockets:
        dist = haversine(user_lon, user_lat, socket.longitude, socket.latitude)
        if dist <= MAX_DISTANCE_KM and dist < min_distance:
            min_distance = dist
            closest_socket = socket

    return closest_socket

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius in km
    return c * r
