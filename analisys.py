import spacy


class PhraseAnalisys:
    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp = spacy.load("en_core_web_md")  # python -m spacy download en_core_web_md
        self.doc = self.nlp(self.phrase)
        self.tokenized_phrase = [word.text for word in self.doc]

    def dependency_tree(self):
        """
        Get the dependency tree for the phrase
        :return: A dict containing the dependency tree in the form: {word: (dep, head)}
        """
        return self.__parse(self.doc.to_json()["tokens"])

    def ner(self):
        """
        Get the named entity recognition for the phrase
        :return: A dict containing the ner in the form: {word: ner}
        """
        return [(word.label_, word.text) for word in self.doc.ents]

    def __parse(self, json_dependency_tree):
        """
        Get the dependency tuple for every word in the phrase
        This method should be private only and only used by the dependency_tree method
        """
        dt = {}
        for count, word in enumerate(self.tokenized_phrase):
            dep = json_dependency_tree[count]["dep"]
            head = json_dependency_tree[count]["head"]
            dt[word] = (dep, self.tokenized_phrase[head])
        return dt


if __name__ == "__main__":
    strin = PhraseAnalisys(
        "The ingredients of the polyjuice potion are: Lacewing flies, Knotgrass and a person's hair.")
    from pprint import pprint

    pprint(strin.dependency_tree())
    pprint(strin.ner())
