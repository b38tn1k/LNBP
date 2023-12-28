import re
import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB."""
    hex_color = hex_color.lstrip('#')
    length = len(hex_color)
    return tuple(int(hex_color[i:i+length//3], 16) for i in range(0, length, length//3))

def rgb_to_hex(rgb_color):
    """Convert RGB color to hex."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def get_brightness(rgb_color):
    """Calculate brightness of an RGB color."""
    return sum(rgb_color) / (255 * 3)

def adjust_color_brightness(rgb_color, target_brightness):
    """Adjust the brightness of an RGB color to match the target_brightness."""
    hsv = colorsys.rgb_to_hsv(*rgb_color)
    adjusted_rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], target_brightness)
    return tuple(int(x*255) for x in adjusted_rgb)

def process_css_colors(css_content, max_brightness=0.7):
    """
    This function takes a CSS string as input and adjusts the colors present In
    the CSS to have a maximum brightness of 0.7. It extracts all colors found In
    the CSS using regular expressions and calculates their brightness levels based
    on their RGB values.

    Args:
        css_content (str): The `css_content` input parameter is the CSS content
            that contains the colors to be processed.
        max_brightness (float): The `max_brightness` parameter sets the maximum
            brightness level for adjusting the colors. It scales all brightness
            levels relative to the specified value. If `max_brightness` is 0.7 and
            a color's brightness level is 1.5 before adjustment (i.e., too bright),
            it will be adjusted down to 1.1 (1.5 x 0.7).

    Returns:
        str: The output returned by this function is a modified CSS content with
        adjusted color brightness levels.

    """
    color_map = {}
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Extract colors and calculate brightness
    def extract_color(match):
        """
        This function takes a match object as input and extracts the color hex
        code from it. It then converts the hex code to an RGB value and calculates
        the brightness of the color.

        Args:
            match (): The `match` input parameter is a regular expression match
                object and is used to extract the color hex code from the input string.

        Returns:
            str: The output returned by this function is the color hex string.

        """
        color_hex = match.group(0)
        rgb = hex_to_rgb(color_hex)
        brightness = get_brightness(rgb)
        color_map[color_hex] = rgb, brightness
        return color_hex

    re.sub(hex_color_pattern, extract_color, css_content)

    # Determine brightness levels
    sorted_colors = sorted(color_map.items(), key=lambda x: x[1][1], reverse=True)
    highest_brightness = sorted_colors[0][1][1] * max_brightness
    brightness_levels = [highest_brightness * (i/len(sorted_colors)) for i in range(len(sorted_colors))]

    # Adjust colors
    for i, (color_hex, (rgb, _)) in enumerate(sorted_colors):
        adjusted_rgb = adjust_color_brightness(rgb, brightness_levels[i])
        color_map[color_hex] = rgb_to_hex(adjusted_rgb)

    # Replace old colors with new colors in CSS
    def replace_color(match):
        """
        This function takes a substring that represents a color (e.g.

        Args:
            match (): In the function `replace_color`, the `match` parameter is a
                tuple containing the matching text and its position info from the
                last pattern match done by the `re` module.

        Returns:
            str: The output returned by the function `replace_color` is the input
            string with all occurrences of the old color replaced with the
            corresponding new color from the `color_map`.

        """
        old_color = match.group(0)
        return color_map.get(old_color, old_color)

    return re.sub(hex_color_pattern, replace_color, css_content)

# Example usage
input_css_path = 'custom_tabler.css'  # Replace with your CSS file path
output_css_path = 'custom_tabler_darkened.css'  # Replace with your desired output path

with open(input_css_path, 'r') as file:
    css_content = file.read()

adjusted_css_content = process_css_colors(css_content)

with open(output_css_path, 'w') as file:
    file.write(adjusted_css_content)
