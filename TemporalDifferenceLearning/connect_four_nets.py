import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable


class Connect4Network(torch.nn.Module):
    def __init__(self):
        super(Connect4Network, self).__init__()

        self.conv1 = torch.nn.Conv2d(1, 8, kernel_size=3, stride=1, padding=1)
        self.pool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = torch.nn.Linear(72, 32)
        self.fc2 = torch.nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = x.view(-1, 72)
        x = self.fc1(x)
        x = self.fc2(x)

        return x

    def create_loss_and_optimizer(self, learning_rate=0.001):
        # Loss function
        loss = torch.nn.MSELoss()

        # Optimizer
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)

        return loss, optimizer

    def fit(self, X, y, num_epochs=20, learning_rate=0.001, verbose=False):
        print("Training network...")
        criterion, optimizer = self.create_loss_and_optimizer(learning_rate=learning_rate)

        for epoch in range(num_epochs):
            X_var = Variable(X)
            y_var = Variable(y)

            # Forward + Backward + Optimize
            optimizer.zero_grad()  # zero the gradient buffer
            outputs = self(X_var)
            loss = criterion(outputs, y_var)
            loss.backward()
            print("Iteration {}: {} loss".format(epoch + 1, loss.data))
            optimizer.step()

    def predict(self, X):
        X_var = Variable(X, requires_grad=False)
        output = self(X_var)
        return output
