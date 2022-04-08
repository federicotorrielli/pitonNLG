import spacy


class PhraseAnalisys:
    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp = spacy.load("en_core_web_md")  # python -m spacy download en_core_web_md
        self.doc = self.nlp(self.phrase)
        self.tokenized_phrase = [word.text.lower() for word in self.doc]
        self.is_question = self.check_if_question()
        self.is_useful = False
        self.polarity = True  # False is negative and True is positive
        self.useful_list = []

    def dependency_tree(self):
        """
        Get the dependency tree for the phrase
        :return: A dict containing the dependency tree in the form: {word: (dep, head)}
        """
        return self.__parse(self.doc.to_json()["tokens"])

    def check_if_question(self):
        """
        Check if the phrase is a question
        :return: True if the phrase is a question, False otherwise
        """
        if "?" in self.phrase:
            self.is_question = True
        else:
            self.is_question = False
        return self.is_question

    def check_polarity(self):
        for m in self.doc.to_json()["tokens"]:
            if m['morph'] == "Polarity=Neg":
                self.polarity = False
        return self.polarity

    def check_if_useful(self, external_useful_list=None):
        """
        Check if the phrase contains any of the ingredients
        of the potions
        :return: True if the phrase contains any of the ingredients
        of the potions, False otherwise
        """
        useful = False
        for word in self.tokenized_phrase:
            if word in external_useful_list:
                useful = True
                self.useful_list.append(word)
        self.is_useful = useful
        return self.is_useful

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
    strin = PhraseAnalisys("There aren't spiders in the potion")
    from pprint import pprint

    pprint(strin.doc.to_json())
    pprint(strin.dependency_tree())
    pprint(strin.ner())
    print(strin.check_polarity())
