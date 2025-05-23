"""
evaluation.py
Compute Hit@Core, Hit2, ROI and generate plots.
"""

import pandas as pd, matplotlib.pyplot as plt, numpy as np, yaml, json, os

def hit_at_core(pred_core, actual):
    return len(set(pred_core).intersection(actual))

def roi_example():
    # placeholder
    return 0.081
