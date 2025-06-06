
import math
import random
from config import *

class SensorNode:
    def __init__(self, node_id, x, y, energy=None):
        self.id = node_id
        self.x = x
        self.y = y
        
        # Initial energy is random unless specified
        self.energy = random.uniform(0.5, 2.0) if energy is None else energy
        self.neighbors = []
        self.successful_transmissions = 0
        self.retry_count = 0
        self.wait_time = 0
        self.total_transmissions = 0

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def harvest_energy(self):
        self.energy += random.uniform(ENERGY_HARVEST_MIN, ENERGY_HARVEST_MAX)
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY

    def can_transmit(self):
        return self.energy >= ENERGY_THRESHOLD

    def transmit(self, receiver):
        if self.can_transmit():
            if receiver.energy >= ENERGY_THRESHOLD:
                self.energy -= TX_ENERGY_COST
                self.successful_transmissions += 1
                self.wait_time = 0
            else:
                self.retry_count += 1
                self.wait_time += 1
            self.total_transmissions += 1