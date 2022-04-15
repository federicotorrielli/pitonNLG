import spacy
from thefuzz import fuzz
from knowledge_base import *


class PhraseAnalisys:
    def __init__(self, phrase: str):
        self.phrase = phrase.lower()
        self.correct_phrase()
        self.nlp = spacy.load("en_core_web_md")  # python -m spacy download en_core_web_md
        self.doc = self.nlp(self.phrase)
        self.tokenized_phrase = [word.text.lower() for word in self.doc]
        self.is_question = self.check_if_question()
        self.is_useful = False
        self.yesno = self.check_yesno()
        self.polarity = self.check_polarity()  # False is negative and True is positive
        self.useful_list = []
        self.number_errors = 0

    def correct_phrase(self) -> None:
        """
        Given a phrase, fuzzy-correct the name and the ingredients
        with the ones in the knowledge base (correct_words)
        :return: None
        """
        self.phrase = self.phrase.replace("?", " ?")
        max_wr = {}
        for wr in correct_words:
            for word in self.phrase.split():
                if fuzz.ratio(word, wr) > 80:
                    if wr not in max_wr or max_wr[wr][0] < fuzz.ratio(word, wr):
                        max_wr[wr] = (fuzz.ratio(word, wr), word)
        for wr in max_wr:
            self.phrase = self.phrase.replace(max_wr[wr][1], wr)
        self.number_errors = len([word for word in max_wr if word in plural_singular_possible_errors])

    def dependency_tree(self) -> dict:
        """
        Get the dependency tree for the phrase
        :return: A dict containing the dependency tree in the form: {word: (dep, head)}
        """
        return self.__parse(self.doc.to_json()["tokens"])

    def check_if_question(self) -> bool:
        """
        Check if the phrase is a question
        :return: True if the phrase is a question, False otherwise
        """
        if "?" in self.phrase or self.tokenized_phrase[0] in question_start_words:
            self.is_question = True
        else:
            self.is_question = False
        return self.is_question

    def check_polarity(self) -> bool:
        self.polarity = True
        for m in self.doc.to_json()["tokens"]:
            if m['morph'] == "Polarity=Neg" or m['dep'] == 'neg':
                self.polarity = False
            elif m['lemma'] == "no" and m['pos'] == "DET" and self.dependency_tree()['no'][1] in correct_words:
                self.polarity = False
        return self.polarity

    def check_if_useful(self) -> bool:
        """
        Check if the phrase contains any of the ingredients
        of the potions
        :return: True if the phrase contains any of the ingredients
        of the potions, False otherwise
        """
        useful = False
        for word in self.tokenized_phrase:
            if word in useful_words:
                useful = True
                self.useful_list.append(word)
            elif self.dependency_tree()[word][
                0] == "amod" and f"{word} {self.dependency_tree()[word][1]}" in useful_words:
                useful = True
                self.useful_list.append(f"{word} {self.dependency_tree()[word][1]}")
            elif self.dependency_tree()[word][
                0] == "poss" and f"{word}'s {self.dependency_tree()[word][1]}" in useful_words:
                useful = True
                self.useful_list.append(f"{word}'s {self.dependency_tree()[word][1]}")
            elif self.dependency_tree()[word][0] == "compound":
                first_word = self.dependency_tree()[word][1]
                compound_phrase = f"{word} {first_word}"
                while compound_phrase not in useful_words and self.dependency_tree()[first_word][0] == "compound":
                    first_word = self.dependency_tree()[first_word][1]
                    compound_phrase = f"{compound_phrase} {first_word}"
                if compound_phrase in useful_words:
                    useful = True
                    self.useful_list.append(compound_phrase)
        self.is_useful = useful
        return self.is_useful

    def ner(self) -> list:
        """
        Get the named entity recognition for the phrase
        :return: A dict containing the ner in the form: {word: ner}
        """
        return [(word.label_, word.text) for word in self.doc.ents]

    def __parse(self, json_dependency_tree) -> dict:
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

    def check_yesno(self):
        """
        Check if the phrase contains a yes or no question
        :return: "yes" if the phrase contains a yes question, "no" if the phrase contains a no question, None otherwise
        """
        if "yes" in self.tokenized_phrase:
            return "yes"
        elif "no" in self.tokenized_phrase:
            return "no"
        else:
            return None


if __name__ == "__main__":
    strin = PhraseAnalisys("I usually eat a lot of spders, I really like to eat a spder")
    print(strin.phrase)
    from pprint import pprint

    pprint(strin.doc.to_json())
    pprint(strin.dependency_tree())
    print(f"NER: {strin.ner()}")
    print(f"Is useful: {strin.check_if_useful()}")
    print(f"Polarity: {strin.check_polarity()}")
    print(f"Is question: {strin.check_if_question()}")
