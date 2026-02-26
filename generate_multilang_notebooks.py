import nbformat as nbf
import os

langs = {
    "es": {
        "text1": """\
# 🧠 Amazon Fine Review - Análisis de Sentimientos y NLP
Este notebook documenta el pipeline de Procesamiento de Lenguaje Natural (NLP) aplicado a las reseñas de Amazon. Está diseñado para mostrar la limpieza de datos, extracción de sentimientos mediante VADER y TextBlob, e identificación de temas principales asociados a reseñas negativas.

## 1. Configuración y Carga de Datos
Importamos librerías y cargamos una muestra representativa de los datos de reseñas.""",
        "text2": """\
## 2. Limpieza y Preprocesamiento de Texto
Aplicamos expresiones regulares y lematización (usando SpaCy) para preparar el texto para el análisis de sentimientos, eliminando ruido como URLs y etiquetas HTML.""",
        "text3": """\
## 3. Análisis de Sentimientos (VADER & TextBlob)
Calculamos un puntaje compuesto de sentimiento para cada reseña, promediando los resultados de VADER y TextBlob para mayor precisión.""",
        "text4": """\
## 4. Modelado de Temas en Reseñas Negativas
Para las reseñas clasificadas como negativas, extraemos los temas predominantes basados en palabras clave predefinidas (ej. 'calidad', 'entrega', 'precio').""",
        "text5": """\
## 5. Exportación de Datos
Finalmente, organizamos las columnas necesarias para el Dashboard Interactivo de Streamlit y guardamos el dataset final."""
    },
    "en": {
        "text1": """\
# 🧠 Amazon Fine Review - Sentiment Analysis and NLP
This notebook documents the Natural Language Processing (NLP) pipeline applied to Amazon reviews. It is designed to showcase data cleaning, sentiment extraction using VADER and TextBlob, and the identification of main topics associated with negative reviews.

## 1. Setup and Data Loading
Importing libraries and loading a representative sample of the reviews data.""",
        "text2": """\
## 2. Text Cleaning and Preprocessing
Applying regular expressions and lemmatization (using SpaCy) to prepare the text for sentiment analysis, removing noise such as URLs and HTML tags.""",
        "text3": """\
## 3. Sentiment Analysis (VADER & TextBlob)
We calculate a composite sentiment score for each review, averaging the results from VADER and TextBlob for better accuracy.""",
        "text4": """\
## 4. Topic Modeling on Negative Reviews
For reviews classified as negative, we extract predominant topics based on predefined keywords (e.g., 'quality', 'delivery', 'price').""",
        "text5": """\
## 5. Data Export
Finally, we organize the necessary columns for the Interactive Streamlit Dashboard and save the final dataset."""
    },
    "pt": {
        "text1": """\
# 🧠 Amazon Fine Review - Análise de Sentimentos e NLP
Este notebook documenta o pipeline de Processamento de Linguagem Natural (NLP) aplicado às avaliações da Amazon. Ele foi projetado para mostrar a limpeza de dados, extração de sentimentos usando VADER e TextBlob, e a identificação de tópicos principais associados a avaliações negativas.

## 1. Configuração e Carregamento de Dados
Importando bibliotecas e carregando uma amostra representativa dos dados de avaliações.""",
        "text2": """\
## 2. Limpeza e Pré-processamento de Texto
Aplicando expressões regulares e lematização (usando SpaCy) para preparar o texto para a análise de sentimentos, removendo ruídos como URLs e tags HTML.""",
        "text3": """\
## 3. Análise de Sentimentos (VADER & TextBlob)
Calculamos uma pontuação de sentimento composta para cada avaliação, calculando a média dos resultados do VADER e TextBlob para maior precisão.""",
        "text4": """\
## 4. Modelagem de Tópicos em Avaliações Negativas
Para avaliações classificadas como negativas, extraímos tópicos predominantes com base em palavras-chave predefinidas (ex: 'qualidade', 'entrega', 'preço').""",
        "text5": """\
## 5. Exportação de Dados
Por fim, organizamos as colunas necessárias para o Dashboard Interativo do Streamlit e salvamos o dataset final."""
    }
}

