import pytest
from src.graphedexcel.excel_parser import extract_references


# Helper function to assert references
def assert_references(formula, expected_direct, expected_range, expected_deps):
    direct_references, range_references, deps = extract_references(formula)
    assert (
        direct_references == expected_direct
    ), f"Expected {expected_direct}, but got {direct_references}"
    assert (
        range_references == expected_range
    ), f"Expected {expected_range}, but got {range_references}"
    assert deps == expected_deps, f"Expected {expected_deps}, but got {deps}"


@pytest.mark.parametrize(
    "formula, expected_direct, expected_range, expected_deps",
    [
        # Test for simple references like B4, A5
        ("=B4+A5", ["B4", "A5"], [], {}),
        # Test for local range references like A2:A11
        ("=SUM(A2:A4)", [], ["A2:A4"], {"A2": "A2:A4", "A3": "A2:A4", "A4": "A2:A4"}),
        # Test for simple absolute references like $A$1, $B$2
        ("=$A$1+$B$2", ["A1", "B2"], [], {}),
        # Test for sheet qualified absolute references like Sheet2!$A$1, Sheet2!$B$2
        ("=Sheet2!$A$1+Sheet2!$B$2", ["Sheet2!A1", "Sheet2!B2"], [], {}),
    ],
)
def test_references(formula, expected_direct, expected_range, expected_deps):
    """
    Test various cell and range references.
    """
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for sheet-qualified absolute range references like Sheet2!$A$1:$A$10
def test_sheet_qualified_absolute_range_references():
    """
    Test for sheet-qualified absolute range references like Sheet2!$A$2:$A$5.
    """
    formula = "=SUM(Sheet2!$A$2:$A$5)"
    expected_direct = []
    expected_range = ["Sheet2!A2:A5"]
    expected_deps = {
        "Sheet2!A2": "Sheet2!A2:A5",
        "Sheet2!A3": "Sheet2!A2:A5",
        "Sheet2!A4": "Sheet2!A2:A5",
        "Sheet2!A5": "Sheet2!A2:A5",
    }
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for sheet-qualified cell like Sheet2!C5
def test_sheet_qualified_reference():
    """
    Test for sheet-qualified cell like Sheet2!C5.
    """
    formula = "=Sheet2!C5"
    expected_direct = ["Sheet2!C5"]
    expected_range = []
    expected_deps = {}
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for expanded range in dependencies
def test_expanded_range_in_dependencies():
    """
    Test for expanded range in dependencies like A1:A3.
    """
    formula = "=SUM(A1:A3)"
    expected_direct = []
    expected_range = ["A1:A3"]
    expected_deps = {"A1": "A1:A3", "A2": "A1:A3", "A3": "A1:A3"}
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for no direct but only range references
def test_no_direct_but_only_range_references():
    """
    Test for no direct references but only range references like A1:A3.
    """
    formula = "=SUM(A1:A3)"
    expected_direct = []
    expected_range = ["A1:A3"]
    expected_deps = {"A1": "A1:A3", "A2": "A1:A3", "A3": "A1:A3"}
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for two ranges
def test_two_ranges():
    """
    Test for two ranges like A1:A3 and B1:B3.
    """
    formula = "=SUM(A1:A3) + SUM(B1:B3)"
    expected_direct = []
    expected_range = ["A1:A3", "B1:B3"]
    expected_deps = {
        "A1": "A1:A3",
        "A2": "A1:A3",
        "A3": "A1:A3",
        "B1": "B1:B3",
        "B2": "B1:B3",
        "B3": "B1:B3",
    }
    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for sheet-qualified range like Sheet2!A1:B10
def test_sheet_qualified_range():
    """
    Test for sheet-qualified range like Sheet2!A1:B3.
    """
    formula = "=SUM(Sheet2!A1:B3)"
    expected_direct = []
    expected_range = ["Sheet2!A1:B3"]

    expected_deps = {
        "Sheet2!A1": "Sheet2!A1:B3",
        "Sheet2!A2": "Sheet2!A1:B3",
        "Sheet2!A3": "Sheet2!A1:B3",
        "Sheet2!B1": "Sheet2!A1:B3",
        "Sheet2!B2": "Sheet2!A1:B3",
        "Sheet2!B3": "Sheet2!A1:B3",
    }

    assert_references(formula, expected_direct, expected_range, expected_deps)


# Test for mixed references with both local and sheet-qualified cells
def test_mixed_references():
    """
    Test for mixed references with both local and sheet-qualified cells.
    """
    formula = "=SUM(Sheet2!A1:B3, A5) + Sheet2!C5 + B6"
    expected_direct = ["A5", "Sheet2!C5", "B6"]
    expected_range = ["Sheet2!A1:B3"]
    expected_deps = {
        "Sheet2!A1": "Sheet2!A1:B3",
        "Sheet2!A2": "Sheet2!A1:B3",
        "Sheet2!A3": "Sheet2!A1:B3",
        "Sheet2!B1": "Sheet2!A1:B3",
        "Sheet2!B2": "Sheet2!A1:B3",
        "Sheet2!B3": "Sheet2!A1:B3",
    }
    assert_references(formula, expected_direct, expected_range, expected_deps)
