import matplotlib.cm as cm
import matplotlib.patches as mpatches
import networkx as nx
import matplotlib.pyplot as plt
import sys

small_graph_settings = {
    "node_size": 50,
    "edge_color": "black",
    "with_labels": False,
    "font_size": 10,
    "linewidths": 0.8,
    "alpha": 0.8,
    "width": 0.2,
}

medium_graph_settings = {
    "node_size": 30,
    "edge_color": "gray",
    "with_labels": True,
    "font_size": 10,
    "linewidths": 0.1,
    "alpha": 0.4,
    "width": 0.2,
}

large_graph_settings = {
    "node_size": 5,
    "edge_color": "gray",
    "with_labels": False,
    "font_size": 12,
    "linewidths": 0.5,
    "alpha": 0.2,
    "width": 0.2,
}


def get_graph_default_settings(graph_size):
    """
    Set the default settings for the graph visualization based on the number of nodes.
    """

    if graph_size < 200:
        settings = small_graph_settings
        fig_size = 10
    elif graph_size < 500:
        settings = medium_graph_settings
        fig_size = 20
    else:
        settings = large_graph_settings
        fig_size = 20

    return settings, fig_size


# Function to get colors and generate legend for sheets
def get_node_colors_and_legend(graph):
    sheets = {data.get("sheet", "Sheet1") for _, data in graph.nodes(data=True)}
    color_map = cm.get_cmap("tab20c", len(sheets))

    # Map sheet names to colors
    sheet_to_color = {sheet: color_map(i) for i, sheet in enumerate(sheets)}

    # Assign colors to nodes based on their sheet
    node_colors = [
        sheet_to_color[data.get("sheet", "Sheet1")]
        for _, data in graph.nodes(data=True)
    ]

    # Create patches for the legend
    legend_patches = [
        mpatches.Patch(color=color, label=sheet)
        for sheet, color in sheet_to_color.items()
    ]

    return node_colors, legend_patches


def visualize_dependency_graph(graph, file_path):
    """
    Render the dependency graph using matplotlib and networkx.
    """

    if "--keep-direction" not in sys.argv:
        # Convert the graph to an undirected graph
        graph = graph.to_undirected()

    # Set the default settings for the graph visualization based on the number of nodes
    graph_settings, fig_size = get_graph_default_settings(len(graph.nodes))

    plt.figure(figsize=(fig_size, fig_size))
    node_colors = [hash(graph.nodes[node]["sheet"]) % 256 for node in graph.nodes]
    pos = nx.spring_layout(graph)  # layout for nodes

    # add legends for the colors
    node_colors, legend_patches = get_node_colors_and_legend(graph)

    nx.draw(
        graph,
        pos,
        node_color=node_colors,
        **graph_settings,
    )

    plt.legend(handles=legend_patches, title="Sheets", loc="upper left")

    filename = f"{file_path}.png"
    plt.savefig(filename)
    print(f"Graph visualization saved to {filename}")

    # open the image file in windows
    if sys.platform == "win32" and "--open-image" in sys.argv:
        import os

        os.system(f"start {filename}")