code1 = """\
import pandas as pd
import numpy as np
import spacy
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load a sample from Amazon Fine Food Reviews dataset
try:
    df = pd.read_csv('data/Reviews.csv').sample(10000, random_state=42).copy()
except FileNotFoundError:
    print("Dataset not found locally. Skipping exact load.")
    df = pd.DataFrame({'Score': [5, 1], 'Summary': ['Great!', 'Bad'], 'Text': ['Good product.', 'Terrible.']})
df['Text'] = df['Text'].fillna('')
print("Sample Shape:", df.shape)
df[['Score', 'Summary', 'Text']].head(3)"""

code2 = """\
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def clean_text(text):
    t = text.lower()
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'http\\S+', ' ', t)
    t = re.sub(r'[^a-zA-Z\\s]', ' ', t)
    return t

df['PreClean'] = df['Text'].apply(clean_text)

cleaned_texts = []
for doc in nlp.pipe(df['PreClean'].tolist(), batch_size=500):
    tokens = [token.lemma_ for token in doc if len(token.text) > 1]
    cleaned_texts.append(" ".join(tokens))
    
df['CleanText'] = cleaned_texts
df[['PreClean', 'CleanText']].head(3)"""

code3 = """\
analyzer = SentimentIntensityAnalyzer()

df['Vader_Score'] = df['Text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
df['TextBlob_Score'] = df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

df['Sentiment_Score'] = (df['Vader_Score'] + df['TextBlob_Score']) / 2

def classify_sentiment(score):
    if score > 0.05: return "Positive"
    elif score < -0.05: return "Negative"
    else: return "Neutral"
    
df['Sentiment_Class'] = df['Sentiment_Score'].apply(classify_sentiment)
print(df['Sentiment_Class'].value_counts(normalize=True)*100)"""

code4 = """\
neg_reviews = df[df['Sentiment_Class'] == 'Negative'].copy()

categories = {
    "entrega/envío": ["deliver", "ship", "arrive", "box", "package"],
    "calidad": ["taste", "stale", "bad", "horrible", "awful"],
    "precio": ["price", "money", "expensive", "cost", "waste"]
}

def assign_category(text):
    text_lower = text.lower()
    counts = {cat: sum([1 for word in words if word in text_lower]) for cat, words in categories.items()}
    best_cat = max(counts, key=counts.get)
    if counts[best_cat] > 0:
        return best_cat
    return "otros"
    
if not neg_reviews.empty:
    neg_reviews['Dominant_Topic'] = neg_reviews['CleanText'].apply(assign_category)
    print("Negative Topics Frequency:\\n", neg_reviews['Dominant_Topic'].value_counts())"""

code5 = """\
# Simulate Category and Date for Dashboard integration
import random
product_categories = ["Snacks", "Beverages", "Pantry", "Candy", "Baby Food"]
df['Category'] = [random.choice(product_categories) for _ in range(len(df))]

if 'Time' in df.columns:
    df['Date'] = pd.to_datetime(df['Time'], unit='s')
else:
    df['Date'] = pd.to_datetime('today')

cols = ['Score', 'Date', 'Category', 'Sentiment_Score', 'Sentiment_Class']
cols = [c for c in cols if c in df.columns]
clean_df = df[cols]
print("Pipeline successful! Shape:", clean_df.shape)"""

def create_notebook(lang_code, lang_dict):
    nb = nbf.v4.new_notebook()

    nb['cells'] = [
        nbf.v4.new_markdown_cell(lang_dict['text1']),
        nbf.v4.new_code_cell(code1),
        nbf.v4.new_markdown_cell(lang_dict['text2']),
        nbf.v4.new_code_cell(code2),
        nbf.v4.new_markdown_cell(lang_dict['text3']),
        nbf.v4.new_code_cell(code3),
        nbf.v4.new_markdown_cell(lang_dict['text4']),
        nbf.v4.new_code_cell(code4),
        nbf.v4.new_markdown_cell(lang_dict['text5']),
        nbf.v4.new_code_cell(code5)
    ]

    filename = f'amazon_sentiment_analysis_{lang_code}.ipynb'
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"Notebook '{filename}' created successfully.")

if __name__ == '__main__':
    for lang_code, lang_dict in langs.items():
        create_notebook(lang_code, lang_dict)
