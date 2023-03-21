import numpy as np
import geopy.distance

class Node:
    def __init__(self, i, lon, lat, depth):
        self.index = i
        self.lon   = lon
        self.lat   = lat
        self.depth = depth

class BoundaryCondition:
    def __init__(self, i, num_nodes, bctype, nodes):
        self.index     = i
        self.num_nodes = num_nodes
        self.bctype    = bctype
        self.nodes     = nodes

    def set_factors(self, factors):
        """Basic setter for the factors attribute"""
        self.factors = factors

    def get_depths(self):
        """ """
        pass

    def avg_dist_between_nodes(self):
        """Calculates distance (in m) between two geographical coordinates
        of adjacent boundary nodes, and returns the average distance over a
        given boundary segment"""

        dists = []
        for i in range(len(self.nodes)-1):
            coord1 = (self.nodes[i  ].lat, self.nodes[i  ].lon)
            coord2 = (self.nodes[i+1].lat, self.nodes[i+1].lon)

            dists.append(geopy.distance.geodesic(coord1, coord2).km * 1000)
            #print('Distance between', coord1, 'and', coord2, ':', dists[-1])

        self.avg_dist = np.mean(dists)
        self.total_bc_len = self.avg_dist * (self.num_nodes - 1)
        return self.avg_dist
