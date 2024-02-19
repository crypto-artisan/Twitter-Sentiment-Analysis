# Sentiment Analysis API for Twitter with a Deep Learnig model and FastAPI

This project implements an API with a deep learning model (Bidirectional LSTM) for sentiment analysis of tweets. The api searches tweets by topic, username and/or date and obtains a prediction of tweets matching the query. The model was trained on a large dataset of tweets (around 1.6 million), and it can classify each tweet as positive or negative.

## Installation

To use this API, you need to have Docker installed on your system. You can then build and run the Docker container by running:

```
docker build -t sentiment-analysis-api .
docker run -p 8000:8000 --name sentiment-api sentiment-analysis-app
```

This will build the Docker image and run the container, which listens on http://localhost:8000/. I strongly recommend visiting the following page, which offers an interactive UI of the API: http://localhost:8000/docs

If you don't want to use Docker you can install the requiered packages by running:

```
pip install -r requirements.txt
```

And then start the API server running the next command:

```
uvicorn api.main:app --reload
```

## Usage

You can then send requests to the API using the following attributes:

- `topic_name`: Returns the sentiment analysis of the latest tweets about a given topic.
- `username`: Returns the sentiment analysis of the latest tweets by a given user.
- `date_init`: Returns the sentiment analysis of the tweets posted since a given date.
- `date_end`: Returns the sentiment analysis of the tweets posted until a given date.
- `limit_number_search`: Limits the number of tweets scraped for the sentiment analysis.

The API will return a JSON response with the sentiment analysis results.

## License

This project is licensed under the MIT License. You can use it for any purpose, including commercial projects. However, please credit the original author and provide a link to the original repository.
