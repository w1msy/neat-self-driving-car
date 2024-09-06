import pygame as py
py.font.init()  # Initialize the font module in pygame

#=================== General constants ==================================
FPS = 60  # Frames per second for the game loop
WIN_WIDTH = 1800  # Width of the game window
WIN_HEIGHT = 1000  # Height of the game window
STARTING_POS = (WIN_WIDTH/2, WIN_HEIGHT-100)  # Starting position of the car in the game
SCORE_VEL_MULTIPLIER = 0.00  # Bonus multiplier for faster cars
BAD_GENOME_TRESHOLD = 200  # Threshold to remove a car if it is too far behind

INPUT_NEURONS = 9  # Number of input neurons for the neural network
OUTPUT_NEURONS = 4  # Number of output neurons for the neural network

#=================== Car Specs ==================================
CAR_DBG = False  # Debug flag for car-related debugging
FRICTION  = -0.1  # Friction coefficient for the car's movement
MAX_VEL = 10  # Maximum velocity of the car
MAX_VEL_REDUCTION = 1  # Initial reduction in maximum speed
ACC_STRENGHT = 0.2  # Acceleration strength of the car
BRAKE_STREGHT = 1.5  # Braking strength of the car
TURN_VEL = 2  # Turning velocity of the car
SENSOR_DISTANCE = 200  # Distance that the car's sensors can detect
ACTIVATION_TRESHOLD = 0.5  # Activation threshold for the neural network

#=================== Road Specs ==================================
ROAD_DBG = False  # Debug flag for road-related debugging
MAX_ANGLE = 1  # Maximum angle for road segments
MAX_DEVIATION = 300  # Maximum deviation for road segments
SPACING = 200  # Spacing between road segments
NUM_POINTS  = 15  # Number of points for each road segment
SAFE_SPACE = SPACING + 50  # Buffer space above the screen
ROAD_WIDTH = 200  # Width of the road

#=================== Display and Colors ==================================
NODE_RADIUS = 20  # Radius of nodes in the display
NODE_SPACING = 5  # Spacing between nodes in the display
LAYER_SPACING = 100  # Spacing between layers in the display
CONNECTION_WIDTH = 1  # Width of connections between nodes

WHITE = (255, 255, 255)  # RGB color for white
GRAY = (200, 200, 200)  # RGB color for gray
BLACK = (0, 0, 0)  # RGB color for black
RED = (200, 0, 0)  # RGB color for red
DARK_RED = (100, 0, 0)  # RGB color for dark red
RED_PALE = (250, 200, 200)  # RGB color for pale red
DARK_RED_PALE = (150, 100, 100)  # RGB color for dark pale red
GREEN = (0, 200, 0)  # RGB color for green
DARK_GREEN = (0, 100, 0)  # RGB color for dark green
GREEN_PALE = (200, 250, 200)  # RGB color for pale green
DARK_GREEN_PALE = (100, 150, 100)  # RGB color for dark pale green
BLUE = (0, 0, 255)  # RGB color for blue
BLUE_PALE = (200, 200, 255)  # RGB color for pale blue
DARK_BLUE = (100, 100, 150)  # RGB color for dark blue

NODE_FONT = py.font.SysFont("comicsans", 15)  # Font for node text
STAT_FONT = py.font.SysFont("comicsans", 50)  # Font for statistics text

#=================== Constants for internal use ==================================
GEN = 0  # Generation counter

# Enumerations for car controls
ACC = 0  # Acceleration control
BRAKE = 1  # Brake control
TURN_LEFT = 2  # Turn left control
TURN_RIGHT = 3  # Turn right control

# Enumerations for neural network layers
INPUT = 0  # Input layer
MIDDLE = 1  # Middle layer
OUTPUT = 2  # Output layer