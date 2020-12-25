"""example.py: Use a maze and solve it with classic wall-following
   algorithm.

   The RL versions should be faster
"""

__author__ = "Pablo Alvarado"
__copyright__ = "Copyright 2020, Pablo Alvarado"
__license__ = "BSD 3-Clause License (Revised)"

import time
import dispatcher
import env
import agent
from QNetwork import Network
from math import exp
import math
import numpy as np
from scipy.spatial.distance import euclidean


import warnings
warnings.filterwarnings("ignore")


OBSERVATION_SPACE = 6

class TrainSolver:

    def __init__(self, dispatch):
        self.dispatch = dispatch
        self.reset()
        self.solver = Network(OBSERVATION_SPACE, len(self.actions) - 1)
        self.state_last = agent.AgentState()
        self.state_last_last = agent.AgentState()
        self.init()
        self.solver.load_model()
        self.lastRenderingTime = time.perf_counter()
        self.episodes = 0
        self.action_memory = []
        self.state_memory = []
        self.reward_memory = []


    def reset(self):
        """Account for posible serialization of new envirnoments"""
        print("ExampleStepper.reset() called")

        # Do this to get a valid reference to the environment in use
        self.env = self.dispatch.env()

        # You can for instance get the number of cells in the maze with:
        self.xCells = self.env.maze.nx
        self.yCells = self.env.maze.ny

        # Or also get the size of a cell
        self.cellSizeX = self.env.maze.cellSizeX
        self.cellSizeY = self.env.maze.cellSizeY

        # Here an arbitrary step size for the "advance" action
        step = self.env.maze.cellSizeX / 3

        # Sample 50/50 a rotation or a translation
        self.actions = [self.env.agent.right,
                        self.env.agent.left,
                        lambda: self.env.agent.advance(step),
                        lambda: self.env.agent.advance(step)]

    def init(self):

        """Reset and setup the stepper"""

        # print("ExampleStepper.init() called")

        # Tell the environment to place the agent at the beginning
        self.env.reset()

        # Ensure the agent's position is properly displayed
        self.dispatch.render()
        self.lastRenderingTime = time.perf_counter()

        self.finX, self.finY = (self.env.maze.endX+0.5)*self.env.maze.cellSizeX, (self.env.maze.endY+0.5)*self.env.maze.cellSizeY
        self.iniX, self.iniY = (0.5)*self.env.maze.cellSizeX, (0.5)*self.env.maze.cellSizeY
        self.dist = euclidean([self.iniX, self.iniY], [self.finX, self.finY])
        self.routes = []

    def normalize(self, state):
        state[0][0], state[0][1], = state[0][0] / 180, state[0][1] / 180
        state[0][2] = state[0][2] / 360
        state[0][3], state[0][4], state[0][5] = state[0][3] / 200, state[0][4] / 200, state[0][5] / 200
        return state

    def step(self, iteration):
        """Perform one simulation step"""

        reward = 0

        state = self.env.agent.state


        state = np.reshape(
            np.array((state.posX, state.posY, state.angle, self.env.agent.observations[0], self.env.agent.observations[1],
                      self.env.agent.observations[2])),
            [1, OBSERVATION_SPACE])


        action= self.solver.take_action(self.normalize(state))

        if (action == 3):
            action = 2
        self.env.tryAction(self.env.agent, self.actions[action])



        done = self.env.finished()

        castigo = -0.001

        if ((state[0][3] < 4 and action == 0)
                or (state[0][4] < 4 and action == 2)
                or (state[0][5] < 4 and action == 1)):
            castigo += -0.1

        if (done):
            reward += 10


        reward -= exp(( euclidean([state[0][0], state[0][1]], [self.iniX, self.iniY]) -
                       euclidean([state[0][0], state[0][1]], [self.finX, self.finY])
                       ) / ( 2 * self.dist)) / math.e + castigo

        state = self.normalize(state)

        self.solver.add_to_memory(state, action, reward)


        if (time.perf_counter() - self.lastRenderingTime) > 1 / 15:
            self.dispatch.render()
            self.lastRenderingTime = time.perf_counter()


        if done:
            self.dispatch.stop()
            self.env.reset()


            self.solver.experience_replay(iteration, self.episodes)

            self.solver.save_model()
            if(self.episodes % 2 == 0):
                self.solver.update_model()

            self.episodes += 1




# #######################
# # Main control center #
# #######################

# This object centralizes everything
theDispatcher = dispatcher.Dispatcher()

# Provide a new environment (maze + agent)
theDispatcher.setEnvironment(env.Environment(12, 8, 15))

# Provide also the simulation stepper, which needs access to the
# agent and maze in the dispatcher.
theDispatcher.setStepper(TrainSolver(theDispatcher))

# Start the GUI and run it until quit is selected
# (Remember Ctrl+\ forces python to quit, in case it is necessary)
theDispatcher.run()
