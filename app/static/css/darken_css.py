import re

def expand_shorthand_hex(hex_color):
    # Expand shorthand hex (#abc -> #aabbcc)
    if len(hex_color) == 4:  # 3 hex digits plus '#'
        return '#' + ''.join([c*2 for c in hex_color[1:]])
    return hex_color

def adjust_brightness(hex_color, coefficient=0.7):
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
    hex_color_pattern = r'#[0-9a-fA-F]{3,6}'

    # Read the input CSS file
    with open(input_file_path, 'r') as file:
        css_content = file.read()

    # Function to replace each color with its adjusted brightness color
    def replace_color(match):
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

