import re

def expand_shorthand_hex(hex_color):
    # Expand shorthand hex (#abc -> #aabbcc)
    """
    This function takes a single argument `hex_color` which is a string representing
    a hexadecimal color code.

    Args:
        hex_color (str): In the `expand_shorthand_hex` function above `hex_color`
            is passed as an argument and its value is an input string that represents
            a shorthand hexadecimal color code of maximum length 4 ( consisting
            of three hexadecimal digits and the "#" character followed by 1 or
            more additional hexadecimal digits up to a total of 8.
            So `hex_color` carries information representing the shorthand hexadecimal
            code to be expanded and processed.

    Returns:
        str: The output returned by this function is the expanded version of a
        given hex color.

    """
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def invert_color(hex_color):
    """
    This function takes a hex string representing a color and returns the inverted
    color.

    Args:
        hex_color (str): The `hex_color` input parameter is a string representing
            a color using either a hexadecimal (#yyyzzz) or RGBA (rgba(rrggbbaa))
            format.

    Returns:
        str: The output returned by this function is a hexadecimal string representing
        an inverted version of the original color.

    """
    hex_color = expand_shorthand_hex(hex_color)
    if hex_color.startswith('#'):
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Invert RGB colors
        inverted_rgb = tuple(255 - x for x in rgb)

        # Convert back to hex
        inverted_hex = '#{:02x}{:02x}{:02x}'.format(*inverted_rgb)
        return inverted_hex
    elif hex_color.startswith('rgba'):
        rgba_pattern = r'rgba\((\d+%?),\s*(\d+%?),\s*(\d+%?),\s*([\d.]+)\)'
        match = re.match(rgba_pattern, hex_color)
        if match:
            r, g, b, alpha = match.groups()
            r, g, b = int(r), int(g), int(b)
            alpha = float(alpha)

            # Invert RGBA colors while keeping the alpha channel
            inverted_rgb = tuple(255 - x for x in (r, g, b))
            inverted_hex = 'rgba({}, {}, {}, {})'.format(*inverted_rgb, alpha)
            return inverted_hex

    # If the input color format is not recognized, return it unchanged
    return hex_color

def invert_colors_in_css_file(input_file_path, output_file_path):
    """
    This function takes two file paths as input and returns the contents of the
    input CSS file with all hex colors inverted (i.e., their value is subtracted
    from 255).

    Args:
        input_file_path (str): The `input_file_path` input parameter is the path
            to the CSS file that contains the colors to be inverted.
        output_file_path (str): The `output_file_path` input parameter specifies
            the path to the output file where the inverted CSS content will be written.

    """
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}|rgba?\(\s*(?:\d+%?\s*,\s*){2,3}\d*\.?\d+\s*(?:,\s*\d*\.?\d+\s*)?\)'

    with open(input_file_path, 'r') as file:
        css_content = file.read()

    def replace_color(match):
        """
        This function replaces a color (represented as a string) with its inverse
        color.

        Args:
            match (): The `match` input parameter is a regular expression match
                object that contains the matched substring and information about
                the match.

        Returns:
            str: The output returned by this function is "inverted" version of the
            input color.

        """
        color = match.group(0)
        return invert_color(color)

    inverted_css_content = re.sub(hex_color_pattern, replace_color, css_content)

    with open(output_file_path, 'w') as file:
        file.write(inverted_css_content)

# Example usage
input_css_path = 'rawcdn_github_backup.css'  # Replace with your CSS file path
output_css_path = 'rawcdn_github_backup_inv.css'  # Replace with your desired output path

invert_colors_in_css_file(input_css_path, output_css_path)
