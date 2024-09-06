import pygame as py
from config_variables import *
from car import decodeCommand
from vect2d import vect2d
from node import *

py.font.init()  # Initialize the font module in pygame

class NN:  # Define the NN class

    def __init__(self, config, genome, pos):  # Initialize the NN class with config, genome, and position
        self.input_nodes = []  # Initialize an empty list for input nodes
        self.output_nodes = []  # Initialize an empty list for output nodes
        self.nodes = []  # Initialize an empty list for all nodes
        self.genome = genome  # Store the genome
        self.pos = (int(pos[0]+NODE_RADIUS), int(pos[1]))  # Set the position with an offset for node radius
        input_names = ["Sensor T", "Sensor TR", "Sensor R", "Sensor BR", "Sensor B", "Sensor BL", "Sensor L", "Sensor TL", "Speed"]  # Define names for input nodes
        output_names = ["Accelerate", "Brake", "Turn Left", "Turn Right"]  # Define names for output nodes
        middle_nodes = [n for n in genome.nodes.keys()]  # Get all node keys from the genome
        nodeIdList = []  # Initialize an empty list for node IDs

        # Create input nodes
        h = (INPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING)  # Calculate the height for input nodes
        for i, input in enumerate(config.genome_config.input_keys):  # Iterate over input keys
            n = Node(input, pos[0], pos[1]+int(-h/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), INPUT, [GREEN_PALE, GREEN, DARK_GREEN_PALE, DARK_GREEN], input_names[i], i)  # Create a Node instance
            self.nodes.append(n)  # Add the node to the nodes list
            nodeIdList.append(input)  # Add the node ID to the nodeIdList

        # Create output nodes
        h = (OUTPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING)  # Calculate the height for output nodes
        for i, out in enumerate(config.genome_config.output_keys):  # Iterate over output keys
            n = Node(out+INPUT_NEURONS, pos[0] + 2*(LAYER_SPACING+2*NODE_RADIUS), pos[1]+int(-h/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), OUTPUT, [RED_PALE, RED, DARK_RED_PALE, DARK_RED], output_names[i], i)  # Create a Node instance
            self.nodes.append(n)  # Add the node to the nodes list
            middle_nodes.remove(out)  # Remove the output node from middle_nodes
            nodeIdList.append(out)  # Add the node ID to the nodeIdList

        # Create middle nodes
        h = (len(middle_nodes)-1)*(NODE_RADIUS*2 + NODE_SPACING)  # Calculate the height for middle nodes
        for i, m in enumerate(middle_nodes):  # Iterate over middle nodes
            n = Node(m, self.pos[0] + (LAYER_SPACING+2*NODE_RADIUS), self.pos[1]+int(-h/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), MIDDLE, [BLUE_PALE, DARK_BLUE, BLUE_PALE, DARK_BLUE])  # Create a Node instance
            self.nodes.append(n)  # Add the node to the nodes list
            nodeIdList.append(m)  # Add the node ID to the nodeIdList

        # Create connections
        self.connections = []  # Initialize an empty list for connections
        for c in genome.connections.values():  # Iterate over genome connections
            if c.enabled:  # Check if the connection is enabled
                input, output = c.key  # Get the input and output node IDs
                self.connections.append(Connection(self.nodes[nodeIdList.index(input)], self.nodes[nodeIdList.index(output)], c.weight))  # Create a Connection instance and add it to the connections list

    def draw(self, world):  # Define the draw method to draw the neural network
        for c in self.connections:  # Iterate over connections
            c.drawConnection(world)  # Draw each connection
        for node in self.nodes:  # Iterate over nodes
            node.draw_node(world)  # Draw each node