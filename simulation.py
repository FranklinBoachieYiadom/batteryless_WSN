# simulation.py
# Main logic for running the simulation
import random
from config import *
from utils import plot_energy_levels, plot_network, plot_network_with_path
from network import Network

# def run_simulation():
#     net = Network()
#     energy_log = {n.id: [] for n in net.nodes}

#     for step in range(SIMULATION_STEPS):
#         for node in net.nodes:
#             node.harvest_energy()

#         for node in net.nodes:
#             if node.can_transmit():
#                 # Select neighbors that are closer to the sink and have enough energy
#                 valid_neighbors = [
#                     n for n in node.neighbors
#                     if n.energy >= ENERGY_THRESHOLD and n.distance_to(net.sink) < node.distance_to(net.sink)
#                 ]
#                 if valid_neighbors:
#                     best = sorted(valid_neighbors, key=lambda n: n.energy, reverse=True)[0]
#                     node.transmit(best)
#                 else:
#                     node.retry_count += 1
#                     node.wait_time += 1

#             energy_log[node.id].append(node.energy)

#     plot_energy_levels(energy_log, net.nodes)
#     plot_network(net)
#     print_results(net)




def run_single_transmission():
    """
    Simulates a single transmission from a random node to the sink node.
    Logs failed paths, energy levels, and time taken for successful transmission.
    Visualizes the network and the transmission path.
    """
    # Initialize the network
    net = Network()
    transmission_path = []  # To store the path of the first successful transmission
    failed_paths = []       # To store paths that failed
    energy_log = {}         # To log energy levels of nodes in paths

    # Select a random starting node (not the sink)
    start_node = random.choice(net.nodes)
    while start_node == net.sink:  # Ensure the starting node is not the sink
        start_node = random.choice(net.nodes)
    print(f"Starting transmission from Node {start_node.id}")

    for step in range(SIMULATION_STEPS):
        # Step 1: Harvest energy for all nodes
        for node in net.nodes:
            node.harvest_energy()

        # Step 2: Attempt transmission from the starting node
        if start_node.can_transmit():
            # Select neighbors that are closer to the sink and have enough energy
            valid_neighbors = [
                n for n in start_node.neighbors
                if n.energy >= ENERGY_THRESHOLD and n.distance_to(net.sink) < start_node.distance_to(net.sink) 
            ]
            print(f"Valid neighbors for Node {start_node.id}: {[n.id for n in valid_neighbors]}")
            if valid_neighbors:
                # Choose the best neighbor (highest energy)
                best = sorted(valid_neighbors, key=lambda n: n.energy, reverse=True)[0]
                start_node.transmit(best)
                transmission_path.append(start_node.id)  # Log the current node in the path

                # Log energy levels of nodes in the path
                energy_log[start_node.id] = start_node.energy

                # Check if the sink is reached
                if best == net.sink:
                    transmission_path.append(best.id)
                    energy_log[best.id] = best.energy
                    print(f"Transmission Path: {transmission_path}")
                    print(f"Energy Levels: {energy_log}")
                    print(f"Time Taken: {step + 1} steps")
                    
                    plot_network_with_path(net, transmission_path)  # Visualize the network and path
                    return
                else:
                    # Update the starting node to the next node in the path
                    start_node = best
            else:
                # Log the failed path and energy levels
                failed_paths.append(transmission_path + [start_node.id])
                energy_log[start_node.id] = start_node.energy
                print(f"Failed Path: {transmission_path + [start_node.id]}")
                print(f"Energy Levels: {energy_log}")

                # No valid neighbors, increment retry count and wait time
                start_node.retry_count += 1
                start_node.wait_time += 1
        else:
            # Log the failed path if the starting node cannot transmit
            failed_paths.append(transmission_path + [start_node.id])
            energy_log[start_node.id] = start_node.energy
            print(f"Failed Path: {transmission_path + [start_node.id]}")
            print(f"Energy Levels: {energy_log}")

    # If the simulation ends without reaching the sink
    print("Transmission failed to reach the sink within the simulation steps.")
    print(f"Failed Paths: {failed_paths}")
    print(f"Energy Levels: {energy_log}")
    

def print_results(net):
    total_sent = sum(n.total_transmissions for n in net.nodes)
    successful = sum(n.successful_transmissions for n in net.nodes)
    retries = sum(n.retry_count for n in net.nodes)
    avg_wait = sum(n.wait_time for n in net.nodes) / len(net.nodes)
    pdr = (successful / total_sent * 100) if total_sent > 0 else 0

    print(f"Total Transmissions: {total_sent}")
    print(f"Successful Transmissions: {successful}")
    print(f"Packet Delivery Ratio (PDR): {pdr:.2f}%")
    print(f"Total Retries: {retries}")
    print(f"Average Wait Time: {avg_wait:.2f} steps")