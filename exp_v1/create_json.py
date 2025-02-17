import json
import os
import re

output_dir = "./sweep_outputs"
pattern = re.compile(
    r"sweep_\d+_prompt_(.+?)_steps_(\d+)_blend_(\d+\.\d+)_weight_(\d+\.\d+)\.png"
)

images = []

for file in os.listdir(output_dir):
    match = pattern.match(file)
    if match:
        images.append(
            {
                "filename": os.path.join(output_dir, file),
                "prompt": match.group(1).replace("_", " "),
                "steps": match.group(2),
                "blend": match.group(3),
                "weight": match.group(4),
            }
        )

with open("images.json", "w") as f:
    json.dump(images, f, indent=4)

print("images.json created with all image details.")
