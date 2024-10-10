import json

# import matplotlib.cm as cm
import matplotlib
import matplotlib.patches as mpatches
import networkx as nx
import matplotlib.pyplot as plt
import sys

import logging

logger = logging.getLogger(__name__)

# Use a non-interactive backend for matplotlib.
# No need to show plots, just save them.
matplotlib.use("Agg")

# Default settings for the graph visualization
base_graph_settings = {
    "node_size": 50,  # the size of the node
    "width": 0.2,  # the width of the edge between nodes
    "edge_color": "black",  # the color of the edge between nodes
    "linewidths": 0,  # the stroke width of the node border
    "with_labels": False,  # whether to show the node labels
    "font_size": 10,  # the size of the node labels
    "cmap": "tab20b",  # the color map to use for coloring nodes
}

# Sized-based settings for small, medium, and large graphs
small_graph_settings = {"with_labels": False, "alpha": 0.8}

medium_graph_settings = {
    "node_size": 30,
    "with_labels": False,
    "alpha": 0.4,
}

large_graph_settings = {
    "node_size": 20,
    "with_labels": False,
    "alpha": 0.2,
}


def load_json_config(config_path: str) -> dict:
    """
    Load the JSON configuration from the specified file.

    Args:
        config_path (str): Path to the JSON config file.

    Returns:
        dict: Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the config file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
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
    Optionally merges with a user-provided JSON config.

    Args:
        graph_size (int): Number of nodes in the graph.
        config_path (str, optional): Path to a JSON configuration file.

    Returns:
        dict: Merged graph settings.
    """
    if graph_size < 200:
        plot_settings = merge_configs(base_graph_settings, small_graph_settings)
    elif graph_size < 500:
        plot_settings = merge_configs(base_graph_settings, medium_graph_settings)
    else:
        plot_settings = merge_configs(base_graph_settings, large_graph_settings)

    if config_path:
        try:
            custom_settings = load_json_config(config_path)
            plot_settings = merge_configs(plot_settings, custom_settings)
        except FileNotFoundError:
            logger.error(
                f"Config file not found: {config_path}. Using default settings."
            )

        except json.JSONDecodeError:
            logger.error(
                f"Invalid JSON format in config file: {config_path}. Using default settings."
            )
        except Exception as e:
            logger.error(
                f"Error loading config file: {config_path}. Using default settings.\n{e}"
            )

    return plot_settings


def calculate_fig_size(graph_size: int) -> tuple:
    base_size = 10
    max_size = 30  # prevents the figure from eating the world
    scaling_factor = max(1, graph_size / 100)

    return (
        min(max_size, base_size * scaling_factor),
        min(max_size, base_size * scaling_factor),
    )


def get_node_colors_and_legend(graph: nx.DiGraph, cmap_id: str) -> tuple[list, list]:
    """
    Assign colors to nodes based on their sheet and create legend patches.
    """
    sheets = {data.get("sheet", "Sheet1") for _, data in graph.nodes(data=True)}
    color_map = plt.get_cmap(cmap_id, len(sheets))

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
    graph: nx.DiGraph,
    output_path: str = None,
    config_path: str = None,
    layout: str = "spring",
):
    """
    Render the dependency graph using matplotlib and networkx.
    """

    # Set the default settings for the graph visualization based on the number of nodes
    graph_settings = get_graph_default_settings(len(graph.nodes), config_path)

    logger.info(
        f"Using the following settings for the graph visualization: {graph_settings}"
    )

    fig_size = calculate_fig_size(len(graph.nodes))
    logger.info(f"Calculated figure size: {fig_size}")

    figsize_override = graph_settings.pop("fig_size", None)
    # Remove fig_size from graph_settings
    if figsize_override:
        logger.info(f"Using size from settings: {figsize_override}")
        fig_size = figsize_override
    plt.figure(figsize=fig_size)

    # Choose layout based on input
    if layout == "spring":
        pos = nx.spring_layout(graph)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(graph)
    elif layout == "circular":
        pos = nx.circular_layout(graph)
    elif layout == "shell":
        pos = nx.shell_layout(graph)
    elif layout == "spectral":
        pos = nx.spectral_layout(graph)
    else:
        logger.warning(f"Unknown layout '{layout}'. Falling back to spring layout.")
        pos = nx.spring_layout(graph)

    # Assign colors and get legend patches
    node_colors, legend_patches = get_node_colors_and_legend(
        graph, graph_settings.pop("cmap", "tab20b")
    )

    nx.draw(
        graph,
        pos,
        node_color=node_colors,
        **graph_settings,
    )

    plt.legend(handles=legend_patches, title="Sheets", loc="upper left")

    plt.savefig(output_path, bbox_inches="tight")  # Ensure layout fits
    plt.close()  # Close the figure to free memory

    logger.info(f"Graph visualization saved to {output_path}")
