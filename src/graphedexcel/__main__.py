import os
import sys
from .graphbuilder import extract_formulas_and_build_dependencies
from .graph_summarizer import print_summary
from .graph_visualizer import visualize_dependency_graph
if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_excel = sys.argv[1]
    else:
        print("Please provide the path to the Excel file as an argument.")
        sys.exit(1)


    # does the file exist?
    if not os.path.exists(path_to_excel):
        print(f"File not found: {path_to_excel}")
        sys.exit(1)


    # Extract formulas and build the dependency graph
    dependency_graph, functions = extract_formulas_and_build_dependencies(path_to_excel)

    print_summary(dependency_graph, functions)

    if "--no-visualize" not in sys.argv:
        print(
            "\033[1;30;40m\nVisualizing the graph of dependencies.\nThis might take a while...\033[0;37;40m\n"  # noqa
        )

        visualize_dependency_graph(dependency_graph, path_to_excel)
