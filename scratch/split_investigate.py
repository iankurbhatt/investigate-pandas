import os
import json

# Ensure investigate_pandas directory exists
os.makedirs('investigate_pandas', exist_ok=True)

with open('investigate.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
metadata = nb['metadata']
nbformat = nb['nbformat']
nbformat_minor = nb['nbformat_minor']

# Prepend setup cells for notebooks that start mid-way
setup_cells = [
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Setup imports & load dataset\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import time\n",
            "import os\n",
            "df = pd.read_csv('data/raw_transactions.csv', na_values=['Nan', ''])\n"
        ]
    }
]

def save_split_nb(filename, start_idx, end_idx, prepend_setup=False):
    selected_cells = cells[start_idx : end_idx + 1]
    if prepend_setup:
        # Prepend the setup cells
        selected_cells = setup_cells + selected_cells
        
    split_nb = {
        "cells": selected_cells,
        "metadata": metadata,
        "nbformat": nbformat,
        "nbformat_minor": nbformat_minor
    }
    path = os.path.join('investigate_pandas', f"investigate_{filename}")
    with open(path, 'w', encoding='utf-8') as f_out:
        json.dump(split_nb, f_out, indent=1)
    print(f"Created notebook slice: {path} (indices {start_idx} to {end_idx})")

# Split according to the exact cell boundaries:
save_split_nb('pandas_basics.ipynb', 0, 18, prepend_setup=False)
save_split_nb('sorting_reshaping.ipynb', 19, 32, prepend_setup=True)
save_split_nb('indexing_subsetting.ipynb', 33, 50, prepend_setup=True)
save_split_nb('combining.ipynb', 51, 54, prepend_setup=True)
save_split_nb('statistics_missing.ipynb', 55, 60, prepend_setup=True)
save_split_nb('groupby_operations.ipynb', 61, 64, prepend_setup=True)
save_split_nb('graphing_plotting.ipynb', 65, 66, prepend_setup=True)
save_split_nb('advanced_concepts.ipynb', 67, 101, prepend_setup=True)
save_split_nb('interview_questions.ipynb', 102, 202, prepend_setup=True)

print("Slicing complete!")
