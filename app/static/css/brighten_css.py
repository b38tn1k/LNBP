import re

def expand_shorthand_hex(hex_color):
    """
    This function takes a hex color string (e.g. "#FF0000") and expands any shorthand
    syntax (e.g. "#FF" instead of "#FFFFFF") to the full hexadecimal representation
    (i.e.

    Args:
        hex_color (str): The `hex_color` input parameter is the string of the form
            `#HHCCBBGGGOBBRR` that the function takes as input and processes to
            return an expanded version of the shorthand hex code.

    Returns:
        str: The output returned by the function is the expanded version of the
        hex color string.
        For example:
        
        expand_shorthand_hex('#ff5733') --> '#ff573333333'

    """
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def lighten_color(hex_color, percentage):
    """
    This function takes a hexadecimal string representing a color and a percentage
    value as input.

    Args:
        hex_color (str): The `hex_color` input parameter is the color that should
            be lightened.
        percentage (float): The `percentage` input parameter specifies how much
            to lighten the color by. It takes a value between 0 and 100 as a
            percentage of the original color to brighten.

    Returns:
        str: The output returned by this function is a string representing the
        brightened color as an ASCII hexadecimal RGB color code.

    """
    hex_color = expand_shorthand_hex(hex_color)
    if hex_color.startswith('#'):
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Brighten RGB colors
        brightened_rgb = tuple(min(255, int(x + (255 - x) * percentage / 100)) for x in rgb)

        # Convert back to hex
        brightened_hex = '#{:02x}{:02x}{:02x}'.format(*brightened_rgb)
        return brightened_hex
    elif hex_color.startswith('rgba'):
        rgba_pattern = r'rgba\((\d+%?),\s*(\d+%?),\s*(\d+%?),\s*([\d.]+)\)'
        match = re.match(rgba_pattern, hex_color)
        if match:
            r, g, b, alpha = match.groups()
            r, g, b = int(r), int(g), int(b)
            alpha = float(alpha)

            # Brighten RGBA colors while keeping the alpha channel
            brightened_rgb = tuple(min(255, int(x + (255 - x) * percentage / 100)) for x in (r, g, b))
            brightened_hex = 'rgba({}, {}, {}, {})'.format(*brightened_rgb, alpha)
            return brightened_hex

    # If the input color format is not recognized, return it unchanged
    return hex_color

def brighten_colors_in_css_file(input_file_path, output_file_path, percentage):
    """
    This function takes an input CSS file path and output file path and a percentage
    value as arguments and it replaces all the hexadecimal colors present  within
    the given input CSS file with the brightened version of the color by lightening
    them by the specified percentage value and then saves the modified CSS content
    to the output file.

    Args:
        input_file_path (str): The `input_file_path` parameter is the path to the
            CSS file that contains the colors to be brightened.
        output_file_path (str): The `output_file_path` parameter is the path to
            the output file where the brightened CSS content will be written.
        percentage (float): The `percentage` input parameter controls how much
            brighter the colors should be.

    """
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}|rgba?\(\s*(?:\d+%?\s*,\s*){2,3}\d*\.?\d+\s*(?:,\s*\d*\.?\d+\s*)?\)'

    with open(input_file_path, 'r') as file:
        css_content = file.read()

    def replace_color(match):
        """
        This function takes a string `match` and replaces any occurrences of a
        color (represented as a string) with the same color lightened by a certain
        percentage.

        Args:
            match (): In this function `replace_color`, `match` is a Pattern object
                that represents the portion of the text where the color should be
                replaced.

        Returns:
            str: The output returned by the `replace_color` function is a lightened
            version of the input color.

        """
        color = match.group(0)
        return lighten_color(color, percentage)

    brightened_css_content = re.sub(hex_color_pattern, replace_color, css_content)

    with open(output_file_path, 'w') as file:
        file.write(brightened_css_content)

# Example usage
input_css_path = 'rawcdn_github_backup_inv.css'  # Replace with your CSS file path
output_css_path = 'rawcdn_github_backup_inv_brightened.css'  # Replace with your desired output path
percentage_to_brighten = 20  # Adjust the percentage as needed

brighten_colors_in_css_file(input_css_path, output_css_path, percentage_to_brighten)
