import sys
from .graphbuilder import extract_formulas_and_build_dependencies
from .graph_summarizer import print_summary

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_excel = sys.argv[1]
    else:
        print("Please provide the path to the Excel file as an argument.")
        sys.exit(1)
        


    # Extract formulas and build the dependency graph
    dependency_graph = extract_formulas_and_build_dependencies(path_to_excel)

    print_summary(dependency_graph, {})