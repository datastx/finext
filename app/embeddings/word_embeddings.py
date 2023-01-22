import os

import numpy as np
import pandas as pd
from openai.embeddings_utils import cosine_similarity, get_embedding



DAVINCI = "text-similarity-davinci-001"
ADA = "text-embedding-ada-002"

def embedding(text: str) -> np.array:
    return get_embedding(text, engine=DAVINCI)


def get_corpus(location: str) -> pd.DataFrame:
    """_summary_

    Args:
        location (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(location, dtype=object)
    return df 

def cacluate_embeddings(df: pd.DataFrame, search_term_vector: np.array) -> pd.DataFrame:
    df['embedding'] = df['text'].apply( lambda x : embedding(x))
    df['embedding'] = df['embedding'].apply(np.array)
    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
    df.sort_values("similarities", ascending=False,inplace=True)
    return df