import random
import pygame
import NN
import numpy as np
import math

class Agent:
    def __init__(self, x, y, width, height, opponent=None):
        self.x = x
        self.y = y
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.radius = 30
        self.speed = 0.05
        self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]  # direction of movement
        self.rotation = random.uniform(0, 2*math.pi)  # direction agent is facing
        self.ticks = 0  # Add a ticks attribute
        self.front = self.update_front()
        self.projectiles = []
        self.opponent = opponent
        self.nn = NN.NeuralNetwork(8, 16, 4)
        self.agentHits =0
        self.timesHit = 0

    def move(self):
        
        # Change direction and rotation every 1000 ticks
        if self.ticks % 1000 == 0:

            ## Pass through to the NN
            self.update_front()
            state = self.get_state()
            action = self.nn.forward(state)
            self.interpret_output(action)

        self.ticks += 1  # Increment ticks

        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]
        self.update_front()
        
        # Add a simple boundary rule so agents stay within the screen
        if self.x <= 0 or self.x >= self.WINDOW_WIDTH:
            self.direction[0] *= -1
        if self.y <= 0 or self.y >= self.WINDOW_HEIGHT:
            self.direction[1] *= -1

    def update_front(self):
           self.front = [(self.radius+20) *  math.cos(self.rotation) + self.x, (self.radius+20) * math.sin(self.rotation) + self.y ]

    def get_state(self):
        # Fetch the current state of the agent
        return np.array([self.x, self.y, self.direction[0], self.direction[1], self.front[0], self.front[1], self.opponent.x, self.opponent.y])
    
    def interpret_output(self, output):
        # Use the neural network's output to modify the agent's state
        self.direction = [output[0], output[1]]
        self.rotation = output[3]
        self.update_front()
        if output[2] > 0.5:
            self.shoot()
    
    def set_opponent(self, opponent):
        self.opponent = opponent


    def shoot(self):
        
        self.projectiles.append(Projectile(self.x, self.y, self.front))

    def delProjectile(self,projectile):
        try:
            self.projectiles.remove(projectile)
        except:
            pass

    def hit(self):
        self.agentHits += 1
        self.opponent.timesHit += 1

   

    def copy(self):
        # Create a new agent with the same weights
        new_agent = Agent(self.x, self.y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        new_agent.nn = NN.NeuralNetwork.from_weights(self.nn.get_weights())
        return new_agent
    
    def crossover(self, other):
        # Create a new agent with weights that are a combination of this agent's and the other agent's weights
        new_agent = self.copy()
        new_agent.nn.crossover(other.nn)
        return new_agent

    def mutate(self):
        # Randomly modify the weights
        self.nn.mutate()


class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 1  # projectiles move faster than agents
        self.direction = [direction[0]-x, direction[1] - y]
        
        magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
        if magnitude != 0:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude

    def move(self):
        
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), 5)


    

