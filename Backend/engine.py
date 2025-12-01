import trafilatura
from transformers import pipeline
import spacy
nlp = spacy.load("en_core_web_sm")
sentiment_analyser = pipeline('text-classification', model='ProsusAI/finbert', top_k=None) #Finbert is trained for financial news

def get_article(url):
    download = trafilatura.fetch_url(url) #Retrieves article from url
    if download is None:
        return None
    text = trafilatura.extract(download) #Extracts the text from the article
    return text

def get_sentiment(text):
    #FinBERT can only read 512 at a time so let it seperate with 512 characters a time
    results = sentiment_analyser(text, truncation=True, max_length=512)[0]
    scores = {item['label']: item['score'] for item in results}
    compound_score = scores['positive'] - scores['negative']
    if compound_score > 0.15:
        label = "Bullish"
    elif compound_score > 0.05:
        label = "Slightly Bullish"
    elif compound_score < -0.15:
        label = "Bearish"
    elif compound_score < -0.05:
        label = "Slightly Bearish"
    else:
        label = "Neutral"
    return {
        "label": label,
        "score": compound_score,
        "details": scores
    }

def get_most_frequent_markets(text):
    doc = nlp(text)
    financial_entities = ["ORG", "GPE", "MONEY"] 
    market_keywords = ["stock", "market", "index", "exchange", "street", "bank", "corp", "inc", "ltd"]
    extracted_entities = set()
    for ent in doc.ents:
        entity_text = ent.text.strip()
        # Check if the entity type is relevant
        if ent.label_ in financial_entities:
            
            if len(entity_text) < 3:
                continue
            
            # Check for general keywords to confirm financial context
            if any(keyword in entity_text.lower() for keyword in market_keywords):
                extracted_entities.add(entity_text)
            
            # Include specific financial hubs/indices that might not have a keyword
            if ent.label_ == "GPE" and entity_text.lower() in ["wall street", "london", "frankfurt", "tokyo", "new york"]:
                extracted_entities.add(entity_text)
                
            if ent.text.isupper() and len(ent.text) <= 5 and ent.label_ == "ORG":
                extracted_entities.add(ent.text)

    # Return as a list of unique strings
    return list(extracted_entities)

if __name__ == "__main__":
    url = "https://www.cnbc.com/2025/11/25/jim-cramer-calls-nvidias-stock-slide-a-buying-opportunity-heres-why.html"
    text = get_article(url)
    print(get_most_frequent_markets(text))