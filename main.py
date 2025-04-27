import os
import pickle
from dataLoader import load_data
from embedding_generator import generate_news_embeddings
from user_profile_builder import build_user_profiles
from recommender import recommend_news_for_user

# Paths for cached files
news_embedding_cache = 'news_embeddings.pkl'
user_vector_cache = 'user_vectors.pkl'

# Step 1: Load data
news_df, behaviors_df = load_data(
    'D:/news_recommender/MINDsmall_train/news.tsv',
    'D:/news_recommender/MINDsmall_train/behaviors.tsv'
)

# Step 2: Load or Generate News Embeddings
if os.path.exists(news_embedding_cache):
    print("Loading cached news embeddings...")
    with open(news_embedding_cache, 'rb') as f:
        news_id_to_emb = pickle.load(f)
else:
    print("Generating news embeddings...")
    news_id_to_emb = generate_news_embeddings(news_df)
    with open(news_embedding_cache, 'wb') as f:
        pickle.dump(news_id_to_emb, f)

# Step 3: Load or Build User Profiles
if os.path.exists(user_vector_cache):
    print("Loading cached user vectors...")
    with open(user_vector_cache, 'rb') as f:
        user_vectors = pickle.load(f)
else:
    print("Building user profiles...")
    user_vectors = build_user_profiles(behaviors_df, news_id_to_emb)
    with open(user_vector_cache, 'wb') as f:
        pickle.dump(user_vectors, f)

# Step 4: Recommend news for a specific user
user_id = "U73700"
recommendations = recommend_news_for_user(user_id, user_vectors, news_id_to_emb, top_n=10)

# Step 5: Extract User's Categories (Fixed)
user_interactions = behaviors_df[behaviors_df['user_id'] == user_id]

interacted_news_ids = []
for history in user_interactions['history'].dropna():
    interacted_news_ids.extend(history.split())

user_categories = news_df[news_df['news_id'].isin(interacted_news_ids)]['category'].unique()

# Step 6: Extract Categories of Recommended Articles
recommended_news_ids = recommendations
recommended_categories = news_df[news_df['news_id'].isin(recommended_news_ids)]['category'].unique()

# Step 7: Compare Categories
matching_categories = set(user_categories).intersection(set(recommended_categories))

#Step 8 : 
match_count = 0
total_recommendations = len(recommended_news_ids)

# For each recommended news, check if its category matches user categories
for news_id in recommended_news_ids:
    news_category = news_df[news_df['news_id'] == news_id]['category'].values
    if len(news_category) > 0 and news_category[0] in user_categories:
        match_count += 1

accuracy_percentage = (match_count / total_recommendations) * 100 if total_recommendations > 0 else 0

# Step 9: Output the Results
print(f"\nUser {user_id} has interacted with categories: {user_categories}")
print(f"Recommended news categories: {recommended_categories}")
print(f"Matching categories between user and recommendations: {matching_categories}")
print(f"\nAccuracy of recommendation: {match_count}/{total_recommendations} ({accuracy_percentage:.2f}%)")