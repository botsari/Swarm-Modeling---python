# config.py

"""
The class Setting is used to place all parameters and settings
together in one place, and grouped conceptually and functionally into methods 
that are used to make assignments explicit, while remaining both 
local and terse.
"""
import numpy as np

class Settings():
    
    # number of steps to iterate the model before termination 
    num_steps = 10000
    # number of ants on the lattice
    num_ants = 1000
    
    """ lattice parameters """
    # number of nodes in the x direction
    lat_size_x = 120
    # number of nodes in the y direction
    lat_size_y = 100
    # 8 = retangular lattice with nearest neighbor edges including diagonals
    edge_num = 8
    """ explanation of rectangular lattice edge vectors (displayed geometrically 
        below for clarity) where the * symbol represents the starting vertex
            [-1, 1] [0, 1] [1, 1]
            [-1, 0]    *   [1, 0]
            [-1,-1] [0,-1] [1,-1]
        the directions in the 'edge_vectors' array are listed in clockwise order
        starting in the upper left (northwest) corner. so for example
        edge_vectors[2] = [1,1], etc. Hence ..."""
    edge_vectors = [
            [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0] ]
    
    """ pheromone parameters """
    # osmotropotaxic sensitivity parameter
    beta = 3.5
    # recriprocal sesory capacity
    delta = 0.2
    # amount layed down per ant per time step
    eta = 0.07
    # decay rate per time step
    kappa = 0.015
    
    """ graphical display settings """
    # pixel spacing per latice point
    pixel_expand = 7
    # title on window
    title = "An Ant Swarm"
    # background color
    background = "black"
    # size of ants/circles
    ant_size = 4
    # color of ants/circles
    ant_color = "red"
    # window x size in pixels
    win_size_x = pixel_expand * lat_size_x
    # window y size in pixels
    win_size_y = pixel_expand * lat_size_y
    
    def __init__(self):
        pass
    
    def directional_bias(self, i):
        """ takes direction i and returns directional bias weights """
        # forward and lef/right-symetric turn weights - increments of 45 degrees
        w0 = 1.0
        w45 = 0.5
        w90 = 0.25
        w135 = 1.0/12.0
        w180 = 1.0/20.0
        # bias array for default "north" i = 1 direction
        bias_array = np.array([w45, w0, w45, w90, w135, w180, w135, w90])
        # bias array for the direction specificed by argument i
        this_bias_array = np.roll(bias_array, i - 1)
        return this_bias_array