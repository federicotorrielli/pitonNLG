import spacy
from spacy.tokenizer import Tokenizer


class PhraseAnalisys:
    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(self.phrase)
        self.tokenizer = Tokenizer(self.nlp.vocab)
        self.tokenized_phrase = [word for word in self.tokenizer(self.phrase)]
        print(self.tokenized_phrase)

    def dependency_tree(self):
        return self.parse(self.doc.to_json()["tokens"])

    def parse(self, json_dependency_tree):
        """
        Get the dependency tuple for every word in the phrase
        """
        dt = {}
        for count, word in enumerate(self.tokenized_phrase):
            dep = json_dependency_tree[count]["dep"]
            head = json_dependency_tree[count]["head"]
            dt[word] = (dep, self.tokenized_phrase[head])
        return dt


if __name__ == "__main__":
    phrase = PhraseAnalisys("The ingredients of the polyjuice potion are: Lacewing flies, Knotgrass and a person's hair.")
    from pprint import pprint
    pprint(phrase.dependency_tree())
