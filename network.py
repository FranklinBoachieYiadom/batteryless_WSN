# Creates and manages the sensor network
import random
from node import SensorNode
from config import *

class Network:
    def __init__(self, positions_seed=42):
        self.nodes = []
        self.sink = SensorNode(0, *SINK_NODE_POSITION, energy=0)  # Sink energy can be 0 or any value
        self.create_nodes(positions_seed)
        self.update_neighbors()

    def create_nodes(self, positions_seed):
        # Fix positions using the seed
        rnd = random.Random(positions_seed)
        positions = []
        for i in range(1, NUM_NODES + 1):
            x = rnd.uniform(0, FIELD_SIZE[0])
            y = rnd.uniform(0, FIELD_SIZE[1])
            positions.append((i, x, y))
        # Now assign random initial energies (unseeded)
        for i, x, y in positions:
            node = SensorNode(i, x, y)  # SensorNode will assign random energy
            self.nodes.append(node)

    def update_neighbors(self):
        for node in self.nodes:
            node.neighbors = [
                n for n in self.nodes + [self.sink]
                if n.id != node.id and node.distance_to(n) <= COMM_RANGE
            ]