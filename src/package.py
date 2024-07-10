import random

# Package
## Represents a package with an ID, type, coordinates, and additional attributes
class Package:
    def __init__(self, id, package_type, coordinates):
        self.id = id # Package ID
        self.package_type = package_type # Package type

        # Coordinates of the package
        self.coordinates_x = coordinates[0] 
        self.coordinates_y = coordinates[1]
        
        if package_type == 'fragile': # If the package is fragile
            self.breaking_chance = random.uniform(0.0001, 0.01) # 0.01-1% chance of breaking per km

            self.breaking_cost = random.uniform(3, 10) # Extra cost in case of breaking

        elif package_type == 'urgent': # If the package is urgent
            self.delivery_time = random.uniform(100, 240) # Delivery time in minutes (100 minutes to 4 hours)       
            
    # String representation of the package
    def __str__(self):
        return f"{self.id}"
    
    # Representation of the package
    def __repr__(self):
        return self.__str__()
    
    # Equality operator
    def __eq__(self, other):
        return self.id == other.id

    # Display the package information
    def display(self):
        if self.package_type == 'fragile':
            print(f"Fragile package {self.id} at ({round(self.coordinates_x,2)},{round(self.coordinates_y,2)}) with breaking chance {round(self.breaking_chance * 100,2)}% and cost {round(self.breaking_cost)}")
        elif self.package_type == 'urgent':
            print(f"Urgent package {self.id} at ({round(self.coordinates_x,2)},{round(self.coordinates_y,2)}) with delivery time at {self.delivery_time // 60}h{round(self.delivery_time % 60)}")
        else:
            print(f"Normal package {self.id} at ({round(self.coordinates_x,2)},{round(self.coordinates_y,2)})")

# Generates a package stream with a given number of packages and map size
def generate_package_stream(num_packages, map_size):
    package_types = ['normal', 'fragile', 'urgent']
    package_stream = [Package(i, random.choice(package_types), (random.uniform(0, map_size), random.uniform(0, map_size))) 
                              for i in range(num_packages)]
    return package_stream
