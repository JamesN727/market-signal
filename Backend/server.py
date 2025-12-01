from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import get_article, get_sentiment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React address
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (POST, GET, etc.)
    allow_headers=["*"], # Allow all headers
)

class RequestData(BaseModel):
    url: str
class ResponseData(BaseModel):
    title: str
    sentiment: str
    score: float
    markets: list[str]
    


@app.post("/analyse", response_model=ResponseData)
async def analyse_url(data: RequestData):
    link = data.url
    text = get_article(link)
    if not text: #Scrape failure
        raise HTTPException(status_code=400, detail="Could not scrape URL")
    result = get_sentiment(text)
    return {
        "title": "Article Title",
        "sentiment": result['label'],
        "score": result['score']
    }

