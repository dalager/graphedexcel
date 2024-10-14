import os


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

    # List of Python files to combine, all .py files in the src/graphedexcel directory, not subdirectories
    python_files = [
        f"src/graphedexcel/{f}"
        for f in os.listdir("src/graphedexcel")
        if f.endswith(".py")
    ]

    output_filename = "combined_project.py"
    combine_python_files(python_files, output_filename)
