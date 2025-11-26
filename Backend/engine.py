import trafilatura
from transformers import pipeline

sentiment_analyser = pipeline('text-classification', model='ProsusAI/finbert') #Finbert is trained for financial news

def get_article(url):
    download = trafilatura.fetch_url(url) #Retrieves article from url
    if download is None:
        return None
    text = trafilatura.extract(download) #Extracts the text from the article
    return text

def get_sentiment(text):
    #FinBERT can only read 512 at a time so let it seperate with 512 characters a time
    result = sentiment_analyser(text, truncation=True, max_length=512)
    return result[0]


if __name__ == "__main__":
    url = "https://www.bbc.co.uk/news/articles/c1kpnxvpgy2o"
    text = get_article(url)
    print(get_sentiment(text))