from flask import Flask, render_template, request, jsonify
from dataLoader import load_data
from embedding_generator import generate_news_embeddings
from user_profile_builder import build_user_profiles
from recommender import recommend_news_for_user
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

with open('models/clicks_vs_accuracy.pkl', 'rb') as f:
    cached_clicks_accuracy_data = pickle.load(f)

print(f"✅ Loaded cached clicks vs accuracy for {len(cached_clicks_accuracy_data)} users.")

# Load data and cache
news_df, behaviors_df = load_data('./news.tsv', './behaviors.tsv')
news_id_to_emb = generate_news_embeddings(news_df)
user_vectors = build_user_profiles(behaviors_df, news_id_to_emb)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_id = request.json['user_id']  # Get user ID from JSON request body

        recommended_news_ids = recommend_news_for_user(user_id, user_vectors, news_id_to_emb, top_n=10)
        # Process the recommendations
        recommendations = []    
        accuracy = 0
        user_categories = []
        recommended_categories = []
        matching_categories = []

        if recommended_news_ids:
            # Get the categories of the user's interacted news
            user_interacted_news = behaviors_df[behaviors_df['user_id'] == user_id]['history'].dropna().str.split().sum()
            user_categories = news_df[news_df['news_id'].isin(user_interacted_news)]['category'].unique()
            user_categories = user_categories.tolist()
            # Get the categories of the recommended news
            
            recommended_categories = news_df[news_df['news_id'].isin(recommended_news_ids)]['category'].unique()

            recommended_categories = recommended_categories.tolist()
            
            matching_categories = set(user_categories).intersection(set(recommended_categories))

            matching_categories = list(matching_categories)

            # Prepare the list of recommendations (news title and category)
            recommendations = news_df[news_df['news_id'].isin(recommended_news_ids)][['title', 'category']].values.tolist()

            # Calculate accuracy
            accuracy = (len(matching_categories) / len(recommended_categories)) * 100 if len(recommended_categories) > 0 else 0

        return jsonify({
            'recommendations': recommendations,
            'accuracy': accuracy,
            'user_categories': user_categories,
            'recommended_categories': recommended_categories,
            'matching_categories': matching_categories
        })

    except Exception as e:
        print(f"Error occurred: {e}")  # Print error for debugging
        return jsonify({'error': str(e)}), 500


@app.route('/clicks_vs_accuracy')
def clicks_vs_accuracy():
    return jsonify(cached_clicks_accuracy_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # default Render port
    app.run(host='0.0.0.0', port=port)
