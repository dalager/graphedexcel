from openpyxl.utils import get_column_letter, range_boundaries
import re
from typing import List, Tuple, Dict

# Regex to detect cell references like A1, B2, or ranges like A1:B2
CELL_REF_REGEX = r"('?[A-Za-z0-9_\-\[\] ]+'?![A-Z]{1,3}[0-9]+(:[A-Z]{1,3}[0-9]+)?)|([A-Z]{1,3}[0-9]+(:[A-Z]{1,3}[0-9]+)?)"  # noqa

def extract_references(formula: str) -> Tuple[List[str], List[str], Dict[str, str]]:
    """
    Extract all referenced cells and ranges from a formula using regular expressions.
    This returns a list of both individual cells and range references.

    Args:
        formula (str): The formula to extract references from.

    Returns:
        Tuple[List[str], List[str], Dict[str, str]]: A tuple containing lists of direct references,
                                                     range references, and a dictionary of dependencies.
    """
    formula = formula.replace("$", "")
    matches = re.findall(CELL_REF_REGEX, formula)
    references = [match[0] if match[0] else match[2] for match in matches]

    # Trim the extracted references
    references = [ref.strip() for ref in references]

    expanded_references = []
    dependencies = {}
    direct_references = []
    range_references = []

    for reference in references:
        if ":" in reference:  # it's a range like A1:A3
            expanded_cells = expand_range(reference)
            expanded_references.extend(expanded_cells)
            range_references.append(reference)
            # Store the range-to-cells relationship
            for cell in expanded_cells:
                dependencies[cell] = reference
        else:  # single cell
            direct_references.append(reference)

    return direct_references, range_references, dependencies

def expand_range(range_reference: str) -> List[str]:
    """
    Expand a range reference (e.g., 'A1:A3') into a list of individual cell references.

    Args:
        range_ref (str): The range reference to expand.

    Returns:
        List[str]: A list of individual cell references.
    """
    # if there is a sheet name in the range reference, put it away for now
    if "!" in range_reference:
        sheet_name, range_reference = range_reference.split("!")
    else:
        sheet_name = None

    min_col, min_row, max_col, max_row = range_boundaries(range_reference)
    expanded_cells = []

    # Loop over rows and columns in the range
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            cell_ref = f"{get_column_letter(col)}{row}"
            if sheet_name:
                expanded_cells.append(f"{sheet_name}!{cell_ref}")
            else:
                expanded_cells.append(cell_ref)

    return expanded_cells


