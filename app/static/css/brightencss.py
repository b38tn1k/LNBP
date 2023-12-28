import re

def expand_shorthand_hex(hex_color):
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def lighten_color(hex_color, percentage):
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
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}|rgba?\(\s*(?:\d+%?\s*,\s*){2,3}\d*\.?\d+\s*(?:,\s*\d*\.?\d+\s*)?\)'

    with open(input_file_path, 'r') as file:
        css_content = file.read()

    def replace_color(match):
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
