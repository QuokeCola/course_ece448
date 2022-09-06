import numpy as np
import utils
import random

MIN = -1000000


class Agent:

    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne  # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        self.points = 0
        self.s = None
        self.a = None

    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self, model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self, model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        """
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)
        """
        discretize_state = self.discretize(state)
        if self._train:
            # Check whether initialized.
            if self.s is not None and self.a is not None:
                if dead:
                    Reward = -1
                elif points > self.points:  # eat food
                    Reward = 1
                else:
                    Reward = -0.1
                alpha = self.C / (self.C + self.N[self.s][self.a])

                max_Q = self.Q[discretize_state][0]
                for action_next in self.actions:
                    if self.Q[discretize_state][action_next] > max_Q:
                        max_Q = self.Q[discretize_state][action_next]

                self.Q[self.s][self.a] = self.Q[self.s][self.a] + alpha * (
                            Reward + self.gamma * max_Q - self.Q[self.s][self.a])
                self.N[self.s][self.a] += 1
            if dead:
                self.reset()
                return 0
            # update state and points
            self.s = discretize_state
            self.points = points

            self.a = 0
            max_exploration = self.explore_func(self.Q[discretize_state][0], self.N[discretize_state][0])
            for action_next in self.actions:
                if max_exploration < self.explore_func(self.Q[discretize_state][action_next], self.N[discretize_state][action_next]):
                    max_exploration = self.explore_func(self.Q[discretize_state][action_next], self.N[discretize_state][action_next])
                    self.a = action_next
        else:
            max_Q = self.Q[discretize_state][0]
            self.a = 0
            for action_next in self.actions:
                if self.Q[discretize_state][action_next] > max_Q:
                    max_Q = self.Q[discretize_state][action_next]
                    self.a = action_next

        return self.actions[self.a]

    def explore_func(self, Q, N):
        if N < self.Ne:
            return 1
        else:
            return Q

    def discretize(self, state):
        """
        :param state: A list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        """
        food_dir_x = int(((state[0]-state[3]) != 0)*(np.sign(state[0] - state[3])+3)/2)
        food_dir_y = int(((state[1]-state[4]) != 0)*(np.sign(state[1] - state[4])+3)/2)

        adjoining_wall_x = (state[0] == utils.GRID_SIZE) * 1 + \
                           (state[0] == utils.DISPLAY_SIZE - utils.GRID_SIZE * 2) * 2
        adjoining_wall_y = (state[1] == utils.GRID_SIZE) * 1 + \
                           (state[1] == utils.DISPLAY_SIZE - utils.GRID_SIZE * 2) * 2

        adjoining_body_top    = int((state[0], state[1] - utils.GRID_SIZE) in state[2])
        adjoining_body_bottom = int((state[0], state[1] + utils.GRID_SIZE) in state[2])
        adjoining_body_left   = int((state[0] - utils.GRID_SIZE, state[1]) in state[2])
        adjoining_body_right  = int((state[0] + utils.GRID_SIZE, state[1]) in state[2])

        return (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y,
                adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right)
