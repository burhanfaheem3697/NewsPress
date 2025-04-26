import pandas as pd

def load_data(news_path='D:/news_recommender/MINDsmall_train/news.tsv', behaviors_path='D:/news_recommender/MINDsmall_train/behaviors.tsv'):
    news = pd.read_csv(news_path, sep='\t', header=None,
                       names=["news_id", "category", "subcategory", "title", "abstract", "url", "title_entities", "abstract_entities"])
    behaviors = pd.read_csv(behaviors_path, sep='\t', header=None,
                            names=["impression_id", "user_id", "time", "history", "impressions"])
    return news, behaviors
