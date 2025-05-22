# Creates and manages the sensor network
import random
from node import SensorNode
from config import *

class Network:
    def __init__(self):
        self.nodes = []
        self.sink = SensorNode(0, *SINK_NODE_POSITION)
        self.create_nodes()
        self.update_neighbors()

    def create_nodes(self):
        for i in range(1,NUM_NODES + 1):
            x = random.uniform(0, FIELD_SIZE[0])
            y = random.uniform(0, FIELD_SIZE[1])
            node = SensorNode(i, x, y)
            self.nodes.append(node)

    def update_neighbors(self):
        for node in self.nodes:
            node.neighbors = [
                n for n in self.nodes + [self.sink]
                if n.id != node.id and node.distance_to(n) <= COMM_RANGE
            ]