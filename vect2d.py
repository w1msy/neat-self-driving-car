class vect2d:
    # Constructor method to initialize the vector with x, y coordinates and an angle
    def __init__(self, x=-1, y=-1, angle=0):
        self.x = x  # Initialize x coordinate
        self.y = y  # Initialize y coordinate
        self.angle = angle  # Initialize angle

    # Method to set new coordinates for the vector
    def co(self, x, y):
        self.x = x  # Update x coordinate
        self.y = y  # Update y coordinate

    # Method to get the current coordinates of the vector
    def getCo(self):
        return (self.x, self.y)  # Return a tuple containing the x and y coordinates