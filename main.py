from typing import Union

from fastapi import FastAPI
from fastapi import Request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!!"}


@app.get("/get_sentiment/{text}")
def read_item(text: str, user_id: Union[str, None] = None):
    return {"item_id": text, "sentiment": "positive", "user_id": user_id}

@app.post('/get_twitter_sentiment')
def get_twitter_sentiment(text: str, ip: str, user_id: Union[str, None] = None):

    return {"ip": ip,
            "text": text, 
            "sentiment": "positive", 
            "user_id": user_id}

@app.post('/get_twitter_sentiment_v2')
async def get_twitter_sentiment_v2(request:Request):
    data = await request.json()

    text = data.get('text')
    ip = data.get('ip')
    user_id = data.get('user_id', None)
    
    return {"ip": ip,
            "text": text, 
            "sentiment": "positive", 
            "user_id": user_id}