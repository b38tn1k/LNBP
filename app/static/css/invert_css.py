import re

def expand_shorthand_hex(hex_color):
    # Expand shorthand hex (#abc -> #aabbcc)
    """
    This function takes a hex color as an input and expands shorthand hex codes
    (#abc) to the full 6-digit hex code (#aabbcc).

    Args:
        hex_color (str): In this function `hex_color` is a string parameter that
            represents a hexadecimal color code.

    Returns:
        str: The output returned by this function is the expanded hexadecimal color
        code.

    """
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def invert_color(hex_color):
    """
    This function takes a hex color string as input and returns the inverted color
    as a hex string. It converts the hex color to RGB values and then computes the
    inverted RGB values by subtracting 255 from each component.

    Args:
        hex_color (str): The `hex_color` input parameter is a string representing
            a hexadecimal color code.

    Returns:
        str: The output returned by this function is a hex string representing the
        inverted RGB values of the original hex color.

    """
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
    """
    This function takes two path parameters: `input_file_path` and `output_file_path`.
    It reads the contents of the input CSS file and replaces all hex color codes
    (#[0-9a-fA-F]{3|6}) with their inverted colors using a given replace function.

    Args:
        input_file_path (str): The `input_file_path` parameter specifies the path
            to the CSS file that contains the colors to be inverted.
        output_file_path (str): The `output_file_path` input parameter is the path
            to the output file where the inverted CSS content will be written.

    """
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Read the input CSS file
    with open(input_file_path, 'r') as file:
        css_content = file.read()

    # Function to replace each color with its inverted color
    def replace_color(match):
        """
        The provided function `replace_color` takes a `match` object as input and
        returns an inverted version of the color mentioned inside the match.

        Args:
            match (): The `match` input parameter is a pattern match object that
                contains information about the portion of the string that matched
                the pattern.

        Returns:
            str: The function `replace_color` takes a string as input and replaces
            any occurrence of a color with its inverse color. Since the function
            does not specify what colors it can match or how it should replace
            them., the function's output cannot be determined concisely.

        """
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
