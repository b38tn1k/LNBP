import os
import re
import requests
import wget

# Define the base URL for the CDN
cdn_base_url = "https://rawcdn.githack.com/Sumukh/Ignite/70bf953851a356e785528b56ca105042074a3d5a/appname/static/tabler/"

# Define the URL of the CSS file
css_url = "https://rawcdn.githack.com/Sumukh/Ignite/70bf953851a356e785528b56ca105042074a3d5a/appname/static/tabler/css/dashboard.css"

# Define the local directory to save the files
local_directory = "appname/static/"

# Create the local directory if it doesn't exist
if not os.path.exists(local_directory):
    os.makedirs(local_directory)

# Download the CSS file
response = requests.get(css_url)
if response.status_code == 200:
    css_content = response.text

    # Use regular expressions to find relative URLs in the CSS
    relative_urls = re.findall(r'url\(\s*"\.\./([^)]+)"\s*\)', css_content)

    for relative_url in relative_urls:
        # Construct the full URL for the asset
        asset_url = cdn_base_url + relative_url

        # Determine the local file path for the asset
        local_file_path = os.path.join(local_directory, relative_url)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Download the asset using wget
        try:
            wget.download(asset_url, local_file_path)
            print(f"Downloaded: {asset_url} to {local_file_path}")
        except Exception as e:
            print(f"Failed to download asset: {asset_url}, Error: {str(e)}")
    print("All assets downloaded successfully.")
else:
    print(f"Failed to download CSS file. Status code: {response.status_code}")
