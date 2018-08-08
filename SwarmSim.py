#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 15:23:18 2018

@author: Mark Millonas
"""
import numpy as np

from graphics import GraphWin, Circle, Point, update
""" Classes from graphics that ared use by class SwarmGraphics - graphics.py is
a simple object oriented graphics library that is a wrapper around Tkinter,
the de-facto standard GUI package for Python, and should run on any platform
(Windows, Linux, IOS, Unix) where Tkinter is available.
"""

from config import Settings
p = Settings() 


class Swarms(Settings):
    """ Swarms class describes ant/pheromone (particle/field) joint dynamics.
        'ants and 'sigma' (pheromone) arrays are the instance data.
        Methods implement the movement of the ants in response to the pheromone
        and the evolution of the pheromone laid down by the ants, and its
        gradual decay over time. """  
    
    def __init__(self):
        # parent class 'Settings' set up simulation details
        Settings.__init__(self)
        # initialize: zero starting pheromone, all ants have state [0 0 0] """
        ants = []
        for i in range(0, self.num_ants):
            # create initial ant swarm data structure [x, y, n] for each ant
            ants.append([0, 0, 0])
        self.ants = ants
        # initialize pheromone array sigma to zero everywhere
        self.sigma = np.zeros((self.lat_size_x, self.lat_size_y))
    
    """ swarm initialization methods for class Swarms """
    
    def randomize_ants(self):
        """ randomize ants on lattice """
        ants = []
        for i in range(0, self.num_ants):
            # create initial ant swarm data structure
            x = np.random.randint(self.lat_size_x)
            y = np.random.randint(self.lat_size_y)
            n = np.random.randint(self.edge_num)
            ants.append([x, y, n])
        self.ants = ants
        
    def erase_sigma(self):
        """ set pheromone to zero ont he whole lattice """
        self.sigma = np.zeros((self.lat_size_x, self.lat_size_y))
        
    """ utility methods for class Swarms """
       
    def pheromone_weight(self, sigma):
        """ takes sigma (pheromone density) and returns the weight factor """
        return np.power(1.0 + sigma/(1 + self.delta * sigma), self.beta)

    def weighted_choice(self, weights):
        """ takes array of relative weights and returns random choice index """
        # initialize probability density function (pdf)
        pdf = np.zeros(len(weights))
        # integrate ...
        i, norm = 0, 0
        for weight in weights:
            norm += weight
            pdf[i] = norm
            i += 1
        # and normalize pdf
        pdf = np.divide(pdf, norm)
        # roll uniform random [0, 1]
        random_number = np.random.rand()
        # select choice index
        choice_index = 0
        while random_number >= pdf[choice_index]:
            choice_index += 1
        return choice_index
    
    def apply_bcs(self, i, j):
        """  applies toriodal boundary conditions on index i,j """
        # apply x toroidal boundary condition
        if i == -1:
            i = self.lat_size_x - 1
        elif i == self.lat_size_x:
            i = 0
        # apply y toroidal boundary condition
        if j == -1:
            j = self.lat_size_y - 1
        elif j == self.lat_size_y:
            j = 0
        return i, j  
    
    """ dynamics methods for class Swarms """

    def local_pheromone_weights(self, index):
        """ returns pheromone weight vector for indexed lattice neighbors """
        sigma_local = np.zeros(8)
        # get lattice coordinates of ant labled by 'index'
        lattice_location  =  [ self.ants[index][0], self.ants[index][1] ]
        for i in range(0, self.edge_num):
            # get lattice index of neighbor
            local_x = lattice_location[0] + self.edge_vectors[i][0]
            local_y = lattice_location[1] + self.edge_vectors[i][1]
            local_x, local_y = self.apply_bcs(local_x, local_y)
            # get the pheromone on neighbor
            sigma_local[i] = self.sigma[local_x][local_y]
        return self.pheromone_weight(sigma_local)
  
    def update_swarm(self):
        """ move each ant once """
        # move each ant
        for i in range(0, self.num_ants):
            """ make local choice and move each ant  """
            # adjust directional bias to the orientation of the ant
            orientation_bias = self.directional_bias(self.ants[i][2])
            # get pheromone bias vector from pheromone field
            pheromone_bias = self.local_pheromone_weights(i)
            # combine biases
            bias = np.multiply(orientation_bias, pheromone_bias)
            # chose the next direction (angle) to move ...
            new_angle = self.weighted_choice(bias)
            # and update the direction of the ant ...
            self.ants[i][2] = new_angle
            # and get the correponding edge vector
            change = self.edge_vectors[new_angle]
            # update the lattice location of the ant
            new_x = self.ants[i][0] + change[0]
            new_y = self.ants[i][1] + change[1]
            # apply toroidal boundary conditions
            self.ants[i][0], self.ants[i][1] = self.apply_bcs(new_x, new_y)
    
    def update_pheromone(self):
        """ implements pheromone drop by ants, and decay over time """
        # ants lay down pheromone
        for i in range(0, self.num_ants):
            self.sigma[ self.ants[i][0] ][ self.ants[i][1] ] += self.eta    
        # attenuate pheromone
        self.sigma = np.multiply(1 - self.kappa, self.sigma)

"""
graphics functions: these use graphics.py 
"""
class SwarmGraph(Settings):
    
    def __init__(self):
        # parent class 'Settings' set up simulation and graphics details
        Settings.__init__(self)
        # 'win' and 'screen_ants' are instance data
        self.win = GraphWin(
                self.title, self.win_size_x, self.win_size_y, autoflush=False)
        self.win.setBackground(self.background)
        self.screen_ants = [None] * self.num_ants
        
    def initialize_display(self, ants):
        """ causes the screen to be updated to current win data """
        for i in range(0, self.num_ants):
            # map lattice to screen pixels
            x_pixel = self.pixel_expand * ants[i][0]
            y_pixel = self.pixel_expand * ants[i][1]
            self.screen_ants[i] = Circle(Point(x_pixel, y_pixel), self.ant_size)
            self.screen_ants[i].setFill(self.ant_color)
            self.screen_ants[i].draw(self.win)
        update()
            
    def update_display(self, ants):
        """ causes the screen to be updated to current win data """
        for i in range(0, self.num_ants):
            # map lattice to screen pixels
            x_pixel = self.pixel_expand * ants[i][0]
            y_pixel = self.pixel_expand * ants[i][1]
            # redraw ant at new location
            self.screen_ants[i].undraw()
            self.screen_ants[i] = Circle(Point(x_pixel, y_pixel), self.ant_size)
            self.screen_ants[i].setFill(self.ant_color)
            self.screen_ants[i].draw(self.win)
        update()
        
    def end_display(self):
        self.win.close()
        update()
        
            

def main():
    # set up ants (particles) and pheromone (field)
    s = Swarms()
    # randomize ant starting locations and orientations
    s.randomize_ants()
    # set up display window
    g = SwarmGraph()
    # dissplay screen ants
    g.initialize_display(s.ants)
    
    """ main iteration loop """
    for step in range(0, s.num_steps):
        # move ants
        s.update_swarm()
        # update pheromone
        s.update_pheromone()
        # update display 
        g.update_display(s.ants)
        
    # graphics book keeping prior to termination
    g.end_display()


main()



