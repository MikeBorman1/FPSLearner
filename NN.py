import numpy as np
import random

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, hidden2_size, output_size):
        # Initialize weights with random values
        self.weights1 =  np.random.randn(input_size, hidden_size)
        self.weights2 =  np.random.randn(hidden_size, hidden2_size)
        self.weights3 =  np.random.randn(hidden2_size, output_size)
    
    def forward(self, inputs):
        # Propagate inputs through the network
        
        
        hidden = np.tanh(np.dot(inputs, self.weights1))
        hidden2 = np.tanh(np.dot(hidden, self.weights2))
        output = np.tanh(np.dot(hidden2, self.weights3))
        #print(f"Inputs: {inputs}, Hidden: {hidden}, Output: {output}")
        return output
    
    def get_weights(self):
        return self.weights1, self.weights2, self.weights3

    @staticmethod
    def from_weights(weights):
        weights1, weights2, weights3 = weights
        input_size, hidden_size = weights1.shape
        hidden2_size, _ = weights2.shape
        _, output_size = weights3.shape
        nn = NeuralNetwork(input_size, hidden_size, hidden2_size, output_size)
        nn.weights1 = weights1.copy()
        nn.weights2 = weights2.copy()
        nn.weights3 = weights3.copy()
        return nn

    def crossover(self, other):
        # Determine a random crossover point for each weight matrix
        crossover_point1 = random.randint(0, self.weights1.size)
        crossover_point2 = random.randint(0, self.weights2.size)
        crossover_point3 = random.randint(0, self.weights3.size)

        # Flatten the weight matrices for easy manipulation
        flat_weights1_self = self.weights1.flatten()
        flat_weights2_self = self.weights2.flatten()
        flat_weights3_self = self.weights3.flatten()

        flat_weights1_other = other.weights1.flatten()
        flat_weights2_other = other.weights2.flatten()
        flat_weights3_other = other.weights3.flatten()

        # Perform the crossover
        new_weights1 = np.concatenate((flat_weights1_self[:crossover_point1], flat_weights1_other[crossover_point1:]))
        new_weights2 = np.concatenate((flat_weights2_self[:crossover_point2], flat_weights2_other[crossover_point2:]))
        new_weights3 = np.concatenate((flat_weights3_self[:crossover_point3], flat_weights3_other[crossover_point3:]))

        # Reshape the new weight matrices to their original shape
        new_weights1 = new_weights1.reshape(self.weights1.shape)
        new_weights2 = new_weights2.reshape(self.weights2.shape)
        new_weights3 = new_weights3.reshape(self.weights3.shape)

        # Assign the new weight matrices to this agent
        self.weights1 = new_weights1
        self.weights2 = new_weights2
        self.weights3 = new_weights3



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
        for i in range(self.weights3.shape[0]):
            for j in range(self.weights3.shape[1]):
                if random.random() < 0.01:
                    self.weights3[i, j] = np.random.randn()


