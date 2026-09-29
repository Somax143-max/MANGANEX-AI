MANGANEX AI - SIH 2026 PS 26009 polish patch

What this patch changes:
1. Replaces the production comparison stacked-looking chart with a clear grouped bar chart.
2. Replaces the rectangular cloud of map points with a weighted prospectivity heatmap plus top candidate points.
3. Makes the synthetic generator spatially clustered so the demo map looks like a prospectivity workflow instead of a random rectangle.
4. Renames reserve display text to "Model-estimated Potential" to avoid implying certified mineral reserves.
5. Adds the end-to-end AI decision pipeline on the Dashboard.
6. Adds model-intelligence sections explaining the Random Forest models and inputs.
7. Adds transparent prospectivity signal contribution visualization in the AI Location Simulator.
8. Adds stronger prototype/synthetic-data disclaimers.
9. Keeps the existing four-page navigation and inference workflow.

Install / run from the MANGANEX_AI project root:

python -m pip install -r requirements.txt
python "src/data/generate_dataset.py"
python "src/train_models.py"
streamlit run "dashboard/app.py"

IMPORTANT:
- The dataset remains SYNTHETIC. Do not present it as real geological reserve data.
- The spatial clusters are only for visual/demo realism.
- Real deployment should replace the synthetic layer with validated satellite, geological and operational data.
