import re

def extract_colors_from_css(css_content):
    # Regular expression for matching hex and RGBA color codes
    """
    This function extracts all unique colors from CSS content using regular
    expressions to match hex and RGBA color codes.

    Args:
        css_content (str): The `css_content` input parameter is the CSS content
            that contains color codes that are to be extracted.

    Returns:
        list: The output returned by this function is a list of unique colors found
        In the given CSS content.

    """
    color_pattern = r'#[0-9a-fA-F]{3,6}|rgba?\(\s*(?:\d+%?\s*,\s*){2,3}\d*\.?\d+\s*(?:,\s*\d*\.?\d+\s*)?\)'

    # Find all occurrences of color codes in the CSS content
    colors = re.findall(color_pattern, css_content)

    # Remove duplicates by converting to a set and back to a list
    unique_colors = list(set(colors))

    return unique_colors

def read_css_file(file_path):
    """
    The function `read_css_file(file_path)` opens the file at the specified path
    `file_path` and reads its contents into a string.

    Args:
        file_path (str): The `file_path` input parameter is the path to the CSS
            file to be read.

    Returns:
        str: The output returned by this function is the contents of the given CSS
        file.

    """
    with open(file_path, 'r') as file:
        return file.read()

# Replace this with the path to your CSS file
css_file_path = 'rawcdn_github_backup.css'

# Read the CSS file
css_content = read_css_file(css_file_path)

# Extract unique colors
unique_colors = extract_colors_from_css(css_content)

# Print the extracted colors
for color in unique_colors:
    print(color)
