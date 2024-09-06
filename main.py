import pygame as py
import neat
import time
import os
import random
from car import Car
from road import Road
from world import World
from NNdraw import NN
from config_variables import *
py.font.init()  # Initialize the font module in pygame

# Create a background surface with the specified window dimensions
bg = py.Surface((WIN_WIDTH, WIN_HEIGHT))
bg.fill(GRAY)  # Fill the background with the color gray

# Function to draw the game window
def draw_win(cars, road, world, GEN):  # x and y are the coordinates of the best machine
    road.draw(world)  # Draw the road on the world
    for car in cars:  # Iterate over each car
        car.draw(world)  # Draw the car on the world

    # Render the score of the best car
    text = STAT_FONT.render("Best Car Score: "+str(int(world.getScore())), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 10))  # Display the score on the window
    # Render the current generation number
    text = STAT_FONT.render("Gen: "+str(GEN), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 50))  # Display the generation number on the window

    world.bestNN.draw(world)  # Draw the best neural network on the world

    py.display.update()  # Update the display
    world.win.blit(bg, (0,0))  # Blit the background immediately after the update

# Main function to run the simulation
def main(genomes = [], config = []):
    global GEN  # Use the global variable GEN
    GEN += 1  # Increment the generation number

    nets = []  # List to store neural networks
    ge = []  # List to store genomes
    cars = []  # List to store cars
    t = 0  # Initialize time counter

    # Create a new world with the starting position and window dimensions
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(bg, (0,0))  # Blit the background on the window

    NNs = []  # List to store neural networks

    # Iterate over each genome
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)  # Create a neural network from the genome
        nets.append(net)  # Add the neural network to the list
        cars.append(Car(0, 0, 0))  # Add a new car to the list
        g.fitness = 0  # Initialize the fitness of the genome
        ge.append(g)  # Add the genome to the list
        NNs.append(NN(config, g, (90, 210)))  # Add a new neural network to the list

    road = Road(world)  # Create a new road
    clock = py.time.Clock()  # Create a clock object to control the frame rate

    run = True  # Set the run flag to True
    while run:
        t += 1  # Increment the time counter
        clock.tick(FPS)  # Control the frame rate
        world.updateScore(0)  # Update the score of the world

        # Handle events
        for event in py.event.get():
            if event.type == py.QUIT:  # If the quit event is triggered
                run = False  # Set the run flag to False
                py.quit()  # Quit pygame
                quit()  # Quit the program

        (xb, yb) = (0,0)  # Initialize the coordinates of the best car
        i = 0  # Initialize the index
        while(i < len(cars)):
            car = cars[i]  # Get the current car

            input = car.getInputs(world, road)  # Get the inputs for the car
            input.append(car.vel/MAX_VEL)  # Append the normalized velocity to the inputs
            car.commands = nets[i].activate(tuple(input))  # Activate the neural network with the inputs

            y_old = car.y  # Store the old y-coordinate of the car
            (x, y) = car.move(road,t)  # Move the car and get the new coordinates
            # If the car collides or meets certain conditions, remove it
            if t>10 and (car.detectCollision(road) or y > world.getBestCarPos()[1] + BAD_GENOME_TRESHOLD or y>y_old or car.vel < 0.1):
                ge[i].fitness -= 1  # Decrease the fitness of the genome
                cars.pop(i)  # Remove the car from the list
                nets.pop(i)  # Remove the neural network from the list
                ge.pop(i)  # Remove the genome from the list
                NNs.pop(i)  # Remove the neural network from the list
            else:
                # Update the fitness of the genome
                ge[i].fitness += -(y - y_old)/100 + car.vel*SCORE_VEL_MULTIPLIER
                if(ge[i].fitness > world.getScore()):  # If the fitness is greater than the current score
                    world.updateScore(ge[i].fitness)  # Update the score of the world
                    world.bestNN = NNs[i]  # Update the best neural network
                    world.bestInputs = input  # Update the best inputs
                    world.bestCommands = car.commands  # Update the best commands
                i += 1  # Increment the index

            if y < yb:  # If the y-coordinate is less than the best y-coordinate
                (xb, yb) = (x, y)  # Update the best coordinates

        if len(cars) == 0:  # If there are no cars left
            run = False  # Set the run flag to False
            break  # Break the loop

        world.updateBestCarPos((xb, yb))  # Update the best car position
        road.update(world)  # Update the road
        draw_win(cars, road, world, GEN)  # Draw the game window

# NEAT function to run the simulation
def run(config_path):
    # Load the NEAT configuration
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)  # Create a population with the configuration

    p.add_reporter(neat.StdOutReporter(True))  # Add a reporter to show progress in the terminal
    stats = neat.StatisticsReporter()  # Create a statistics reporter
    p.add_reporter(stats)  # Add the statistics reporter to the population

    winner = p.run(main, 10000)  # Run the NEAT algorithm for 10000 generations

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)  # Get the directory of the current file
    config_path = os.path.join(local_dir, "config_file.txt")  # Get the path to the configuration file
    run(config_path)  # Run the NEAT algorithm with the configuration file