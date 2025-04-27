import os
import pickle

def generate_news_embeddings(news_df, cache_path='models/news_embeddings.pkl'):
    # Check if cache file exists
    if os.path.exists(cache_path):
        print(f"Loading news embeddings from {cache_path}...")
        with open(cache_path, 'rb') as f:
            news_id_to_emb = pickle.load(f)
    else:
        print("Generating news embeddings...")
        # Your normal embedding generation code
        # Example:
        from transformers import BertTokenizer, BertModel
        import torch

        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        news_id_to_emb = {}

        for idx, row in news_df.iterrows():
            news_id = row['news_id']
            title = row['title']

            inputs = tokenizer(title, return_tensors='pt', truncation=True, padding=True)
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()

            news_id_to_emb[news_id] = embedding

        # Save embeddings to pickle
        with open(cache_path, 'wb') as f:
            pickle.dump(news_id_to_emb, f)
        print(f"Saved news embeddings to {cache_path}")

    return news_id_to_emb
