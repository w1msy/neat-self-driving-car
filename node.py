import pygame as py
from car import decodeCommand
from config_variables import *

class Node:
    def __init__(self, id, x, y, type, color, label = "", index=0):
        # Initialize a Node object with id, x and y coordinates, type, color, label, and index
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.label = label
        self.index = index

    def draw_node(self, world):
        # Draw the node on the given world surface

        colorScheme = self.getNodeColors(world)  # Get the color scheme for the node

        # Draw the outer circle of the node
        py.draw.circle(world.win, colorScheme[0], (self.x, self.y), NODE_RADIUS)
        # Draw the inner circle of the node
        py.draw.circle(world.win, colorScheme[1], (self.x, self.y), NODE_RADIUS-2)

        # Draw the label if the node type is not MIDDLE
        if self.type != MIDDLE:
            text = NODE_FONT.render(self.label, 1, BLACK)  # Render the label text
            # Position the label text based on the node type and draw it on the world surface
            world.win.blit(text, (self.x + (self.type-1) * ((text.get_width() if not self.type else 0) + NODE_RADIUS + 5), self.y - text.get_height()/2))

    def getNodeColors(self, world):
        # Determine the color scheme for the node based on its type and world state

        if self.type == INPUT:
            ratio = world.bestInputs[self.index]  # Get the ratio for input nodes
        elif self.type == OUTPUT:
            ratio = 1 if decodeCommand(world.bestCommands, self.index) else 0  # Get the ratio for output nodes based on decoded command
        else:
            ratio = 0  # Default ratio for other node types

        col = [[0,0,0], [0,0,0]]  # Initialize color arrays
        for i in range(3):
            # Calculate the colors based on the ratio and predefined colors
            col[0][i] = int(ratio * (self.color[1][i]-self.color[3][i]) + self.color[3][i])
            col[1][i] = int(ratio * (self.color[0][i]-self.color[2][i]) + self.color[2][i])
        return col  # Return the calculated color scheme

class Connection:
    def __init__(self, input, output, wt):
        # Initialize a Connection object with input node, output node, and weight
        self.input = input
        self.output = output
        self.wt = wt

    def drawConnection(self, world):
        # Draw the connection line between input and output nodes on the given world surface

        color = GREEN if self.wt >= 0 else RED  # Determine the color based on the weight
        width = int(abs(self.wt * CONNECTION_WIDTH))  # Determine the width based on the weight
        # Draw the line representing the connection
        py.draw.line(world.win, color, (self.input.x + NODE_RADIUS, self.input.y), (self.output.x - NODE_RADIUS, self.output.y), width)