def combine_python_files(file_list, output_file):
    """
    Combines multiple Python files into a single file with comments indicating
    the start and end of each original file.

    Parameters:
    - file_list: List of Python file names to combine.
    - output_file: Name of the output file.
    """
    with open(output_file, "w") as outfile:
        for fname in file_list:
            # Add a comment indicating the start of a file
            outfile.write(f"# --- Start of {fname} ---\n\n")
            with open(fname, "r") as infile:
                outfile.write(infile.read())
                outfile.write("\n")
            # Add a comment indicating the end of a file
            outfile.write(f"# --- End of {fname} ---\n\n")
    print(f"All files have been combined into {output_file}")


if __name__ == "__main__":
    # Replace these with your actual file names
    python_files = [
        "src/graphedexcel/__main__.py",
        "src/graphedexcel/graphbuilder.py",
        "src/graphedexcel/graph_visualizer.py",
        "src/graphedexcel/graph_summarizer.py",
        "src/graphedexcel/excel_parser.py",
    ]
    output_filename = "combined_project.py"
    combine_python_files(python_files, output_filename)
