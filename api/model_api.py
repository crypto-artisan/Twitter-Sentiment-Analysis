import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Union
import joblib
import pickle
import re
import string
import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
from utils.load_files import download_model, download_tokenizer
from utils.process_text import clean_text
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model


class SearchedTweets(BaseModel):
    """
    Class defining the attributes of searched tweets.

    Attributes:
    -----------
    topic_name : str, optional
        The topic or keyword to search for in tweets.
    username : str, optional
        The Twitter username to search for tweets from.
    date_init : str, optional
        The start date to search tweets from (YYYY-MM-DD).
    date_end : str, optional
        The end date to search tweets up to (YYYY-MM-DD).
    limit_number_search : int, optional
        The maximum number of tweets to return in the search.
    """
    topic_name: Union[str, None] = None
    username: Union[str, None] = None
    date_init: Union[str, None] = None
    date_end: Union[str, None] = None
    limit_number_search: int = 100
    


class SenimentModel:
    """
    Class for predicting the sentiment of tweets.

    Attributes:
    -----------
    _model_path : str
        The path to the saved Keras model for predicting sentiment.
    _tokenizer_path : str
        The path to the saved tokenizer for preprocessing text.
    tokenizer : keras.preprocessing.text.Tokenizer
        The tokenizer object for converting text to sequences of integers.
    model : keras.engine.sequential.Sequential
        The Keras model for predicting sentiment.
    """
    def __init__(self):
        """
        Initialize the SenimentModel object.

        Loads the saved Keras model and tokenizer for preprocessing text.
        """
        self._model_path = './model/saved_model/blstm_model'
        self._tokenizer_path = './model/saved_tokenizer/tokenizer.pickle'
        self.tokenizer = Tokenizer()
        try:
            with open(self._tokenizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
        except:
            with open(download_tokenizer(), 'rb') as handle:
                self.tokenizer = pickle.load(handle)
                
        try:   
            self.model = load_model(self._model_path)
        except:
            self.model = load_model(download_model())


    def _scrapp_tweet(self, topic_name=None, username=None, date_init=None, date_end=None, limit_number_search=None):
        """
        Scrape tweets based on search query.

        Parameters:
        -----------
        topic_name : str, optional
            The topic or keyword to search for in tweets.
        username : str, optional
            The Twitter username to search for tweets from.
        date_init : str, optional
            The start date to search tweets from (YYYY-MM-DD).
        date_end : str, optional
            The end date to search tweets up to (YYYY-MM-DD).
        limit_number_search : int, optional
            The maximum number of tweets to return in the search.

        Returns:
        --------
        pandas.core.frame.DataFrame
            A DataFrame containing the scraped tweets with cleaned text.
        """
        attributes_container = []

        if not limit_number_search: limit_number_search = 100
        if username: username = 'from:' + username
        if date_init: date_init = 'since:' + date_init
        if date_end: 
            # convert the string to a datetime object
            date = datetime.strptime(date_end, '%Y-%m-%d')

            # add one day
            new_date = date + timedelta(days=1)

            # convert the new date back to a string
            new_date_str = datetime.strftime(new_date, '%Y-%m-%d')
            
            date_end = 'until:' + new_date_str

        list_kwords = [username, topic_name, date_init, date_end]

        search_sentence = " ".join([s for s in list_kwords if s])
        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_sentence).get_items()):
            if i > (limit_number_search - 1):
                break
            attributes_container.append([tweet.user.username, tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content])
    
        # Creating a dataframe to load the list
        tweets_df = pd.DataFrame(attributes_container, columns=["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"])
        # Applying the cleaning function to both test and training datasets
        tweets_df["Tweet"] = tweets_df["Tweet"].apply(lambda x: clean_text(x))
        return tweets_df[["Date Created", "Number of Likes", "Tweet"]]


    def _preprocess_tweet(self, tweets_df: pd.DataFrame):   
        """
        Preprocesses cleaned tweets to be fed into the Keras neural network.

        Parameters:
        -----------
        tweets_df : pd.DataFrame
            The cleaned tweets in a pd.DataFrame format.

        Returns:
        --------
        pandas.core.frame.DataFrame
            A DataFrame containing the preprocessed tweets.
        """   
        tweets = tweets_df['Tweet'].values

        input_sequence = self.tokenizer.texts_to_sequences(tweets)
        padded_sequence = pad_sequences(input_sequence, maxlen=280, truncating='post')
        return padded_sequence


    def predict(self, topic_name=None, username=None, date_init=None, date_end=None, limit_number_search=None):
        """
        Takes search query parameters as arguments and returns a Pandas DataFrame of predicted sentiments.

        Parameters:
        -----------
        topic_name : str, optional
            The topic or keyword to search for in tweets.
        username : str, optional
            The Twitter username to search for tweets from.
        date_init : str, optional
            The start date to search tweets from (YYYY-MM-DD).
        date_end : str, optional
            The end date to search tweets up to (YYYY-MM-DD).
        limit_number_search : int, optional
            The maximum number of tweets to return in the search.

        Returns:
        --------
        pandas.core.frame.DataFrame
            A DataFrame containing the predictions and the cleaned tweets.
        """   
        
        tweets_df = self._scrapp_tweet(topic_name, username, date_init, date_end, limit_number_search)

        if len(tweets_df) == 0:
            return tweets_df
        
        processed_tweet = self._preprocess_tweet(tweets_df)

        # predict the sentiment probabilities
        sentiment_probs = self.model.predict(processed_tweet)

        # create a new column with rounded values
        tweets_df['Probability'] = sentiment_probs
        # create a new column with 'Positive' or 'Negative' values
        tweets_df['Sentiment'] = tweets_df['Probability'].apply(lambda x: 'Positive' if round(x) == 1 else 'Negative')

        return tweets_df[["Date Created", "Number of Likes", "Tweet", "Sentiment", "Probability"]]
    