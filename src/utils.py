"""Utility functions"""
import pandas as pd
from pathlib import Path

def load_cases(file_path):
    return pd.read_csv(file_path)
