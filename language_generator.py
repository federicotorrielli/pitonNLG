import markovify


class NaturalLanguageGenerator:
    def __init__(self, corpus_path: str):
        self.text = self.read_text_file(corpus_path)
        # TODO: generare un corpus di SOLO DOMANDE che Piton potrebbe fare allo studente
        self.text_model = markovify.Text(self.text)

    def read_text_file(self, corpus_path: str):
        with open(corpus_path, 'r') as f:
            return f.read()

    def generate_sentence(self) -> str:
        return self.text_model.make_sentence(tries=100)
