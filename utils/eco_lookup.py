import os
import json

def load_all_eco_packs(directory="eco_packs", debug=False):
    eco_data = {}

    if debug:
        print(f"[DEBUG] Loading Eco-Packs from: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            region = os.path.splitext(filename)[0]
            json_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory, region + ".txt")

            try:
                # Load bird names from .txt first
                with open(txt_path, "r") as f:
                    txt_species = set(line.strip() for line in f if line.strip())
                if debug:
                    print(f"[DEBUG] Loaded '{txt_path}' with {len(txt_species)} species")

                # Load detailed info from .json
                with open(json_path, "r") as f:
                    detailed_info = json.load(f)

                eco_data[region] = {
                    "species_list": txt_species,
                    "details": detailed_info
                }
                if debug:
                    print(f"[DEBUG] Loaded '{filename}' with {len(detailed_info)} details")

            except Exception as e:
                print(f"[WARN] Failed to load Eco-Pack '{region}': {e}")

    return eco_data


def get_bird_info(bird_name, eco_data, region=None, debug=False):
    # Check specified region first
    if region and region in eco_data:
        pack = eco_data[region]
        if bird_name in pack["species_list"]:
            if debug:
                print(f"[DEBUG] Found '{bird_name}' in text list for region '{region}'")
            return pack["details"].get(bird_name, {"notes": "No details available."})
        elif debug:
            print(f"[DEBUG] Not found in text list for region '{region}'")

    # Fallback: search all regions
    for rname, pack in eco_data.items():
        if bird_name in pack["species_list"]:
            if debug:
                print(f"[DEBUG] Found '{bird_name}' in fallback region '{rname}'")
            return pack["details"].get(bird_name, {"notes": "No details available."})

    if debug:
        print(f"[DEBUG] '{bird_name}' not found in any Eco-Pack.")
    return None
