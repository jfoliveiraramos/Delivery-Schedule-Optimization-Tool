from package import *
from utils import *

import numpy as np

# Delivery Schedule
## Represents the delivery schedule problem and stores the values of the parameters
class DeliverySchedule:
    def __init__(self, num_packages, map_size, cost_per_km, cost_per_min, travelling_weight, damage_weight, delay_weight, driver_speed, delivery_delay):
        self.packages = generate_package_stream(num_packages, map_size) # Generate the package stream
        self.num_packages = num_packages # Number of packages
        self.map_size = map_size # Size of the map
        self.cost_per_km = cost_per_km # Cost per km travelled
        self.cost_per_min = cost_per_min # Cost per min of delay on urgent packages
        self.travelling_weight = travelling_weight # Weight of the travelling cost
        self.damage_weight = damage_weight # Weight of the damage cost
        self.delay_weight = delay_weight # Weight of the delay cost
        self.driver_speed = driver_speed # Speed of the driver
        self.delivery_delay = delivery_delay # Time taken to deliver each package

    # Calculates the travelling cost of an ordered list of packages
    def travelling_cost(self, packages_delivery):
        if self.num_packages < 1:
            raise ValueError("No packages to deliver")
        
        if (self.num_packages != len(packages_delivery)):
            raise ValueError("Number of packages does not match")
        
        # Calculate the distance from the start position to the first package
        distance = calculate_distance(0, 0, packages_delivery[0].coordinates_x, packages_delivery[0].coordinates_y)
        
        # Calculate the distance between each package
        for i in range(0, self.num_packages-1):
            package1 = packages_delivery[i]
            package2 = packages_delivery[i+1]
            
            distance += calculate_distance(package1.coordinates_x, package1.coordinates_y, package2.coordinates_x, package2.coordinates_y)

        return self.travelling_weight * self.cost_per_km * distance

    # Calculates the damage cost of an ordered list of packages (only for fragile packages)
    def damage_cost(self, packages_delivery): 
        if self.num_packages < 1:
            raise ValueError("No packages to deliver")
        
        if (self.num_packages != len(packages_delivery)):
            raise ValueError("Number of packages does not match")
        
        # Calculate the distance from the start position to the first package
        travelled_distance = calculate_distance(0, 0, packages_delivery[0].coordinates_x, packages_delivery[0].coordinates_y)
        
        damage_cost = 0

        # Calculate the damage cost of the first package
        if packages_delivery[0].package_type == 'fragile':
            package = packages_delivery[0]
            # Calculate the probability of the package breaking
            p_damage = 1 - (1 - package.breaking_chance) ** travelled_distance
            # Calculate the damage cost of the package mean
            damage_cost = packages_delivery[0].breaking_cost * p_damage

        # Calculate the damage cost of the rest of the packages
        for i in range(1,  self.num_packages):
            package = packages_delivery[i]
            last_package = packages_delivery[i-1]
            # Calculate the total distance to the package delivery point
            travelled_distance += calculate_distance(last_package.coordinates_x, last_package.coordinates_y, package.coordinates_x, package.coordinates_y)

            # If the package is fragile, calculate the damage cost
            if package.package_type == 'fragile':
                # Calculate the probability of the package breaking
                p_damage = 1 - (1 - package.breaking_chance) ** travelled_distance
                # Calculate the damage cost of the package mean
                damage_cost += package.breaking_cost * p_damage
        
        return self.damage_weight * damage_cost

    # Calculates the delay cost of an ordered list of packages (only for urgent packages)
    def delay_cost(self, packages_delivery):
        if self.num_packages < 1:
            raise ValueError("No packages to deliver")
        
        if (self.num_packages != len(packages_delivery)):
            raise ValueError("Number of packages does not match")
        
        # Calculate the distance from the start position to the first package
        travelled_distance = calculate_distance(0, 0, packages_delivery[0].coordinates_x, packages_delivery[0].coordinates_y)

        delay_cost = 0

        # Calculate the delay cost of the first package
        if packages_delivery[0].package_type == 'urgent':
            # Calculate the time to deliver the package
            time = calculate_time(travelled_distance, self.driver_speed) + self.delivery_delay
            # Calculate the delay of the package
            delay = time - packages_delivery[0].delivery_time
            
            if delay > 0: # If the package is delayed, calculate the delay cost
                delay_cost = self.cost_per_min * delay
        
        # Calculate the delay cost of the rest of the packages
        for i in range(1, self.num_packages):
            package = packages_delivery[i]
            last_package = packages_delivery[i-1]
            # Calculate the total distance to the package delivery point
            travelled_distance += calculate_distance(last_package.coordinates_x, last_package.coordinates_y, package.coordinates_x, package.coordinates_y)

            if package.package_type == 'urgent':
                # Calculate the time to deliver the package
                time = calculate_time(travelled_distance, self.driver_speed) + self.delivery_delay * (i + 1)
                # Calculate the delay of the package
                delay = time - package.delivery_time

                if delay > 0: # If the package is delayed, calculate the delay cost
                    delay_cost += self.cost_per_min * delay

        return self.delay_weight * delay_cost

    # Calculates the total cost of an ordered list of packages
    def total_cost(self, packages_delivery):
        if (self.num_packages != len(packages_delivery)):
            raise ValueError("Number of packages does not match")
        
        return self.travelling_cost(packages_delivery) + self.damage_cost(packages_delivery) + self.delay_cost(packages_delivery)

    # String representation of the delivery schedule
    def __str__(self):
        text = f"Delivery Schedule Constraints:\n\n"

        text += f"Number of packages: {self.num_packages}\n"
        text += f"Map size: {self.map_size}\n"
        text += f"Cost per km: {self.cost_per_km}\n"
        text += f"Cost per min: {self.cost_per_min}\n"
        text += f"Travelling weight: {self.travelling_weight}\n"
        text += f"Damage weight: {self.damage_weight}\n"
        text += f"Delay weight: {self.delay_weight}\n"
        text += f"Driver speed: {self.driver_speed}\n"
        text += f"Delivery delay: {self.delivery_delay}\n"        

        return text
    