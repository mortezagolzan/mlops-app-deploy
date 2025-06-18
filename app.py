from scripts.data_model import NLPDataInput, NLPDataOutput
from scripts.s3 import download_directory
from typing import Union
import os
import uvicorn
from fastapi import FastAPI
from fastapi import Request
import torch
from transformers import pipeline
import time


app = FastAPI()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


######## Downlaod Model ########

model_name = 'tinybert-sentiment-analysis'
local_path = 'ml-models/' + model_name

if not os.path.exists(local_path):
    download_directory(local_path, model_name)

sentiment_model = pipeline('text-classification', model=local_path, device=device)


################################

@app.get("/")
def read_root():
    return {"Hello": "World!!"}

@app.post('/api/v1/get_sentiment')
def get_sentiment(data: NLPDataInput):

    start = time.time()
    output = sentiment_model(data.text)
    end = time.time()

    prediction_time = int((end - start) * 1000)

    labels = [item['label'] for item in output]
    scores = [item['score'] for item in output]

    output = NLPDataOutput(
        model_name = model_name,
        text=data.text,
        labels=labels,
        scores=scores,
        prediction_time=prediction_time
    )
    return output

if __name__ == "__main__":
    uvicorn.run(app = "app:app", port = 8000, reload = True)