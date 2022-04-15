import markovify


class NaturalLanguageGenerator:
    def __init__(self, corpus_path: str = '', sentence: str = ''):
        if corpus_path != '':
            self.text = self.read_text_file(corpus_path)
        else:
            self.text = sentence
        self.text_model = markovify.Text(self.text)

    def read_text_file(self, corpus_path: str):
        with open(corpus_path, 'r') as f:
            return f.read()

    def generate_sentence(self) -> str:
        return self.text_model.make_sentence(tries=100)


if __name__ == '__main__':
    nlg = NaturalLanguageGenerator(corpus_path='corpus_potion_questions_happy.txt')
    print(nlg.generate_sentence())
