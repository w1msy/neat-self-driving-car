import pygame as py

class World:

    initialPos = (0,0)  # Class variable to store the initial position of the world
    bestCarPos = (0,0)  # Class variable to store the best car position

    def __init__(self, starting_pos, world_width, world_height):
        self.initialPos = starting_pos  # Initialize the starting position of the world
        self.bestCarPos = (0, 0)  # Initialize the best car position to (0, 0)
        self.win  = py.display.set_mode((world_width, world_height))  # Create a window with the given width and height
        self.win_width = world_width  # Store the width of the window
        self.win_height = world_height  # Store the height of the window
        self.score = 0  # Initialize the score to 0
        self.bestGenome = None  # Initialize the best genome to None

    def updateBestCarPos(self, pos):
        self.bestCarPos = pos  # Update the best car position with the given position

    def getScreenCoords(self, x, y):
        # Calculate and return the screen coordinates based on the initial position and best car position
        return (int(x + self.initialPos[0] - self.bestCarPos[0]), int(y + self.initialPos[1] - self.bestCarPos[1]))

    def getBestCarPos(self):
        return self.bestCarPos  # Return the current best car position

    def updateScore(self, new_score):
        self.score = new_score  # Update the score with the new score

    def getScore(self):
        return self.score  # Return the current score