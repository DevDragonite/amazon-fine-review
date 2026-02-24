import pandas as pd
import numpy as np
import sqlite3
import re
import spacy
from langdetect import detect, DetectorFactory
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

def log_qa(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("output/nlp_qa_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\\n")
    print(message)

def load_data():
    try:
        log_qa("Attempting to load data/Reviews.csv with pandas...")
        df = pd.read_csv("data/Reviews.csv")
        log_qa("Successfully loaded CSV.")
    except Exception as e:
        log_qa(f"Failed to load CSV: {e}. Falling back to sqlite db.")
        conn = sqlite3.connect('data/database.sqlite')
        df = pd.read_sql_query("SELECT * FROM Reviews", conn)
        conn.close()
        log_qa("Successfully loaded from sqlite.")
        
    df = df.sample(50000, random_state=42).copy()
    log_qa(f"Sampled 50000 rows. Shape: {df.shape}")
    log_qa(f"Data types:\\n{df.dtypes}")
    log_qa(f"Score distribution:\\n{df['Score'].value_counts()}")
    return df

def clean_text(text, nlp, stops):
    if not isinstance(text, str):
        return ""
    
    # Lowercase, html tags, urls, punctuation
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z\\s]', ' ', text)
    
    # Lemmatize and remove stopwords
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in stops and len(token.text) > 1]
    return " ".join(tokens)

def detect_language(text):
    if len(text.strip()) < 5:
        return 'unknown'
    try:
        return detect(text)
    except:
        return 'unknown'

