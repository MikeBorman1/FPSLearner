import numpy as np
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights with random values
        self.weights1 = np.random.randn(input_size, hidden_size)
        self.weights2 = np.random.randn(hidden_size, output_size)
    
    def forward(self, inputs):
        # Propagate inputs through the network
        hidden = np.tanh(np.dot(inputs, self.weights1))
        output = np.tanh(np.dot(hidden, self.weights2))
        return output
    
    def get_weights(self):
        return self.weights1, self.weights2

    @staticmethod
    def from_weights(weights):
        weights1, weights2 = weights
        input_size, hidden_size = weights1.shape
        _, output_size = weights2.shape
        nn = NeuralNetwork(input_size, hidden_size, output_size)
        nn.weights1 = weights1.copy()
        nn.weights2 = weights2.copy()
        return nn

    def crossover(self, other):
        # For each weight, randomly choose whether it comes from this neural network or the other one
        for i in range(self.weights1.shape[0]):
            for j in range(self.weights1.shape[1]):
                if random.random() < 0.5:
                    self.weights1[i, j] = other.weights1[i, j]
        for i in range(self.weights2.shape[0]):
            for j in range(self.weights2.shape[1]):
                if random.random() < 0.5:
                    self.weights2[i, j] = other.weights2[i, j]

    def mutate(self):
        # For each weight, there is a 1% chance that it gets replaced by a random value
        for i in range(self.weights1.shape[0]):
            for j in range(self.weights1.shape[1]):
                if random.random() < 0.01:
                    self.weights1[i, j] = np.random.randn()
        for i in range(self.weights2.shape[0]):
            for j in range(self.weights2.shape[1]):
                if random.random() < 0.01:
                    self.weights2[i, j] = np.random.randn()


