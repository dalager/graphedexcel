from graphedexcel.graph_summarizer import print_summary
import networkx as nx


def test_graph_with_functionsstats():
    # Test that the function runs without errors
    G = nx.DiGraph()
    G.add_node("Src", sheet="Sheet1")
    G.add_node("Dest", sheet="Sheet2")
    G.add_edge("Src", "Dest")

    print_summary(G, {"SUM": 5, "AVERAGE": 3})
    assert True


# can handle empty graph
def test_empty_graph():
    # Test that the function runs without errors
    G = nx.DiGraph()
    print_summary(G, {"SUM": 5, "AVERAGE": 3})
    assert True


# can handle empty functionsdict
def test_empty_functionsdict():
    # Test that the function runs without errors
    G = nx.DiGraph()
    G.add_node("Src", sheet="Sheet1")
    G.add_node("Dest", sheet="Sheet2")
    G.add_edge("Src", "Dest")

    print_summary(G, {})
    assert True
