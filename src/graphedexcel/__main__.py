import os
import sys
from .graphbuilder import extract_formulas_and_build_dependencies
from .graph_summarizer import print_summary
from .graph_visualizer import visualize_dependency_graph
import logging
import src.graphedexcel.logger_config  # noqa

logger = logging.getLogger("graphedexcel.main")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_excel = sys.argv[1]
    else:
        logger.warning("Please provide the path to the Excel file as an argument.")
        sys.exit(1)

    # does the file exist?
    if not os.path.exists(path_to_excel):
        logger.error(f"File not found: {path_to_excel}")
        sys.exit(1)

    # Extract formulas and build the dependency graph
    dependency_graph, functions = extract_formulas_and_build_dependencies(path_to_excel)

    print_summary(dependency_graph, functions)

    if "--no-visualize" in sys.argv:
        logger.info("Skipping visualization.")
        sys.exit(0)

    logger.info("Visualizing the graph of dependencies. (This might take a while...)")

    if "--layout" in sys.argv:
        layout_index = sys.argv.index("--layout")
        layout = sys.argv[layout_index + 1]
    else:
        layout = "spring"

    if "--config" in sys.argv:
        config_index = sys.argv.index("--config")
        config_path = sys.argv[config_index + 1]
    else:
        config_path = None

    filename = f"{path_to_excel}_dependency_graph.png"

    if "--output-path" in sys.argv:
        output_index = sys.argv.index("--output-path")
        filename = sys.argv[output_index + 1]

    visualize_dependency_graph(
        dependency_graph, path_to_excel, filename, config_path, layout
    )

    # Open the image file
    if "--open-image" in sys.argv:
        os.startfile(filename)
