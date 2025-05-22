
import random
import csv
from config import *
from utils import plot_all_paths_with_energies
from network import Network


def generate_fixed_network(seed=42):
    random.seed(seed)
    net = Network()
    return net

def get_farthest_node(net):
    sink = net.sink
    farthest_node = max(net.nodes, key=lambda n: n.distance_to(sink))
    return farthest_node

def run_multi_phase_transmissions(phases=10, seed=42):
    # 1. Generate network with fixed seed
    net = generate_fixed_network(seed)
    # 2. Select the farthest node from the sink
    start_node = get_farthest_node(net)
    print(f"Selected farthest node: {start_node.id}")

    # 3. Prepare logging
    all_phase_logs = []

    for phase in range(1, phases + 1):
        print(f"\n--- Phase {phase} ---")
        # Harvest energy for all nodes before each phase
        for node in net.nodes:
            node.harvest_energy()
        net.sink.harvest_energy()

       # Prepare phase log
        phase_log = {
            "phase": phase,
            "start_node": start_node.id,
            "start_energy": round(start_node.energy, 2),
            "path": [],
            "hops": []
        }

        # Transmission logic
        current_node = start_node
        path = [current_node.id]
        hops_log = []

        while current_node != net.sink:
            # Find valid neighbors
            valid_neighbors = [
                n for n in current_node.neighbors
                if n.energy >= ENERGY_THRESHOLD and n.distance_to(net.sink) < current_node.distance_to(net.sink)
            ]
            # Log valid neighbors and their energies
            neighbors_info = [(n.id, round(n.energy, 2)) for n in valid_neighbors]
            hops_log.append({
                "node": current_node.id,
                "valid_neighbors": neighbors_info,
                "energy": round(current_node.energy, 2)
            })

            if not valid_neighbors:
                break  # No path to sink

            # Prefer direct transmission to sink if possible
            sink_neighbor = next((n for n in valid_neighbors if n == net.sink), None)
            if sink_neighbor:
                next_node = net.sink
            else:
                # Otherwise, pick neighbor with highest energy
                next_node = max(valid_neighbors, key=lambda n: n.energy)

            # Transmit and update energy
            current_node.transmit(next_node)
            path.append(next_node.id)
            current_node = next_node

        # Log the path and hops for this phase
        phase_log["path"] = path
        phase_log["hops"] = hops_log    
        all_phase_logs.append(phase_log)

    export_logs_to_csv(all_phase_logs)
    plot_all_paths_with_energies(net, all_phase_logs)
    return all_phase_logs


def export_logs_to_csv(all_phase_logs, filename="transmission_logs.csv"):
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ["phase", "hop", "node", "energy", "valid_neighbors", "path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for phase_log in all_phase_logs:
            phase = phase_log["phase"]
            path_str = str(phase_log["path"])
            for hop_num, hop in enumerate(phase_log["hops"], 1):
                writer.writerow({
                    "phase": phase,
                    "hop": hop_num,
                    "node": hop["node"],
                    "energy": hop["energy"],
                    "valid_neighbors": str(hop["valid_neighbors"]),
                    "path": path_str
                })