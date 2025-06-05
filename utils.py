
import matplotlib.pyplot as plt

def plot_all_paths_with_energies(net, all_phase_logs):
    plt.figure(figsize=(10, 10))

    # Plot all nodes with their energies as text
    for node in net.nodes:
        plt.scatter(node.x, node.y, c='gray', s=40, zorder=2)
        plt.text(node.x + 1, node.y + 1, f"{node.id}", fontsize=7, color='black', zorder=3)

    # Plot the sink node in red
    sink = net.sink
    plt.scatter(sink.x, sink.y, c='red', s=120, label='Sink', zorder=4)
    plt.text(sink.x + 1, sink.y + 1, f"{sink.id}", fontsize=9, color='red', zorder=5)

    # Color cycle for phases
    colors = plt.cm.get_cmap('tab10', len(all_phase_logs))

    # Plot all paths, each in a different color
    for idx, phase_log in enumerate(all_phase_logs):
        path = phase_log["path"]
        if len(path) < 2:
            continue
        xs, ys = [], []
        for node_id in path:
            if node_id == 0:
                node = net.sink
            else:
                node = next(n for n in net.nodes if n.id == node_id)
            xs.append(node.x)
            ys.append(node.y)
        plt.plot(xs, ys, color=colors(idx), linewidth=1, label=f"Phase {phase_log['phase']}", zorder=1)

    # Plot attacker positions for each phase as a star
    for idx, phase_log in enumerate(all_phase_logs):
        attacker_id = phase_log.get("attacker_position", None)
        if attacker_id is not None:
            if attacker_id == 0:
                attacker_node = net.sink
            else:
                attacker_node = next(n for n in net.nodes if n.id == attacker_id)
            plt.scatter(attacker_node.x, attacker_node.y, marker='*', s=400,
                        c='red', edgecolors='black', zorder=10,
                        label=f"Attacker Phase {phase_log['phase']}" if idx == 0 else "")

    plt.title("All Transmission Paths with Attacker Progress")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    # plt.legend()
    plt.grid(True)
    # plt.tight_layout()
    plt.show()



