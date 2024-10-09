import json
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import networkx as nx
import matplotlib.pyplot as plt
import sys


# Default settings for the graph visualization
base_graph_settings = {
    "node_size": 50,  # the size of the node
    "width": 0.2,  # the width of the edge between nodes
    "edge_color": "black",  # the color of the edge between nodes
    "linewidths": 0,  # the stroke width of the node border
    "with_labels": False,  # whether to show the node labels
    "font_size": 10,  # the size of the node labels
    "cmap": "tab20b",  # the color map to use for coloring nodes
    "fig_size": (10, 10),  # the size of the figure
}

# Sized-based settings for small, medium, and large graphs
small_graph_settings = {"with_labels": False, "alpha": 0.8}

medium_graph_settings = {
    "node_size": 30,
    "with_labels": False,
    "alpha": 0.4,
    "fig_size": (20, 20),
}

large_graph_settings = {
    "node_size": 20,
    "with_labels": False,
    "alpha": 0.2,
    "fig_size": (25, 25),
}


def load_json_config(config_path: str) -> dict:
    """
    Load the JSON config file.
    """
    with open(config_path, "r") as file:
        return json.load(file)


def merge_configs(default_config: dict, custom_config: dict) -> dict:
    """
    Merge the custom config with the default config.
    """
    merged_config = default_config.copy()
    merged_config.update(custom_config)
    return merged_config


def get_graph_default_settings(graph_size: int, config_path: str = None) -> dict:
    """
    Gets the default settings for the graph visualization based on the number of nodes.
    And the Fig size based on the number of nodes.
    """
    plot_settings = {}

    if graph_size < 200:
        plot_settings = merge_configs(base_graph_settings, small_graph_settings)

    elif graph_size < 500:
        plot_settings = merge_configs(base_graph_settings, medium_graph_settings)

    else:
        plot_settings = merge_configs(base_graph_settings, large_graph_settings)

    if config_path:
        try:
            custom_settings = load_json_config(config_path)
            return merge_configs(base_graph_settings, custom_settings)
        except Exception as e:
            print(
                f"Error loading config file: {config_path}, using default settings.\n{e}"
            )
    return plot_settings


def get_node_colors_and_legend(graph: nx.DiGraph, color_map: str) -> tuple[list, list]:
    """
    Assign colors to nodes based on their sheet and create legend patches.
    """
    sheets = {data.get("sheet", "Sheet1") for _, data in graph.nodes(data=True)}
    color_map = cm.get_cmap(color_map, len(sheets))

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


def visualize_dependency_graph(
    graph: nx.DiGraph, file_path: str, config_path: str = None
):
    """
    Render the dependency graph using matplotlib and networkx.
    """

    if "--keep-direction" not in sys.argv:
        # Convert the graph to an undirected graph
        graph = graph.to_undirected()

    # Set the default settings for the graph visualization based on the number of nodes
    graph_settings = get_graph_default_settings(len(graph.nodes), config_path)

    # print graph_settings
    print(graph_settings)
    plt.figure(figsize=graph_settings["fig_size"])
    # remove fig_size from the graph_settings, we have already used it
    graph_settings.pop("fig_size", None)
    node_colors = [hash(graph.nodes[node]["sheet"]) % 256 for node in graph.nodes]
    pos = nx.spring_layout(graph)  # layout for nodes

    # add legends for the colors
    node_colors, legend_patches = get_node_colors_and_legend(
        graph, graph_settings["cmap"]
    )
    # remove 'cmap' from the graph_settings, we have already used it
    graph_settings.pop("cmap", None)

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
