import os
import pickle

def build_user_profiles(behaviors_df, news_id_to_emb, cache_path='models/user_vectors.pkl'):
    # Check if cache file exists
    if os.path.exists(cache_path):
        print(f"Loading user profiles from {cache_path}...")
        with open(cache_path, 'rb') as f:
            user_vectors = pickle.load(f)
    else:
        print("Building user profiles...")
        # Your normal user profile building code
        import numpy as np

        user_vectors = {}

        for idx, row in behaviors_df.iterrows():
            user_id = row['user_id']
            history = row['history']
            if pd.isna(history):
                continue
            clicked_news = history.split()

            vectors = []
            for news_id in clicked_news:
                if news_id in news_id_to_emb:
                    vectors.append(news_id_to_emb[news_id])

            if vectors:
                user_vectors[user_id] = np.mean(vectors, axis=0)

        # Save user vectors to pickle
        with open(cache_path, 'wb') as f:
            pickle.dump(user_vectors, f)
        print(f"Saved user profiles to {cache_path}")

    return user_vectors
