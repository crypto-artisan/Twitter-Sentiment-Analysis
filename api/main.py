import uvicorn
import os
from uvicorn import run
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.model_api import SearchedTweets, SenimentModel



app = FastAPI()
model = SenimentModel()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)

class NoMatchException(HTTPException):
    """Custom exception for handling no matching tweets."""
    def __init__(self, tweets: SearchedTweets):
        super().__init__(status_code=404, detail=f"No matches found for tweets with attributes: '{tweets}'")


class PredictionErrorException(HTTPException):
    """Custom exception for handling errors during sentiment analysis."""
    def __init__(self, error_message: str):
        detail = f"Error occurred during prediction using BLSTM model : {error_message}"
        super().__init__(status_code=500, detail=detail)



@app.get("/")
async def root():
    """Default endpoint for the API."""
    return {"message": "Welcome to the Sentiment Analysis for Twieets API!"}


@app.post('/predict')
async def predict_sentiment(tweets: SearchedTweets):
    """
    Endpoint for performing sentiment analysis on searched tweets.

    Parameters:
    - `tweets` (SearchedTweets): Object containing search parameters for tweets.

    Returns:
    - (str): JSON formatted string containing sentiment analysis of searched tweets.
    """
    try:
        tweets_df = model.predict(
            tweets.topic_name, tweets.username, tweets.date_init, tweets.date_end, tweets.limit_number_search
        )            
    
    except Exception as e:
        if str(e) == 'empty query':
            raise NoMatchException(tweets)
        
        raise PredictionErrorException(error_message=str(e))
    
    tweets_json = tweets_df.to_json()
    return tweets_json



if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
