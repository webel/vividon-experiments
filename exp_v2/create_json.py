import json
import os
import re

output_dir = "./sweep_outputs"

# Pattern to extract base filename up to "weight_X"
pattern = re.compile(
    r"(sweep_\d+_prompt_.+?_iclightmult_[\d.]+_steps_\d+_blend_[\d.]+_weight_[\d.]+)"
)

images = {}
ico_images = {}

# Collect filenames
for file in os.listdir(output_dir):
    match = pattern.match(file)
    if match:
        base_name = match.group(1)

        # Normalize filenames by stripping redundant .png endings
        file_path = os.path.join(output_dir, file)
        if file.endswith("_ico.png"):
            ico_images[base_name] = file_path  # Store as _ico match
        else:
            images[base_name] = {
                "filename": file_path,
                "prompt": base_name.split("_prompt_")[1]
                .split("_iclightmult_")[0]
                .replace("_", " "),
                "iclight_multiplier": float(
                    base_name.split("_iclightmult_")[1].split("_steps_")[0]
                ),
                "steps": int(base_name.split("_steps_")[1].split("_blend_")[0]),
                "blend": float(base_name.split("_blend_")[1].split("_weight_")[0]),
                "weight": float(base_name.split("_weight_")[1]),
                "ico_filename": None,  # Will be updated if found
            }

# Match _ico files based on the cleaned base_name
for base_name, img_data in images.items():
    if base_name in ico_images:
        img_data["ico_filename"] = ico_images[base_name]

# Save to JSON
with open("images.json", "w") as f:
    json.dump(list(images.values()), f, indent=4)

print("✅ images.json created successfully with proper _ico matches!")