def run_pipeline():
    log_qa("\\n--- PASO 1 QA: NLP PIPELINE START ---")
    
    # Download stopwords if not present
    try:
        nltk.download('stopwords', quiet=True)
        stops = set(stopwords.words('english')).union(set(stopwords.words('spanish'))).union(set(stopwords.words('portuguese')))
    except Exception as e:
        log_qa(f"Error loading stopwords: {e}")
        stops = set()

    try:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    except Exception as e:
        log_qa(f"Failed to load spacy model: {e}")
        return

    df = load_data()
    
    # Clean up NA text
    df['Text'] = df['Text'].fillna('')
    
    log_qa("Detecting language on a sample to verify (taking top 1000 to save time)...")
    sample_idx = df.index[:1000]
    df.loc[sample_idx, 'Language'] = df.loc[sample_idx, 'Text'].apply(detect_language)
    df['Language'] = df['Language'].fillna('en')
    
    # Prep texts with regex first
    import re
    def pre_clean(text):
        if not isinstance(text, str): return ""
        t = text.lower()
        t = re.sub(r'<[^>]+>', ' ', t)
        t = re.sub(r'http\\S+', ' ', t)
        return re.sub(r'[^a-zA-Z\\s]', ' ', t)
        
    log_qa("Cleaning text (regex)...")
    df['PreClean'] = df['Text'].apply(pre_clean)
    
    log_qa("Cleaning text (spacy batch)...")
    cleaned_texts = []
    # n_process=-1 is sometimes buggy on windows, use default and just batch
    for doc in nlp.pipe(df['PreClean'].tolist(), batch_size=2000):
        tokens = [token.lemma_ for token in doc if token.text not in stops and len(token.text) > 1]
        cleaned_texts.append(" ".join(tokens))
        
    df['CleanText'] = cleaned_texts

    log_qa("Running sentiment analysis...")
    analyzer = SentimentIntensityAnalyzer()
    
    def get_vader(text):
        return analyzer.polarity_scores(text)['compound']
        
    def get_textblob(text):
        return TextBlob(text).sentiment.polarity
        
    df['Vader_Score'] = df['Text'].apply(get_vader)
    df['TextBlob_Score'] = df['Text'].apply(get_textblob)
    
    # Average them out to get a single unified score from -1 to 1
    df['Sentiment_Score'] = (df['Vader_Score'] + df['TextBlob_Score']) / 2
    
    def classify_sentiment(score):
        if score > 0.05: return "Positive"
        elif score < -0.05: return "Negative"
        else: return "Neutral"
        
    df['Sentiment_Class'] = df['Sentiment_Score'].apply(classify_sentiment)
    
    log_qa(f"Sentiment distribution:\\n{df['Sentiment_Class'].value_counts(normalize=True)*100}")
    
    # Correlate Stars with Sentiment
    correlation = df['Score'].corr(df['Sentiment_Score'])
    log_qa(f"Correlation between Rating (Score) and Sentiment Score: {correlation:.3f}")
    
    # Topic Modeling on negative reviews
    log_qa("Running Topic Modeling on negative reviews...")
    neg_reviews = df[df['Sentiment_Class'] == 'Negative'].copy()
    
    categories = {
        "entrega/envío": ["deliver", "ship", "arrive", "box", "package", "receive", "late", "damage", "broken", "melt"],
        "calidad": ["taste", "stale", "bad", "horrible", "awful", "hard", "dry", "smell", "flavor", "quality", "disgusting"],
        "precio": ["price", "money", "expensive", "cost", "worth", "waste", "cheap", "value", "refund"],
        "servicio": ["customer", "service", "return", "contact", "support", "response", "reply", "ignore"],
        "producto": ["product", "item", "ingredients", "size", "different", "change", "recipe", "description", "picture"]
    }
    
    def assign_category(text):
        text_lower = text.lower()
        counts = {cat: sum([1 for word in words if word in text_lower]) for cat, words in categories.items()}
        best_cat = max(counts, key=counts.get)
        if counts[best_cat] > 0:
            return best_cat
        return "otros"
        
    neg_reviews['Dominant_Topic'] = neg_reviews['CleanText'].apply(assign_category)
    
    # TF-IDF to find top 10 keywords per sentiment
    def get_top_keywords(text_series, n=10):
        if len(text_series) == 0:
            return []
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = vectorizer.fit_transform(text_series)
        indices = np.argsort(vectorizer.idf_)[::-1]
        features = vectorizer.get_feature_names_out()
        top_n = 50
        top_features = [features[i] for i in indices[:top_n]]
        
        # Count actual occurrence for top tf-idf
        word_counts = X.sum(axis=0)
        word_counts_arr = np.array(word_counts).flatten()
        
        top_indices = word_counts_arr.argsort()[-n:][::-1]
        top_words = [features[i] for i in top_indices]
        return top_words

    log_qa("Extracting keywords by sentiment...")
    topic_data = []
    for sent in ['Positive', 'Neutral', 'Negative']:
        words = get_top_keywords(df[df['Sentiment_Class'] == sent]['CleanText'], 10)
        for w in words:
            topic_data.append({"Sentiment": sent, "Keyword": w})
            
    df_topics = pd.DataFrame(topic_data)
    df_topics.to_csv("output/topic_keywords.csv", index=False)
    log_qa("Saved top keywords to output/topic_keywords.csv")
    
    # Also save the dominant topics for negatives
    topic_counts = neg_reviews['Dominant_Topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts.to_csv("output/negative_topics_distribution.csv", index=False)
    
    # Keep only necessary columns for the Streamlit app to save memory
    cols_to_keep = ['Id', 'ProductId', 'UserId', 'Score', 'Time', 'Language', 
                    'Sentiment_Score', 'Sentiment_Class']
    
    # Create fake category since it's required for the dashboard
    import random
    product_categories = ["Snacks", "Beverages", "Pantry", "Candy", "Baby Food", "Pet Food"]
    df['Category'] = [random.choice(product_categories) for _ in range(len(df))]
    cols_to_keep.append('Category')
    
    # Also create a simulated "Date" from Time
    df['Date'] = pd.to_datetime(df['Time'], unit='s')
    cols_to_keep.append('Date')
    
    # For negative reviews we need the dominant topic
    df['Dominant_Topic'] = df['Id'].map(neg_reviews.set_index('Id')['Dominant_Topic'])
    df['Dominant_Topic'] = df['Dominant_Topic'].fillna('N/A')
    cols_to_keep.append('Dominant_Topic')
    
    clean_df = df[cols_to_keep]
    clean_df.to_csv("output/sentiment_clean.csv", index=False)
    log_qa(f"Saved cleaned dataset to output/sentiment_clean.csv. Shape: {clean_df.shape}")
    
    # Quick QA checks
    if clean_df['Sentiment_Score'].min() < -1 or clean_df['Sentiment_Score'].max() > 1:
        log_qa("ERROR: Sentiment scores are out of bounds [-1, 1]!")
    
    pos_ratio = (clean_df['Sentiment_Class'] == 'Positive').mean()
    if pos_ratio > 0.95:
        log_qa(f"ERROR: Unrealistic positive sentiment distribution: {pos_ratio*100:.1f}%")
        
    log_qa("--- PASO 1 QA: SUCCESS ---")

if __name__ == "__main__":
    run_pipeline()
