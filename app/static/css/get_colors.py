import re

def extract_colors_from_css(css_content):
    # Regular expression for matching hex and RGBA color codes
    color_pattern = r'#[0-9a-fA-F]{3,6}|rgba?\(\s*(?:\d+%?\s*,\s*){2,3}\d*\.?\d+\s*(?:,\s*\d*\.?\d+\s*)?\)'

    # Find all occurrences of color codes in the CSS content
    colors = re.findall(color_pattern, css_content)

    # Remove duplicates by converting to a set and back to a list
    unique_colors = list(set(colors))

    return unique_colors

def read_css_file(file_path):
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
