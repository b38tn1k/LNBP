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
    color_map = {}
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Extract colors and calculate brightness
    def extract_color(match):
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
