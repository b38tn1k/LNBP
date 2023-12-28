import re

def expand_shorthand_hex(hex_color):
    # Expand shorthand hex (#abc -> #aabbcc)
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def invert_color(hex_color):
    hex_color = expand_shorthand_hex(hex_color)
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Invert RGB colors
    inverted_rgb = tuple(255 - x for x in rgb)

    # Convert back to hex
    inverted_hex = '#{:02x}{:02x}{:02x}'.format(*inverted_rgb)
    return inverted_hex

def invert_colors_in_css_file(input_file_path, output_file_path):
    # Regular expression for matching hex color codes
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Read the input CSS file
    with open(input_file_path, 'r') as file:
        css_content = file.read()

    # Function to replace each color with its inverted color
    def replace_color(match):
        color = match.group(0)
        return invert_color(color)

    # Replace all color occurrences in the CSS content
    inverted_css_content = re.sub(hex_color_pattern, replace_color, css_content)

    # Write the inverted CSS content to the output file
    with open(output_file_path, 'w') as file:
        file.write(inverted_css_content)

# Example usage
input_css_path = 'custom_tabler.css'  # Replace with your CSS file path
output_css_path = 'custom_tabler_dark.css'  # Replace with your desired output path

invert_colors_in_css_file(input_css_path, output_css_path)
