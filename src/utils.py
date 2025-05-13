import pandas as pd
import numpy as np

def load_relationship_matrix():
    df = pd.read_csv("data/seating_data.csv", index_col=0)
    return df.values.astype(np.int32)
