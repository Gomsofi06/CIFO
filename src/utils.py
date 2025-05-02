import pandas as pd
import numpy as np

# read csv and convert to array and return
def load_relationship_matrix(csv_path):
    df = pd.read_csv(csv_path)
    matrix = df.to_numpy()
    return matrix