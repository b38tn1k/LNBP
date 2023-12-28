import re

def expand_shorthand_hex(hex_color):
    # Expand shorthand hex (#abc -> #aabbcc)
    """
    This function takes a string representing a hex color (with or without the "#"
    symbol) and expands any shorthand notation (such as "#abc" becoming "#aabbcc").

    Args:
        hex_color (str): The `hex_color` input parameter is a string that represents
            a hexadecimal color value.

    Returns:
        str: The output returned by this function is:
        
        #abc -> #aabbcc

    """
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def adjust_brightness(hex_color, coefficient=0.7):
    """
    This function takes a hex color code as an input and adjusts the brightness
    of the color by multiplying each component (redgreenblue) with a coefficient
    (default = 0.7), clamping the result to [0..255], and returning the adjusted
    color as a new hex code.

    Args:
        hex_color (str): The `hex_color` input parameter is a string representation
            of a color using hexadecimal notation (e.g., "#RGB").
        coefficient (float): The `coefficient` input parameter controls the amount
            of brightness adjustment applied to the color.

    Returns:
        str: The output returned by this function is a new hexadecimal color code
        representing the adjusted brightness of the input hex code.

    """
    hex_color = expand_shorthand_hex(hex_color)
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Adjust brightness
    adjusted_rgb = tuple(max(0, min(int(x * coefficient), 255)) for x in rgb)

    # Convert back to hex
    adjusted_hex = '#{:02x}{:02x}{:02x}'.format(*adjusted_rgb)
    return adjusted_hex

def adjust_colors_brightness_in_css_file(input_file_path, output_file_path):
    # Regular expression for matching hex color codes
    """
    This function takes two file paths as inputs and adjusts the brightness of hex
    color codes found within the CSS content of the input file.

    Args:
        input_file_path (str): The `input_file_path` parameter is the path to the
            CSS file that contains the hex color codes to be adjusted.
        output_file_path (str): The `output_file_path` parameter specifies the
            path to the output file where the adjusted CSS content will be written.

    """
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Read the input CSS file
    with open(input_file_path, 'r') as file:
        css_content = file.read()

    # Function to replace each color with its adjusted brightness color
    def replace_color(match):
        """
        This function takes a string and replaces any color mentions (i.e., words
        or phrases that refer to colors) with the same color but with an adjusted
        brightness.

        Args:
            match (): In this function `replace_color`, the `match` input parameter
                is a Match Object returned by the regular expression engine when
                it matches a pattern.

        Returns:
            str: The function `replace_color` takes a string `match` as input and
            returns the same string with the color portion replaced by the adjusted
            brightness of that color.
            
            So the output returned by this function will be the original string
            with the colors adjusted.

        """
        color = match.group(0)
        return adjust_brightness(color)

    # Replace all color occurrences in the CSS content
    adjusted_css_content = re.sub(hex_color_pattern, replace_color, css_content)

    # Write the adjusted CSS content to the output file
    with open(output_file_path, 'w') as file:
        file.write(adjusted_css_content)

# Example usage
input_css_path = 'custom_tabler.css'  # Replace with your CSS file path
output_css_path = 'custom_tabler_dark.css'  # Replace with your desired output path

adjust_colors_brightness_in_css_file(input_css_path, output_css_path)

