
import matplotlib.pyplot as plt

def plot_network_with_path(net, transmission_path):
    """
    Visualize the network topology with node IDs and highlight the transmission path.
    """
    plt.figure(figsize=(10, 10))
    
    # Plot all regular nodes
    for node in net.nodes:
        plt.scatter(node.x, node.y, c='blue', s=100)
        plt.text(node.x + 1, node.y + 1, str(node.id), fontsize=8, color='black')

    # Plot the sink node in red
    sink = net.sink
    plt.scatter(sink.x, sink.y, c='red', s=120, label='Sink')
    plt.text(sink.x + 1, sink.y + 1, str(sink.id), fontsize=10, color='red')

    # Highlight the transmission path
    if transmission_path:
        for i in range(len(transmission_path) - 1):
            # Get start node
            if transmission_path[i] == 0:
                start_node = net.sink
            else:
                start_node = next(n for n in net.nodes if n.id == transmission_path[i])
            # Get end node
            if transmission_path[i + 1] == 0:
                end_node = net.sink
            else:
                end_node = next(n for n in net.nodes if n.id == transmission_path[i + 1])
            plt.plot(
                [start_node.x, end_node.x],
                [start_node.y, end_node.y],
                color='green', linewidth=2, linestyle='--', label='Transmission Path' if i == 0 else ""
            )

    plt.title("Network Topology with Transmission Path")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()