import feedparser
from datetime import datetime
import os
import json
from engine import get_article, get_sentiment

rss_feeds = [
    "http://feeds.marketwatch.com/marketwatch/topstories/",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    "http://feeds.reuters.com/reuters/businessNews"
]

def get_daily_score():
    scores = []
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article_url = entry.link
            article_text = get_article(article_url)
            if article_text:
                sentiment = get_sentiment(article_text)
                score = sentiment['score']
                scores.append(score)
    if scores:
        average_score = sum(scores) / len(scores)
    else:
        return False
    data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "average_score": average_score,
        "article_count": len(scores)
    }
    with open("daily_scores.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    get_daily_score()
    

