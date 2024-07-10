import math

# Calculates the distance (in km) between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Calculates the time (in minutes) it takes to travel a certain distance at a given speed
def calculate_time(distance, speed):
    return (distance/speed)*60
