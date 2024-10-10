import os
import sys
import argparse
import logging
from .graphbuilder import build_graph_and_stats
from .graph_summarizer import print_summary
from .graph_visualizer import visualize_dependency_graph
import src.graphedexcel.logger_config  # noqa

logger = logging.getLogger("graphedexcel.main")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="graphedexcel",
        description="Process an Excel file to build and visualize dependency graphs.",
    )

    # Positional argument for the path to the Excel file
    parser.add_argument(
        "path_to_excel", type=str, help="Path to the Excel file to process."
    )

    # Optional flags with shorthand aliases
    parser.add_argument(
        "--remove-unconnected",
        "-r",
        action="store_true",
        help="Remove unconnected nodes from the dependency graph.",
    )

    parser.add_argument(
        "--as-directed-graph",
        "-d",
        action="store_true",
        help="Treat the dependency graph as directed.",
    )

    parser.add_argument(
        "--no-visualize",
        "-n",
        action="store_true",
        help="Skip the visualization of the dependency graph.",
    )

    parser.add_argument(
        "--layout",
        "-l",
        type=str,
        default="spring",
        choices=["spring", "circular", "kamada_kawai", "shell", "spectral"],
        help="Layout algorithm for graph visualization (default: spring).",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="Path to the configuration file for visualization. See README for details.",
    )

    parser.add_argument(
        "--output-path",
        "-o",
        type=str,
        default=None,
        help="Specify the output path for the generated graph image.",
    )

    parser.add_argument(
        "--open-image",
        action="store_true",
        help="Open the generated image after visualization.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    path_to_excel = args.path_to_excel

    # Check if the file exists
    if not os.path.exists(path_to_excel):
        logger.error(f"File not found: {path_to_excel}")
        sys.exit(1)

    # Build the dependency graph and gather statistics
    dependency_graph, function_stats = build_graph_and_stats(
        path_to_excel,
        remove_unconnected=args.remove_unconnected,
        as_directed=args.as_directed_graph,
    )

    # Print summary of the dependency graph
    print_summary(dependency_graph, function_stats)

    if args.no_visualize:
        logger.info("Skipping visualization as per the '--no-visualize' flag.")
        sys.exit(0)

    logger.info("Visualizing the graph of dependencies. (This might take a while...)")

    # Determine layout
    layout = args.layout

    # Configuration path
    config_path = args.config

    # Determine output filename
    if args.output_path:
        filename = args.output_path
    else:
        # Create a default filename based on the Excel file name
        base_name = os.path.splitext(os.path.basename(path_to_excel))[0]
        filename = f"{base_name}_dependency_graph.png"

    # Visualize the dependency graph
    visualize_dependency_graph(dependency_graph, filename, config_path, layout)

    logger.info(f"Dependency graph image saved to {filename}.")

    # Open the image file if requested
    if args.open_image:
        try:
            os.startfile(filename)  # Note: os.startfile is Windows-specific
        except AttributeError:
            # For macOS and Linux, use 'open' and 'xdg-open' respectively
            import subprocess
            import platform

            if platform.system() == "Darwin":  # macOS
                subprocess.call(["open", filename])
            elif platform.system() == "Linux":
                subprocess.call(["xdg-open", filename])
            else:
                logger.warning("Unable to open the image automatically on this OS.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("An unexpected error occurred:", e)
        sys.exit(1)
