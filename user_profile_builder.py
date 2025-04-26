import numpy as np
import pandas as pd

def build_user_profiles(behaviors_df, news_id_to_emb):
    user_vectors = {}

    for index, row in behaviors_df.iterrows():
        user_id = row['user_id']
        history = row['history']
        
        if pd.isna(history):
            continue
        
        history_ids = history.split()
        embeddings = [news_id_to_emb[nid] for nid in history_ids if nid in news_id_to_emb]
        
        if embeddings:
            user_vectors[user_id] = np.mean(embeddings, axis=0)
    
    return user_vectors
