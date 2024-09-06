from config_variables import *
import pygame as py
import os
from math import *
from random import random
from road import *
import numpy as np
from vect2d import vect2d


class Car:
    x = 0  # Initialize x coordinate of the car
    y = 0  # Initialize y coordinate of the car

    def __init__(self, x, y, turn):
        self.x = x  # Set the x coordinate of the car
        self.y = y  # Set the y coordinate of the car
        self.rot = turn  # Set the initial rotation of the car
        self.rot = 0  # Reset the rotation to 0
        self.vel = MAX_VEL / 2  # Set the initial velocity of the car to half of MAX_VEL
        self.acc = 0  # Initialize acceleration to 0
        self.initImgs()  # Initialize car images
        self.commands = [0, 0, 0, 0]  # Initialize command list with zeros

    def initImgs(self):
        img_names = ["yellow_car.png", "red_car.png", "blu_car.png", "green_car.png"]  # List of car image filenames
        name = img_names[floor(random() * len(img_names)) % len(img_names)]  # Pick one of these images at random

        # Load and transform the car image
        self.img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", name)).convert_alpha(), (120, 69)), -90)
        # Load and transform the brake image
        self.brake_img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", "brakes.png")).convert_alpha(), (120, 69)), -90)

    def detectCollision(self, road):
        mask = py.mask.from_surface(self.img)  # Get the mask of the car image
        (width, height) = mask.get_size()  # Get the size of the mask
        for v in [road.pointsLeft, road.pointsRight]:  # Iterate over left and right road points
            for p in v:
                x = p.x - self.x + width / 2  # Calculate x coordinate relative to the car
                y = p.y - self.y + height / 2  # Calculate y coordinate relative to the car
                try:
                    if mask.get_at((int(x), int(y))):  # Check if the mask collides at the given point
                        return True  # Collision detected
                except IndexError as error:
                    continue  # Ignore index errors and continue
        return False  # No collision detected

    def getInputs(self, world, road):  # Get sensor inputs
        sensors = [SENSOR_DISTANCE] * 8  # Initialize sensors with SENSOR_DISTANCE
        sensorsEquations = getSensorEquations(self, world)  # Get sensor equations

        for v in [road.pointsLeft, road.pointsRight]:  # Iterate over left and right road points
            i = road.bottomPointIndex  # Start from the bottom point index
            while v[i].y > self.y - SENSOR_DISTANCE:  # Check points within SENSOR_DISTANCE
                next_index = getPoint(i + 1, NUM_POINTS * road.num_ctrl_points)  # Get the next point index
                getDistance(world, self, sensors, sensorsEquations, v[i], v[next_index])  # Calculate distance to sensors
                i = next_index  # Move to the next point

        if CAR_DBG:  # If debugging is enabled
            for k, s in enumerate(sensors):
                omega = radians(self.rot + 45 * k)  # Calculate sensor angle
                dx = s * sin(omega)  # Calculate x displacement
                dy = -s * cos(omega)  # Calculate y displacement
                if s < SENSOR_DISTANCE:  # If sensor detects an object
                    py.draw.circle(world.win, RED, world.getScreenCoords(self.x + dx, self.y + dy), 6)  # Draw sensor intersection

        for s in range(len(sensors)):  # Normalize sensor values
            sensors[s] = 1 - sensors[s] / SENSOR_DISTANCE  # Convert to value between 0 and 1

        return sensors  # Return sensor values

    def move(self, road, t):
        self.acc = FRICTION  # Set initial acceleration to friction

        if decodeCommand(self.commands, ACC):  # If acceleration command is active
            self.acc = ACC_STRENGHT  # Set acceleration strength
        if decodeCommand(self.commands, BRAKE):  # If brake command is active
            self.acc = -BRAKE_STREGHT  # Set brake strength
        if decodeCommand(self.commands, TURN_LEFT):  # If turn left command is active
            self.rot -= TURN_VEL  # Decrease rotation
        if decodeCommand(self.commands, TURN_RIGHT):  # If turn right command is active
            self.rot += TURN_VEL  # Increase rotation

        timeBuffer = 500  # Time buffer for velocity reduction
        if MAX_VEL_REDUCTION == 1 or t >= timeBuffer:  # Check if velocity reduction is needed
            max_vel_local = MAX_VEL  # Set maximum velocity
        else:
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION) * (t / timeBuffer)  # Calculate velocity reduction ratio
            max_vel_local = MAX_VEL * ratio  # Apply velocity reduction

        self.vel += self.acc  # Update velocity with acceleration
        if self.vel > max_vel_local:  # Cap velocity to maximum velocity
            self.vel = max_vel_local
        if self.vel < 0:  # Ensure velocity is not negative
            self.vel = 0
        self.x = self.x + self.vel * sin(radians(self.rot))  # Update x coordinate based on velocity and rotation
        self.y = self.y - self.vel * cos(radians(self.rot))  # Update y coordinate based on velocity and rotation

        return (self.x, self.y)  # Return updated coordinates

    def draw(self, world):
        screen_position = world.getScreenCoords(self.x, self.y)  # Get screen coordinates of the car
        rotated_img = py.transform.rotate(self.img, -self.rot)  # Rotate the car image based on rotation
        new_rect = rotated_img.get_rect(center=screen_position)  # Get the new rectangle for the rotated image
        world.win.blit(rotated_img, new_rect.topleft)  # Draw the rotated car image on the screen

        if decodeCommand(self.commands, BRAKE):  # If brake command is active
            rotated_img = py.transform.rotate(self.brake_img, -self.rot)  # Rotate the brake image based on rotation
            new_rect = rotated_img.get_rect(center=screen_position)  # Get the new rectangle for the rotated brake image
            world.win.blit(rotated_img, new_rect.topleft)  # Draw the rotated brake image on the screen

    # ======================== LOCAL FUNCTIONS ==========================

