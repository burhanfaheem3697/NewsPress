import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_news_for_user(user_id, user_vectors, news_id_to_emb, top_n=10):
    if user_id not in user_vectors:
        return []
    
    user_vector = user_vectors[user_id].reshape(1, -1)
    all_news_vecs = np.array(list(news_id_to_emb.values()))
    
    similarities = cosine_similarity(user_vector, all_news_vecs)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    news_ids = list(news_id_to_emb.keys())
    return [news_ids[i] for i in top_indices]
