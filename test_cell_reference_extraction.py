from excel_parser import (
    extract_references,
    expand_range,
)  # Ensure you replace this with the actual name of your module


# def test_expand_range():
#     formula = "=Sum(A1:A3)"
#     expected_references = ["A1", "A2", "A3"]
#     direct_references, deps = extract_references(formula)
#     assert (
#         direct_references == expected_references
#     ), f"Expected {expected_references}, but got {direct_references}"


# def test_expand_range_other_sheet():
#     formula = "=Sum(Other!A1:A3)"
#     expected_references = ["Other!A1", "Other!A2", "Other!A3"]
#     direct_references, deps = extract_references(formula)
#     assert (
#         direct_references == expected_references
#     ), f"Expected {expected_references}, but got {direct_references}"


# # Test for simple references like B4, A5
def test_simple_references():
    formula = "=B4+A5"
    expected_references = ["B4", "A5"]
    direct_references, range_references, deps = extract_references(formula)
    assert (
        direct_references == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# # Test for local range references like A2:A11
def test_local_range_references():
    formula = "=SUM(A2:A4)"
    expected_references = ["A2:A4"]
    direct_references, range_refs, deps = extract_references(formula)
    assert (
        range_refs == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# Test for simple absolute references like $A$1, $B$2
def test_absolute_references():
    formula = "=$A$1+$B$2"
    expected_references = ["A1", "B2"]
    direct_references, range_refs, deps = extract_references(formula)
    assert (
        direct_references == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# Test for sheet qualified absolute references like Sheet2!$A$1, Sheet2!$B$2
def test_sheet_qualified_absolute_references():
    formula = "=Sheet2!$A$1+Sheet2!$B$2"
    expected_references = ["Sheet2!A1", "Sheet2!B2"]
    direct_references, range_refs, deps = extract_references(formula)
    assert (
        direct_references == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# Test for sheet-qualified absolute range references like Sheet2!$A$1:$A$10
def test_sheet_qualified_absolute_range_references():
    formula = "=SUM(Sheet2!$A$2:$A$5)"
    expected_references = [
        "Sheet2!A2:A5",
    ]
    direct_references, range_refs, deps = extract_references(formula)
    assert (
        range_refs == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# Test for sheet-qualified cell like Sheet2!C5
def test_sheet_qualified_reference():
    formula = "=Sheet2!C5"
    expected_references = ["Sheet2!C5"]
    direct_references, rr, deps = extract_references(formula)
    assert (
        direct_references == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


def test_expanded_range_in_dependencies():
    formula = "=SUM(A1:A3)"
    expected_references = ["A1", "A2", "A3"]
    direct_references, range_refs, deps = extract_references(formula)
    assert deps == {
        "A1": "A1:A3",
        "A2": "A1:A3",
        "A3": "A1:A3",
    }, f"Expected {expected_references}, but got {deps}"


def test_no_direct_but_only_range_references():
    formula = "=SUM(A1:A3)"
    direct_references, range_refs, deps = extract_references(formula)
    assert (
        direct_references == []
    ), f"Expected no direct references, but got {direct_references}"


def test_two_ranges():
    formula = "=SUM(A1:A3) + SUM(B1:B3)"
    direct_references, range_refs, deps = extract_references(formula)
    assert range_refs == [
        "A1:A3",
        "B1:B3",
    ], f"Expected ['A1:A3', 'B1:B3'], but got {range_refs}"


# Test for sheet-qualified range like Sheet2!A1:B10
def test_sheet_qualified_range():
    formula = "=SUM(Sheet2!A1:B3)"
    expected_references = [
        "Sheet2!A1:B3",
    ]
    direct_references, rr, deps = extract_references(formula)
    assert (
        rr == expected_references
    ), f"Expected {expected_references}, but got {direct_references}"


# # Test for mixed references with both local and sheet-qualified cells
# def test_mixed_references():
#     formula = "=SUM(Sheet2!A1:B3, A5) + Sheet2!C5 + B6"
#     expected_references = [
#         "Sheet2!A1",
#         "Sheet2!B1",
#         "Sheet2!A2",
#         "Sheet2!B2",
#         "Sheet2!A3",
#         "Sheet2!B3",
#         "A5",
#         "Sheet2!C5",
#         "B6",
#     ]
#     direct_references, deps = extract_references(formula)
#     assert (
#         direct_references == expected_references
#     ), f"Expected {expected_references}, but got {direct_references}"


# # Test for sheet-qualified ranges and mix of cell references
# def test_mixed_ranges_and_cells():
#     formula = "=A1+Sheet1!B1+B10+SUM(Sheet2!A1:A3)"
#     expected_references = [
#         "A1",
#         "Sheet1!B1",
#         "B10",
#         "Sheet2!A1",
#         "Sheet2!A2",
#         "Sheet2!A3",
#     ]
#     direct_references, deps = extract_references(formula)
#     assert (
#         direct_references == expected_references
#     ), f"Expected {expected_references}, but got {direct_references}"
