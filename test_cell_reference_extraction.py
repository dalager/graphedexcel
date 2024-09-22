from excel_parser import (
    extract_references,
    expand_range,
)  # Ensure you replace this with the actual name of your module


def test_expand_range():
    formula = "=Sum(A1:A3)"
    expected_references = ["A1", "A2", "A3"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


def test_expand_range_other_sheet():
    formula = "=Sum(Other!A1:A3)"
    expected_references = ["Other!A1", "Other!A2", "Other!A3"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for simple references like B4, A5
def test_simple_references():
    formula = "=B4+A5"
    expected_references = ["B4", "A5"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for local range references like A2:A11
def test_local_range_references():
    formula = "=SUM(A2:A11)"
    expected_references = ["A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for simple absolute references like $A$1, $B$2
def test_absolute_references():
    formula = "=$A$1+$B$2"
    expected_references = ["A1", "B2"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet qualified absolute references like Sheet2!$A$1, Sheet2!$B$2
def test_sheet_qualified_absolute_references():
    formula = "=Sheet2!$A$1+Sheet2!$B$2"
    expected_references = ["Sheet2!A1", "Sheet2!B2"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified absolute range references like Sheet2!$A$1:$A$10
def test_sheet_qualified_absolute_range_references():
    formula = "=SUM(Sheet2!$A$1:$A$10)"
    expected_references = [
        "Sheet2!A1",
        "Sheet2!A2",
        "Sheet2!A3",
        "Sheet2!A4",
        "Sheet2!A5",
        "Sheet2!A6",
        "Sheet2!A7",
        "Sheet2!A8",
        "Sheet2!A9",
        "Sheet2!A10",
    ]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified cell like Sheet2!C5
def test_sheet_qualified_reference():
    formula = "=Sheet2!C5"
    expected_references = ["Sheet2!C5"]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified range like Sheet2!A1:B10
def test_sheet_qualified_range():
    formula = "=SUM(Sheet2!A1:B3)"
    expected_references = [
        "Sheet2!A1",
        "Sheet2!B1",
        "Sheet2!A2",
        "Sheet2!B2",
        "Sheet2!A3",
        "Sheet2!B3",
    ]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for mixed references with both local and sheet-qualified cells
def test_mixed_references():
    formula = "=SUM(Sheet2!A1:B3, A5) + Sheet2!C5 + B6"
    expected_references = [
        "Sheet2!A1",
        "Sheet2!B1",
        "Sheet2!A2",
        "Sheet2!B2",
        "Sheet2!A3",
        "Sheet2!B3",
        "A5",
        "Sheet2!C5",
        "B6",
    ]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"


# Test for sheet-qualified ranges and mix of cell references
def test_mixed_ranges_and_cells():
    formula = "=A1+Sheet1!B1+B10+SUM(Sheet2!A1:A3)"
    expected_references = [
        "A1",
        "Sheet1!B1",
        "B10",
        "Sheet2!A1",
        "Sheet2!A2",
        "Sheet2!A3",
    ]
    actual_references, deps = extract_references(formula)
    assert (
        actual_references == expected_references
    ), f"Expected {expected_references}, but got {actual_references}"