def getSensorEquations(self, world):  # Returns the equations of the sensor lines
    eq = []
    for i in range(4):
        omega = radians(self.rot + 45 * i)  # Calculate sensor angle
        dx = SENSOR_DISTANCE * sin(omega)  # Calculate x displacement
        dy = -SENSOR_DISTANCE * cos(omega)  # Calculate y displacement

        if CAR_DBG:  # If debugging is enabled
            py.draw.lines(world.win, GREEN, False, [world.getScreenCoords(self.x + dx, self.y + dy), world.getScreenCoords(self.x - dx, self.y - dy)], 2)  # Draw sensor lines

        coef = getSegmentEquation(self, vect2d(x=self.x + dx, y=self.y + dy))  # Get the equation of the sensor line
        eq.append(coef)  # Append the equation to the list
    return eq  # Return the list of equations

def getSegmentEquation(p, q):  # Returns the equation of the line segment between two points
    a = p.y - q.y  # Calculate coefficient a
    b = q.x - p.x  # Calculate coefficient b
    c = p.x * q.y - q.x * p.y  # Calculate coefficient c

    return (a, b, c)  # Return the coefficients as a tuple

def getDistance(world, car, sensors, sensorsEquations, p, q):  # Calculate the distance to the sensors
    (a2, b2, c2) = getSegmentEquation(p, q)  # Get the equation of the segment

    for i, (a1, b1, c1) in enumerate(sensorsEquations):  # Iterate over sensor equations
        if a1 != a2 or b1 != b2:  # Check if lines are not coinciding
            d = b1 * a2 - a1 * b2  # Calculate determinant
            if d == 0:
                continue  # Skip if determinant is zero
            y = (a1 * c2 - c1 * a2) / d  # Calculate y coordinate of intersection
            x = (c1 * b2 - b1 * c2) / d  # Calculate x coordinate of intersection
            if (y - p.y) * (y - q.y) > 0 or (x - p.x) * (x - q.x) > 0:  # Check if intersection is within segment
                continue  # Skip if not within segment
        else:  # Coinciding lines
            (x, y) = (abs(p.x - q.x), abs(p.y - q.y))  # Calculate distance between points

        dist = ((car.x - x) ** 2 + (car.y - y) ** 2) ** 0.5  # Calculate distance to car

        omega = car.rot + 45 * i  # Calculate sensor angle
        alpha = 90 - degrees(atan2(car.y - y, x - car.x))  # Calculate angle from vertical
        if cos(alpha) * cos(omega) * 100 + sin(alpha) * sin(omega) * 100 > 0:  # Check if intersection is in the right direction
            index = i  # Set sensor index
        else:
            index = i + 4  # Set opposite sensor index

        if dist < sensors[index]:  # Update sensor distance if closer
            sensors[index] = dist

def decodeCommand(commands, type):  # Decode the command based on activation threshold
    if commands[type] > ACTIVATION_TRESHOLD:  # Check if command is above activation threshold
        if type == ACC and commands[type] > commands[BRAKE]:  # Check if acceleration command is stronger than brake
            return True
        elif type == BRAKE and commands[type] > commands[ACC]:  # Check if brake command is stronger than acceleration
            return True
        elif type == TURN_LEFT and commands[type] > commands[TURN_RIGHT]:  # Check if turn left command is stronger than turn right
            return True
        elif type == TURN_RIGHT and commands[type] > commands[TURN_LEFT]:  # Check if turn right command is stronger than turn left
            return True
    return False  # Return False if no command is active