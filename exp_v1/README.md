# Experiment 1

## Key takeaway

**Good**: we're semi-successfully keeping the foreground untouched.
**Bad**: we're barely relighting, the prompts look mostly the same, and the background does get a lot of shadows.

## Run locally

Serve this directory any way you like, maybe with

```
python3 -m http.server 8000

# or

npx server
```

Enjoy.

## Deets

This experiment automates relighting tasks by sweeping across:

Blend percentages: [0.3, 0.5, 0.7, 1.0]

Weights: [0.1, 0.3, 0.5]

Steps: [20, 30, 50]

Lighting prompts: 15 different lighting conditions like natural light, golden hour, candlelight, studio lighting, etc.

The script ran relighting_v6.py (converted relighting_v6.json workflow), and stored images uniquely named with their parameters in ./sweep_outputs.
