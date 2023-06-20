import numpy as np

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