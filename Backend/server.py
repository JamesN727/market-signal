from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from engine import get_article, get_sentiment

app = FastAPI()

class RequestData(BaseModel):
    url: str
class ResponseData(BaseModel):
    title: str
    sentiment: str
    score: float
    


@app.post("/analyse", response_model=ResponseData)
def analyse_url(data: RequestData):
    link = data.url
    text = get_article(link)
    if not text: #Scrape failure
        raise HTTPException(status_code=400, response="Could not scrape URL")
    result = get_sentiment(text)
    return {
        "title": "Article Title",
        "sentiment": result['label'],
        "score": result['score']
    }

