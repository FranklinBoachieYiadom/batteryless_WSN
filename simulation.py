import random
import csv
import numpy as np
import matplotlib.pyplot as plt
from config import *
from utils import plot_all_paths_with_energies
from network import Network



def generate_fixed_network(positions_seed=42):
    net = Network(positions_seed=positions_seed)
    return net

def get_farthest_node(net):
    sink = net.sink
    farthest_node = max(net.nodes, key=lambda n: n.distance_to(sink))
    return farthest_node

def run_multi_phase_transmissions(seed=42, visualize=True):
    net = generate_fixed_network(seed)
    start_node = get_farthest_node(net)    
    print(f"Selected farthest node: {start_node.id}")

    all_phase_logs = []
    attacker_pos = net.sink.id  # Attacker starts at sink only at the very beginning
    attacker_path = [attacker_pos]
    phase = 1

    while True:
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
            "hops": [],
            "attacker_position": attacker_pos,
            "attacker_path": list(attacker_path),  # Copy for this phase
            "attacker_captured_source": False
        }

        # Transmission logic
        current_node = start_node
        path = [current_node.id]
        hops_log = []

        while current_node != net.sink:
            # valid_neighbors = [
            #     n for n in current_node.neighbors
            #     if n.energy >= ENERGY_THRESHOLD and n.distance_to(net.sink) < current_node.distance_to(net.sink)
            # ]
            valid_neighbors = [
                n for n in current_node.neighbors
                if (
                    (n == net.sink) or
                    (n.energy >= ENERGY_THRESHOLD)
                ) and n.distance_to(net.sink) < current_node.distance_to(net.sink)
            ]
            neighbors_info = [(n.id, round(n.energy, 2)) for n in valid_neighbors]
            hops_log.append({
                "node": current_node.id,
                "valid_neighbors": neighbors_info,
                "energy": round(current_node.energy, 2)
            })

            if not valid_neighbors:
                break  # No path to sink

            sink_neighbor = next((n for n in valid_neighbors if n == net.sink), None)
            if sink_neighbor:
                next_node = net.sink
            else:
                next_node = max(valid_neighbors, key=lambda n: n.energy)

            current_node.transmit(next_node)
            path.append(next_node.id)
            current_node = next_node

        # Log the path and hops for this phase
        phase_log["path"] = path
        phase_log["hops"] = hops_log

        # --- Attacker logic ---
        # If attacker is on the path (and not at the source), move one hop toward the source
        if attacker_pos in path and attacker_pos != start_node.id:
            idx = path.index(attacker_pos)
            if idx > 0:
                attacker_pos = path[idx - 1]
                attacker_path.append(attacker_pos)
        # If attacker reaches the source, mark as captured and stop
        if attacker_pos == start_node.id:
            phase_log["attacker_captured_source"] = True
            phase_log["attacker_position"] = attacker_pos
            phase_log["attacker_path"] = list(attacker_path)
            all_phase_logs.append(phase_log)
            print(f"Attacker captured the source at phase {phase}!")
            break

        phase_log["attacker_position"] = attacker_pos
        phase_log["attacker_path"] = list(attacker_path)
        all_phase_logs.append(phase_log)
        phase += 1

    
    export_logs_to_csv(all_phase_logs)
    if visualize:
        plot_all_paths_with_energies(net, all_phase_logs)
    print(f"Total phases until attacker captured source: {phase}")
    return all_phase_logs

    # export_logs_to_csv(all_phase_logs)
    # plot_all_paths_with_energies(net, all_phase_logs)
    # print(f"Total phases until attacker captured source: {phase}")
    # return all_phase_logs

def export_logs_to_csv(all_phase_logs, filename="transmission_logs.csv"):
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = [
            "phase", "hop", "node", "energy", "valid_neighbors", "path",
            "attacker_position", "attacker_path", "attacker_captured_source"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for phase_log in all_phase_logs:
            phase = phase_log["phase"]
            path_str = str(phase_log["path"])
            attacker_position = phase_log.get("attacker_position", "")
            attacker_path = str(phase_log.get("attacker_path", []))
            attacker_captured = phase_log.get("attacker_captured_source", False)
            for hop_num, hop in enumerate(phase_log["hops"], 1):
                writer.writerow({
                    "phase": phase,
                    "hop": hop_num,
                    "node": hop["node"],
                    "energy": hop["energy"],
                    "valid_neighbors": str(hop["valid_neighbors"]),
                    "path": path_str,
                    "attacker_position": attacker_position,
                    "attacker_path": attacker_path,
                    "attacker_captured_source": attacker_captured
                })

def average_capture_phases(num_trials=5, seed_start=1000, visualize_last=True):
    """
    Runs the simulation multiple times and computes the average number of phases
    it takes for the attacker to capture the source node.
    Each run uses a different random seed for initial energies and harvesting.
    """
    phase_counts = []
    for i in range(num_trials):
        print(f"\n=== Trial {i+1}/{num_trials} ===")
        # Use a different seed for each run to ensure different energy dynamics
        all_phase_logs = run_multi_phase_transmissions(seed=seed_start + i, visualize=(visualize_last and i == num_trials-1))
        phase_counts.append(len(all_phase_logs))
    avg = np.mean(phase_counts)
    std = np.std(phase_counts)
    print(f"\nAverage number of phases for attacker to capture source: {avg:.2f} ± {std:.2f} (std)")
    print(f"All phase counts: {phase_counts}")

    # Plot histogram
    plt.figure()
    plt.hist(phase_counts, bins=20, color='skyblue', edgecolor='black')
    plt.title("Histogram of Phases Until Attacker Captures Source")
    plt.xlabel("Number of Phases")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return avg, std, phase_counts