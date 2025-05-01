import pickle
import pandas as pd
from dataLoader import load_data
from embedding_generator import generate_news_embeddings
from user_profile_builder import build_user_profiles
from recommender import recommend_news_for_user

# Load your data
news_df, behaviors_df = load_data('D:/news_recommender/MINDsmall_train/news.tsv', 'D:/news_recommender/MINDsmall_train/behaviors.tsv')
news_id_to_emb = generate_news_embeddings(news_df)
user_vectors = build_user_profiles(behaviors_df, news_id_to_emb)

clicks_vs_accuracy_list = []

for user_id in behaviors_df['user_id'].unique():
    user_history_series = behaviors_df[behaviors_df['user_id'] == user_id]['history'].dropna()

    if user_history_series.empty:
        continue  # No history for this user

    user_history_list = user_history_series.iloc[0].split()

    if not user_history_list:
        continue  # Skip if history is empty (no clicks)

    num_clicks = len(user_history_list)

    recommended_news_ids = recommend_news_for_user(user_id, user_vectors, news_id_to_emb, top_n=10)

    if recommended_news_ids:
        user_categories = news_df[news_df['news_id'].isin(user_history_list)]['category'].unique()
        recommended_categories = news_df[news_df['news_id'].isin(recommended_news_ids)]['category'].unique()

        if len(recommended_categories) == 0:
            continue  # No recommended categories, skip

        matching_categories = set(user_categories).intersection(set(recommended_categories))

        accuracy = (len(matching_categories) / len(recommended_categories)) * 100

        clicks_vs_accuracy_list.append({
            'clicks': num_clicks,
            'accuracy': accuracy
        })


# Save it as pickle
with open('clicks_vs_accuracy.pkl', 'wb') as f:
    pickle.dump(clicks_vs_accuracy_list, f)

print(f"✅ Saved clicks vs accuracy for {len(clicks_vs_accuracy_list)} users to clicks_vs_accuracy.pkl")
