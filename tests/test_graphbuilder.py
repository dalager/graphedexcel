from openpyxl import Workbook
import pytest

# from unittest import mock
import networkx as nx

# Import the functions and variables from your module
from graphedexcel.graphbuilder import (
    sanitize_sheetname,
    sanitize_range,
    stat_functions,
    add_node,
    build_graph_and_stats,
    functions_dict,
)
from graphedexcel.graphbuilder import sanitize_nodename


@pytest.fixture(autouse=True)
def reset_functions_dict():
    """
    Fixture to reset the global functions_dict before each test.
    """
    functions_dict.clear()


def test_sanitize_nodename():
    """
    Test the sanitize node name
    """

    assert sanitize_nodename("Sheet1!A1") == "Sheet1!A1"
    assert sanitize_nodename("Sheet'2!B1") == "Sheet2!B1"
    assert sanitize_nodename("Sheet'3!C1") == "Sheet3!C1"


def test_sanitize_sheetname():
    """
    Test the sanitize_sheetname function to ensure it removes single quotes.
    """
    assert sanitize_sheetname("Sheet1") == "Sheet1"
    assert sanitize_sheetname("Sheet'1") == "Sheet1"
    assert sanitize_sheetname("O'Brien") == "OBrien"
    assert sanitize_sheetname("Data!1") == "Data!1"  # Only removes single quotes


def test_sanitize_range():
    """
    Test the sanitize_range function to ensure it
    removes single quotes and handles sheet delimiters.
    """
    assert sanitize_range("Sheet1!A1:B2") == "Sheet1!A1:B2"
    assert sanitize_range("'Sheet1'!A1:B2") == "Sheet1!A1:B2"
    assert sanitize_range("A1:B2") == "A1:B2"
    assert sanitize_range("'Data Sheet'!C3") == "Data Sheet!C3"


def test_stat_functions():
    """
    Test the stat_functions function to ensure it correctly
    parses function names and updates functions_dict.
    """
    stat_functions("=SUM(A1:A10)")
    assert functions_dict.get("SUM") == 1

    stat_functions("=AVERAGE(B1:B5)")
    assert functions_dict.get("AVERAGE") == 1

    stat_functions("=SUM(A1:A10) + SUM(B1:B10)")
    assert functions_dict.get("SUM") == 3

    stat_functions("=IF(C1 > 0, SUM(D1:D10), 0)")
    assert functions_dict.get("IF") == 1
    assert functions_dict.get("SUM") == 4  # SUM incremented again


def test_add_node():
    """
    Test the add_node function to ensure nodes are added with
    correct attributes and sheet names are sanitized.
    """
    graph = nx.DiGraph()
    add_node(graph, "Sheet1!A1", "Sheet1")
    add_node(graph, "Sheet1!B1", "Sheet1")
    add_node(graph, "Sheet2!A1", "Sheet2")

    assert graph.has_node("Sheet1!A1")
    assert graph.nodes["Sheet1!A1"]["sheet"] == "Sheet1"

    assert graph.has_node("Sheet1!B1")
    assert graph.nodes["Sheet1!B1"]["sheet"] == "Sheet1"

    assert graph.has_node("Sheet2!A1")
    assert graph.nodes["Sheet2!A1"]["sheet"] == "Sheet2"

    # Test sanitization
    add_node(graph, "Sheet'3!C1", "Sheet'3")

    assert graph.has_node("Sheet3!C1")
    assert graph.nodes["Sheet3!C1"]["sheet"] == "Sheet3"


@pytest.fixture
def create_excel_file(tmp_path):
    def _create_excel_file(data):
        file_path = tmp_path / "test.xlsx"
        wb = Workbook()
        for sheet_name, sheet_data in data.items():
            ws = wb.create_sheet(title=sheet_name)
            for row in sheet_data:
                ws.append(row)
        wb.save(file_path)
        return file_path

    return _create_excel_file


def test_build_graph_with_simple_formulas(create_excel_file):
    data = {
        "Sheet1": [
            ["41", "81", "71", "99"],
            ["=A1+B1", "=C1+D1"],
            ["=E1+F1", "=G1+H1"],
        ]
    }
    file_path = create_excel_file(data)
    graph, functions_dict = build_graph_and_stats(file_path)

    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 12
    assert len(graph.edges) == 8
    assert functions_dict == {}


def test_build_graph_with_range_references(create_excel_file):
    data = {
        "Sheet1": [
            ["=SUM(A1:A3)", "=SUM(B1:B3)"],
        ]
    }
    file_path = create_excel_file(data)
    graph, functions_dict = build_graph_and_stats(file_path)

    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 8
    assert len(graph.edges) == 6
    assert functions_dict == {"SUM": 2}


def test_self_loops_are_removed(create_excel_file):
    data = {"sheet1": [["=A1", "=B1"]]}
    file_path = create_excel_file(data)
    graph, functions_dict = build_graph_and_stats(file_path)
    selfloops = nx.selfloop_edges(graph)
    for loop in selfloops:
        print(loop)

    assert isinstance(graph, nx.Graph)
    assert len(graph.edges) == 0
    assert len(graph.nodes) == 0


def test_directed_graph(create_excel_file):
    data = {
        "Sheet1": [
            ["=B1", "=A1"],
        ]
    }
    file_path = create_excel_file(data)
    graph, functions_dict = build_graph_and_stats(file_path, as_directed=True)

    assert isinstance(graph, nx.DiGraph)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 2
    assert functions_dict == {}


def test_undirected_graph(create_excel_file):
    data = {
        "Sheet1": [
            ["=B1", "=A1"],
        ]
    }
    file_path = create_excel_file(data)
    graph, functions_dict = build_graph_and_stats(file_path, as_directed=False)

    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert functions_dict == {}
