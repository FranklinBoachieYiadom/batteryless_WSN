
import matplotlib.pyplot as plt
import os

def plot_energy_levels(energy_log, nodes):
    os.makedirs("results", exist_ok=True)
    for node in nodes[:5]:  # Plot only a few for readability
        plt.plot(energy_log[node.id], label=f"Node {node.id}")
    plt.title("Energy Levels Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Energy (J)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/plots.png")
    plt.close()

def plot_network(net):
    plt.figure(figsize=(8, 8))
    for node in net.nodes:
        plt.plot(node.x, node.y, 'bo')
        for neighbor in node.neighbors:
            plt.plot([node.x, neighbor.x], [node.y, neighbor.y], 'g--', alpha=0.3)
    plt.plot(net.sink.x, net.sink.y, 'rs', label="Sink")
    plt.title("Sensor Network Topology")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/network_topology.png")
    plt.close()


def plot_network_with_path(net, transmission_path):
    """
    Visualize the network topology with node IDs and highlight the transmission path.
    """
    plt.figure(figsize=(10, 10))
    
    # Plot all nodes
    for node in net.nodes:
        color = 'blue' if node != net.sink else 'red'  # Sink node in red
        plt.scatter(node.x, node.y, c=color, s=100, label='Sink' if node == net.sink else 'Node')
        plt.text(node.x + 1, node.y + 1, str(node.id), fontsize=8, color='black')  # Node ID

    # Highlight the transmission path
    if transmission_path:
        for i in range(len(transmission_path) - 1):
            start_node = next(n for n in net.nodes if n.id == transmission_path[i])
            end_node = next(n for n in net.nodes if n.id == transmission_path[i + 1])
            plt.plot(
                [start_node.x, end_node.x],
                [start_node.y, end_node.y],
                color='green', linewidth=2, linestyle='--', label='Transmission Path' if i == 0 else ""
            )

    plt.title("Network Topology with Transmission Path")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    # plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()