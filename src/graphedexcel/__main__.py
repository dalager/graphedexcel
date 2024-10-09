import os
import sys
from .graphbuilder import extract_formulas_and_build_dependencies
from .graph_summarizer import print_summary
from .graph_visualizer import visualize_dependency_graph
import logging
import src.graphedexcel.logger_config  # noqa

logger = logging.getLogger(__name__)

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

    if "--no-visualize" not in sys.argv:
        logger.info(
            "\033[1;30;40m\nVisualizing the graph of dependencies.\nThis might take a while...\033[0;37;40m\n"  # noqa
        )

        # if commandline argument --config is provided with a path to a JSON file, pass that path to the visualizer
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

        visualize_dependency_graph(dependency_graph, path_to_excel, config_path, layout)
