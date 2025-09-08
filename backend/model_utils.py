# backend/utils.py
import numpy as np

def create_sequences(data, seq_length=6):
    X = []
    for i in range(len(data) - seq_length+1):
        X.append(data[i:i + seq_length])
    return np.array(X)
