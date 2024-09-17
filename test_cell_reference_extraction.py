import pytest
from graphbuilder import (
    extract_references,
)  # Ensure you replace this with the actual name of your module


# Test for simple references like B4, A5
def test_simple_references():
    formula = "=B4+A5"
    expected_references = ["B4", "A5"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for local range references like A2:A11
def test_local_range_references():
    formula = "=SUM(A2:A11)"
    expected_references = ["A2:A11"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified cell like Sheet2!C5
def test_sheet_qualified_reference():
    formula = "=Sheet2!C5"
    expected_references = ["Sheet2!C5"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified range like Sheet2!A1:B10
def test_sheet_qualified_range():
    formula = "=SUM(Sheet2!A1:B10)"
    expected_references = ["Sheet2!A1:B10"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for mixed references with both local and sheet-qualified cells
def test_mixed_references():
    formula = "=SUM(Sheet2!A1:B10, A5) + Sheet2!C5 + B6"
    expected_references = ["Sheet2!A1:B10", "A5", "Sheet2!C5", "B6"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified ranges and mix of cell references
def test_mixed_ranges_and_cells():
    formula = "=A1+Sheet1!B1+B10+SUM(Sheet2!A1:A5)"
    expected_references = ["A1", "Sheet1!B1", "B10", "Sheet2!A1:A5"]
    actual_references = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"
