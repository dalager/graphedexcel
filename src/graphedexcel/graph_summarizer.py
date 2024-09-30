from collections import Counter


def print_summary(graph, functionsdict):
    """
    Summarize a networkx DiGraph representing a dependency graph and print the most used functions in the formulas.
    """
    strpadsize = 28
    numpadsize = 5

    print_basic_info(graph, strpadsize, numpadsize)
    print_highest_degree_nodes(graph, strpadsize, numpadsize)
    print_most_used_functions(functionsdict, strpadsize, numpadsize)


def print_basic_info(graph, strpadsize, numpadsize):
    print("===  Dependency Graph Summary ===")
    print(
        "Cell/Node count".ljust(strpadsize, " ")
        + str(graph.number_of_nodes()).rjust(numpadsize, " ")
    )
    print(
        "Dependency count".ljust(strpadsize, " ")
        + str(graph.number_of_edges()).rjust(numpadsize, " ")
    )
    print()


def print_highest_degree_nodes(graph, strpadsize, numpadsize):
    print("\n===  Most connected nodes     ===")
    degree_view = graph.degree()
    degree_counts = Counter(dict(degree_view))
    max_degree_node = degree_counts.most_common(10)

    for node, degree in max_degree_node:
        print(f"{node.ljust(strpadsize)}{str(degree).rjust(numpadsize, ' ')} ")


def print_most_used_functions(functionsdict, strpadsize, numpadsize):
    print("\n===  Most used functions      ===")
    sorted_functions = dict(
        sorted(functionsdict.items(), key=lambda item: item[1], reverse=True)
    )

    for function, count in sorted_functions.items():
        print(f"{function.ljust(strpadsize, ' ')}{str(count).rjust(numpadsize, ' ')}")
