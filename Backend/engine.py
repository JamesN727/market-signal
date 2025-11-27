import trafilatura
from transformers import pipeline

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


if __name__ == "__main__":
    url = "https://www.cnbc.com/2025/11/25/stock-market-today-live-updates.html"
    text = get_article(url)
    print(get_sentiment(text))