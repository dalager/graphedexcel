import sys
from .graphbuilder import extract_formulas_and_build_dependencies
from .graph_summarizer import print_summary
from .graph_visualizer import visualize_dependency_graph

functions_dict = {}

def main(path_to_excel: str = "Book1.xlsx", visualize: bool = True) -> None:
    """
    Main function to extract formulas, build the dependency graph, and optionally visualize it.

    Args:
        path_to_excel (str): Path to the Excel file.
        visualize (bool): Whether to visualize the dependency graph.
    """
    # Extract formulas and build the dependency graph
    dependency_graph = extract_formulas_and_build_dependencies(path_to_excel)

    print_summary(dependency_graph, functions_dict)

    if visualize:
        print(
            "\033[1;30;40m\nVisualizing the graph of dependencies.\nThis might take a while...\033[0;37;40m\n"  # noqa
        )
        visualize_dependency_graph(dependency_graph, path_to_excel)

def run_from_command_line() -> None:
    """
    Run the main function with command-line arguments.
    """
    path_to_excel = "Book1.xlsx"
    visualize = "--no-visualize" not in sys.argv

    if len(sys.argv) > 1:
        path_to_excel = sys.argv[1]

    main(path_to_excel, visualize)

if __name__ == "__main__":
    run_from_command_line()