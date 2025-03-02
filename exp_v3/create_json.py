import json
import os
import re
from pathlib import Path

output_dir = "./sweep_outputs"

# Updated pattern to extract main components from all sweep filenames
base_pattern = r"sweep_(\d+)_prompt_(.+?)_iclightmult_([\d.]+)_steps_(\d+)_blend_([\d.]+)_weight_([\d.]+)"


def parse_filename(filename):
    """Parse a sweep filename and extract all parameters."""
    # First match the base pattern
    base_match = re.match(base_pattern, filename)
    if not base_match:
        return None

    sweep_id, prompt_text, iclightmult, steps, blend, weight = base_match.groups()

    # Create base parameter dictionary
    params = {
        "sweep_id": int(sweep_id),
        "prompt": prompt_text.replace("_", " "),
        "iclight_multiplier": float(iclightmult),
        "steps": int(steps),
        "blend": float(blend),
        "weight": float(weight),
        "ico_filename": None,
    }

    # Extract optional parameters that might appear after the base pattern
    remaining = filename[base_match.end() :]

    # Check for usemask parameter
    usemask_match = re.search(r"_usemask_(True|False)", remaining)
    if usemask_match:
        params["usemask"] = usemask_match.group(1) == "True"

    # Check for alphamask parameter
    alphamask_match = re.search(r"_alphamask_([^_.]+)", remaining)
    if alphamask_match:
        params["alphamask"] = alphamask_match.group(1)

    # Check if this is an ico image
    if "_ico.png" in remaining:
        params["is_ico"] = True
    else:
        params["is_ico"] = False

    return params


def main():
    images = {}
    ico_images = {}

    # Collect and process filenames
    for file in os.listdir(output_dir):
        if not file.startswith("sweep_"):
            continue

        params = parse_filename(file)
        if not params:
            continue

        # Get the full file path
        file_path = os.path.join(output_dir, file)

        # Generate a consistent base key for matching regular images with ico images
        # This includes all the base parameters, which should be common between paired files
        base_key = f"sweep_{params['sweep_id']}_prompt_{params['prompt'].replace(' ', '_')}_iclightmult_{params['iclight_multiplier']}_steps_{params['steps']}_blend_{params['blend']}_weight_{params['weight']}"

        if params["is_ico"]:
            ico_images[base_key] = file_path
        else:
            # Store the complete params dictionary for the main image
            images[base_key] = {
                "filename": file_path,
                **params,
                "ico_filename": None,  # Will be updated later if found
            }

    # Match ico images with their main images
    for base_key, ico_path in ico_images.items():
        if base_key in images:
            images[base_key]["ico_filename"] = ico_path

    # Convert to a list for easier serialization/usage
    result = list(images.values())

    # Output the results
    print(f"Processed {len(result)} images with {len(ico_images)} ico variants")

    # Save results to JSON
    with open("processed_sweep_results.json", "w") as f:
        json.dump(result, f, indent=2)

    # Print some sample entries to verify
    if result:
        print("\nSample entries:")
        for i in range(min(3, len(result))):
            print(f"\n{json.dumps(result[i], indent=2)}")


if __name__ == "__main__":
    main()
