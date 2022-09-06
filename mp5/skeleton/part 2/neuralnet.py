# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques for the fall 2021 semester
# Modified by Kaiwen Hong for the Spring 2022 semester

"""
This is the main entry point for part 2. You should only modify code
within this file and neuralnet.py -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class NeuralNet(nn.Module):

    def __init__(self, lrate, loss_fn, in_size, out_size):

        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size = out_size
        self.lrate = lrate

        self.network = nn.Sequential(
            nn.Linear(self.in_size, 128),
            nn.ReLU(),
            nn.Linear(128, self.out_size),
            nn.ReLU()
        )
        self.optimizer = optim.Adagrad(self.network.parameters(), self.lrate, weight_decay=0.001)

    def get_parameters(self):
        """ Gets the parameters of your network.

        @return params: a list of tensors containing all parameters of the network
        """
        return self.network.parameters()

    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """
        return self.network(x)

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) at this timestep as a float
        """
        self.optimizer.zero_grad()
        # forward
        y_new = self.forward(x)

        # loss
        loss = self.loss_fn(y_new, y)

        # backward pass, update weight
        loss.backward()
        self.optimizer.step()

        return loss.item()


def fit(train_set, train_labels, dev_set, n_iter, batch_size=100):
    """ Fit a neural net. Use the full batch size.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param n_iter: an int, the number of epoches of training
    @param batch_size: size of each batch to train on. (default 100)

    NOTE: This method _must_ work for arbitrary M and N.

    @return losses: array of total loss at the beginning and after each iteration.
            Ensure that len(losses) == n_iter.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """

    N = train_set.shape[0]

    lrate = 0.001
    loss_fn = torch.nn.CrossEntropyLoss()
    in_size = train_set.shape[1]
    out_size = 2

    net = NeuralNet(lrate, loss_fn, in_size, out_size)
    losses = []

    train_set_ = (train_set - train_set.mean())/train_set.std()
    # Epoches
    batches = range(n_iter*100)
    for i in range(n_iter*100):
        # Random get batch data

        rnd_idxes = np.random.permutation(N)
        train_set_batch = train_set_[rnd_idxes[:batch_size]]
        train_label_batch = train_labels[rnd_idxes[:batch_size]]

        loss = net.step(train_set_batch, train_label_batch)
        losses.append(loss)

    plt.plot(batches, losses)
    plt.xlabel("Epoches Number")
    plt.ylabel("Losses")
    plt.title("Epoches vs. Losses")
    plt.show()
    # develop
    y_res = np.argmax(net(dev_set).detach().numpy(), axis=1)

    return losses, y_res, net
