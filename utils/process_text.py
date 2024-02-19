import re
import string


def clean_text(text):
    """
    Cleans the given text by performing the following operations:
    - Convert the text to lowercase.
    - Remove all user mentions.
    - Remove all hashtags.
    - Remove text in square brackets.
    - Remove all URLs.
    - Remove all HTML tags.
    - Remove all punctuation.
    - Remove all newline characters.
    - Remove words containing numbers.
    - Remove all emojis.

    Args:
    text (str): The text to be cleaned.

    Returns:
    text (str): The cleaned text.
    """
    text = text.lower()
    text = re.sub("@[A-Za-z0-9_]+","", text)
    text = re.sub("#[A-Za-z0-9_]+","", text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)

    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    return text