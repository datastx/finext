# TODO kill dis
import sys

sys.path.append('/Users/brianmoore/githib.com/datastx/finext')

import argparse
import os
from dataclasses import dataclass

from app.embeddings.word_embeddings import (cacluate_embeddings, embedding,
                                            get_corpus)


@dataclass
class CliInput:
    search_term: str

def get_args()-> CliInput:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        CliInput: _description_
    """
    parser = argparse.ArgumentParser()  
    parser.add_argument("-i", "--input", help="Input text to process")
    args = parser.parse_args()
    search_term = None
    if args.input:
        search_term = args.input
    else:
        raise ValueError(f'Must provide a search term')

    cli_input = CliInput(search_term=search_term)
    return cli_input



def run() -> None:
    """_summary_

    Raises:
        ValueError: _description_
    """
    api_key = "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"
    os.environ['OPENAI_API_KEY'] = api_key
    if os.getenv('OPENAI_API_KEY') == None:
        raise ValueError(f"must set OPENAI_API_KEY which is currently {os.getenv('OPENAI_API_KEY')}")
    else:
        print(f"key is {os.getenv('OPENAI_API_KEY')}" )
    cli_input = get_args()
    search_term_vector = embedding(cli_input.search_term)

    df = get_corpus('/Users/brianmoore/githib.com/datastx/finext/app/fixtures/words.csv')
    df = cacluate_embeddings(df, search_term_vector)

    
    print(df[['text','similarities']].head(10))


if __name__ == "__main__":
    run()