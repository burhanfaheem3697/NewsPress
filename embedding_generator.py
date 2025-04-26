from sentence_transformers import SentenceTransformer

def generate_news_embeddings(news_df):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    news_df['text'] = news_df['title'].fillna('') + ' ' + news_df['abstract'].fillna('')
    embeddings = model.encode(news_df['text'].tolist(), show_progress_bar=True)
    return dict(zip(news_df['news_id'], embeddings))
