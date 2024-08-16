### TEST CODE BS

class Point:
    def __init__(self, value=0, attributes=None):
        self.value = value
        self.attributes = attributes if attributes is not None else {}

class World:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.grid = {}

    def set_point(self, coordinates, value, attributes=None):
        if len(coordinates) != self.dimensions:
            raise ValueError("Number of coordinates must match the number of dimensions.")
        self.grid[coordinates] = Point(value, attributes)

    def get_point(self, coordinates):
        return self.grid.get(coordinates)

    def interact(self, coord1, coord2):
        point1 = self.get_point(coord1)
        point2 = self.get_point(coord2)

        # Define interaction rules based on attributes
        if point1 and point2:
            # Example interaction: combine values based on some rule
            combined_value = point1.value + point2.value
            # Example attribute interaction
            if "type" in point1.attributes and "type" in point2.attributes:
                if point1.attributes["type"] == "water" and point2.attributes["type"] == "fire":
                    combined_value /= 2  # Water extinguishes fire
            return combined_value
        return None
