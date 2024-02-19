import os
import gdown

def download_model():
    """
    Downloads a pre-trained model from Google Drive using the gdown package.

    Returns:
    destination_path (str): The path to the saved model.
    """
    url = "https://drive.google.com/drive/folders/1B2C9CIzZYhuGUd82sHsH2gAmqvtSfhTh?usp=sharing"
    gdown.download_folder(url)
    source_path = './blstm_model'
    destination_path = './model/saved_model/blstm_model'
    os.rename(source_path, destination_path)
    return destination_path


def download_tokenizer():
    url = "https://drive.google.com/drive/folders/1w6PFUhIBXEfA4d5JCd54-r2Nb59UdiDP?usp=sharing"
    gdown.download_folder(url)
    source_path = './tokenizer'
    destination_path = './model/saved_tokenizer/'
    os.rename(source_path, destination_path)
    return destination_path