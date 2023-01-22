import pytest
import pandas as pd
import numpy as np
from app.main import get_search_term_vector, embedding, run

class TestSimilarity:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.read_csv('/Users/brianmoore/githib.com/datastx/finext/app/fixtures/words.csv')
        self.df['embedding'] = self.df['text'].apply(lambda x: embedding(x))
        self.df['embedding'] = self.df['embedding'].apply(np.array)

    def test_run(self, capsys):
        with patch('builtins.input', return_value='example'):
            run()
            captured = capsys.readouterr()
            expected_output = '         text  similarities\n3     example      1.000000\n4      sample      0.965724\n1     examples      0.957484\n2     exampled      0.955375\n5    exemplify      0.951613\n8   exemplarize      0.948768\n6   exemplifying      0.948552\n7   exemplarity      0.948552\n9  exemplariness      0.948552\n0   exemplariness      0.948552\n'
            assert captured.out == expected_output
            
    def test_get_search_term_vector(self):
        search_term = "example"
        result = get_search_term_vector(search_term)
        expected_result = self.df[self.df['text'] == search_term]['embedding'].values[0]
        assert (result == expected_result).all()
