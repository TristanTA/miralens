import os
import json

def load_all_eco_packs(directory="eco_packs", debug=False):
    eco_data = {}

    if debug:
        print(f"[DEBUG] Loading Eco-Packs from: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            region = os.path.splitext(filename)[0]
            path = os.path.join(directory, filename)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    eco_data[region] = data
                    if debug:
                        print(f"[DEBUG] Loaded '{filename}' with {len(data)} species")
            except Exception as e:
                print(f"[WARN] Failed to load {filename}: {e}")

    return eco_data

def get_bird_info(bird_name, eco_data, region=None, debug=False):
    # Try specific region first
    if region and region in eco_data:
        match = eco_data[region].get(bird_name)
        if debug:
            print(f"[DEBUG] {'Found' if match else 'Not found'} in region '{region}'")
        if match:
            return match

    # Search all regions
    for rname, rpack in eco_data.items():
        if bird_name in rpack:
            if debug:
                print(f"[DEBUG] Found '{bird_name}' in fallback region '{rname}'")
            return rpack[bird_name]

    if debug:
        print(f"[DEBUG] '{bird_name}' not found in any Eco-Pack.")
    return None