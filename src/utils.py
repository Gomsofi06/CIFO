import pandas as pd
import numpy as np

# Lê o ficheiro CSV, converte para um array e retorna 
def load_relationship_matrix(csv_path):
    df = pd.read_csv(csv_path)
    matrix = df.to_numpy()
    return matrix