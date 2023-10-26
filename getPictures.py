import requests
import json
import os

q_value = "reflex camera back"

# Your existing code
res = requests.get(
    f"https://api.search.brave.com/res/v1/images/search?q={q_value}&safesearch=strict&count=100&search_lang=en&country=us&spellcheck=1",
    headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": "BSArCBHslQs8k4GSeCIT_GgG7hVOQIY",
    },
)

# Check if the initial API request was successful
if res.status_code != 200:
    print(f"Failed to get images from API: {res.status_code}")

    exit()

# Check if the response is valid JSON
try:
    res_data = res.json()
except json.JSONDecodeError:
    print("Failed to parse API response as JSON.")
    exit()

# Path to the desktop folder
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Search Images")

# Check if directory can be created (or if it already exists)
try:
    os.makedirs(desktop_path, exist_ok=True)
except PermissionError:
    print(f"Permission denied: Cannot create or access directory at {desktop_path}.")
    exit()

# Check the structure of the API response
if not res_data.get("results"):
    print("Unexpected API response structure or no results found.")
    print(json.dumps(res_data, indent=4))  # Print the API response to debug
    exit()

# Iterate through the image results and download each image
for i, result in enumerate(res_data.get("results", []), 1):
    img_url = result.get("thumbnail", {}).get("src")
    if img_url:
        # Send a request to download the image
        response = requests.get(img_url)
        # Check for a valid response
        if response.status_code == 200:
            # Construct a filename based on the loop index
            filename = f"{desktop_path}/image_back_{i}.jpg"
            # Save the image to the 'Search Image' directory on the desktop
            with open(filename, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to retrieve image {i}: {response.status_code}")
    else:
        print(f"No image URL found for item {i}")
