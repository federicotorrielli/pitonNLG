import markovify
from pathlib import Path


class NaturalLanguageGenerator:
    def __init__(self, sentiment: str, corpus_path=False):
        self.sentiment = sentiment
        self.text = self.read_text_file(corpus_path)
        self.text_model = markovify.Text(self.text)

    def read_text_file(self, corpus_path: bool) -> str:
        if corpus_path:
            paths = [p for p in Path('.').glob('questions/*.txt')]
            final_path = [p for p in paths if self.sentiment in p.name][0]
        else:
            paths = [p for p in Path('.').glob('fillers/*.txt')]
            final_path = [p for p in paths if self.sentiment in p.name][0]
        text = ''
        f = final_path.open('r')
        text += f.read()
        f.close()
        return text

    def generate_sentence(self) -> str:
        generated_sentence = self.text_model.make_sentence(tries=100)
        if generated_sentence is None:
            return self.generate_sentence()
        else:
            return generated_sentence


if __name__ == '__main__':
    nlg = NaturalLanguageGenerator(False)
    print(nlg.generate_sentence())
