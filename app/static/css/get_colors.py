import re

def extract_colors_from_css(css_content):
    # Regular expression for matching hex color codes
    """
    This function takes CSS content as input and extracts all unique hex color
    codes from it using regular expressions.

    Args:
        css_content (str): The `css_content` input parameter is the CSS code that
            contains hex color codes that need to be extracted.

    Returns:
        list: The output returned by this function is a list of unique hex color
        codes found within the provided CSS content.

    """
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'
    
    # Find all occurrences of color codes in the CSS content
    colors = re.findall(hex_color_pattern, css_content)
    
    # Remove duplicates by converting to a set and back to a list
    unique_colors = list(set(colors))

    return unique_colors

def read_css_file(file_path):
    """
    This function reads the contents of a CSS file located at the specified `file_path`.

    Args:
        file_path (str): The `file_path` input parameter is the path to the CSS
            file that should be read.

    Returns:
        str: The function `read_css_file` reads the contents of a CSS file and
        returns the contents as a string.

    """
    with open(file_path, 'r') as file:
        return file.read()

# Replace this with the path to your CSS file
css_file_path = 'custom_tabler.css'

# Read the CSS file
css_content = read_css_file(css_file_path)

# Extract unique colors
unique_colors = extract_colors_from_css(css_content)

# Print the extracted colors
print(unique_colors)

