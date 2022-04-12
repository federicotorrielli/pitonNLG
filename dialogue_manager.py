import random

import analisys
import frame
import language_generator
from knowledge_base import *


class DialogueManager:
    """
    Dialogue Manager for the PitonNLG project:
    - The system will take initiative in the conversation
    - It is FRAME-BASED: every potion is represented as a frame
      to be filled with ingredients (common ground)
    - The DialogueMananger will ask the user the ingredients that
      miss from the potions, proposing true/false statements
    - At the end of the conversation, a grade and a comment must be stated
    - Backup-strategy needed in case of other dialogue
    - It has to keep memory of the previous phrases told to the DM
    """
    # TODO: check plurale o singolare ingredienti
    # TODO: generazione ending e voto...
    # TODO: check iterazioni strane (es. "no", "yes")

    def __init__(self, max_turns=15):
        self.max_turns = max_turns
        self.analized_phrase = None
        self.current_answer = None
        self.potions = [polyjuice_potion, invisibility_potion, forgetfulness_potion]
        self.current_potion = random.choice(self.potions)
        self.memory = []
        self.user_memory = []
        self.current_frame = frame.Frame(self.current_potion, [])
        self.current_state = "intro"
        self.current_mental_state = random.choices(["neutral", "happy", "angry"], weights=[0.2, 0.1, 0.7])[0]
        self.hint = {"neutral": 0.5, "happy": 0.8, "angry": 0.2}
        self.trabocchetto = {"neutral": 0.5, "happy": 0.2, "angry": 0.7}
        self.current_grade = 1
        self.current_comment = ""
        self.turn = 1
        self.nlg_questions = language_generator.NaturalLanguageGenerator(corpus_path="corpus_potion_questions.txt")
        self.nlg_fillers = language_generator.NaturalLanguageGenerator(corpus_path="corpus_filler_phrases.txt")

    def flow(self):
        """
        The main flow of the dialogue manager
        The dialogue ends when the frame is complete or after a certain number of turns (or time passed)
        """
        self.intro()
        self.wait_for_user_input()
        while not self.check_ending_condition():
            self.questions()
            self.wait_for_user_input()
            self.turn += 1
        self.end()

    def intro(self):
        """
        Introduce the system
        """
        self.__print_and_mem("Hello, I'm Professor Piton.")
        if self.current_mental_state == "neutral":
            self.__print_and_mem(random.choice(neutral_intro_phrases))
        elif self.current_mental_state == "happy":
            self.__print_and_mem(random.choice(happy_intro_phrases))
        elif self.current_mental_state == "angry":
            self.__print_and_mem(random.choice(angry_intro_phrases))
        self.current_state = "questions"
        self.intro_generation()

    def questions(self):
        """
        Start the first question about a random potion, expect the first (incomplete,complete) answer
        """
        if self.analized_phrase.is_question:
            self.__print_and_mem("The only person here that can make the questions is me.")
        else:
            if self.current_state == "not useful":
                self.__print_and_mem("Silence. This is not what you are supposed to say to me.")
                self.__print_and_mem(self.memory[len(self.memory) - 2])
            else:
                self.__print_and_mem(self.generate_phrase())

    def __print_and_mem(self, phrase, user=False):
        """
        Print the phrase and memorize it
        """
        print(phrase)
        if user:
            self.user_memory.append(phrase)
        else:
            self.memory.append(phrase)

    def intro_generation(self):
        if self.current_mental_state == "neutral":
            self.__print_and_mem(
                f"Tell me the ingredients of the {self.current_potion.get_name()}.\nYou should also tell me about the quantities... But it's up to you.")
        elif self.current_mental_state == "happy":
            self.__print_and_mem(
                f"As you will remember the training we did, the {self.current_potion.get_name()} contains what ingredients?")
            self.__print_and_mem(f"I can give you an hint, if you want...")
        elif self.current_mental_state == "angry":
            self.__print_and_mem(
                f"Give me all the ingredients and the quantities of the {self.current_potion.get_name()}.")

    def end(self):
        """
        Gives the user the grade and the comment
        """
        print(f"Fine del cazzo {self.turn}")
        pass

    def check_ending_condition(self):
        return self.current_frame.check_complete() or self.turn > self.max_turns or self.non_sa()

    def non_sa(self):
        not_know = False
        if not self.analized_phrase.polarity and not self.analized_phrase.is_useful:
            for w in ending_words:
                if w in self.analized_phrase.tokenized_phrase:
                    not_know = True
        return not_know

    def wait_for_user_input(self):
        self.current_answer = input()
        self.analized_phrase = analisys.PhraseAnalisys(self.current_answer)
        if self.analized_phrase.check_if_useful():
            self.current_state = "fill the frame"
            if not self.analized_phrase.is_question:
                ingredients_to_add = set([])
                bool_list = []
                for ingredient in self.analized_phrase.useful_list:
                    ingredients_to_add.add(ingredient)
                    bool_list.append(self.analized_phrase.polarity)
                self.current_frame.add_ingredients(ingredients_to_add, bool_list)
        else:
            self.current_state = "not useful"
        self.user_memory.append(self.current_answer)

    def generate_phrase(self):
        self.current_frame.debug()
        choice = random.uniform(0, 1)
        if choice < self.hint[self.current_mental_state]:
            return self.generate_hint_question()
        else:
            return self.generate_filler()

    def generate_hint_question(self):
        generated_phrase = self.nlg_questions.generate_sentence()
        phrase_validity = True
        phrase_ingredient = False
        current_ingredient = ""
        for ingredient in self.current_potion.get_ingredients():
            if ingredient in generated_phrase.lower():
                phrase_ingredient = True
                current_ingredient = ingredient
                break
        if current_ingredient not in self.current_frame.ingredients and current_ingredient not in self.current_frame.error_ingredients:
            phrase_validity = True
        if phrase_ingredient:
            if phrase_validity:
                return generated_phrase
            else:
                return self.generate_hint_question()
        else:
            choice = random.uniform(0, 1)
            print(choice)
            if choice < self.trabocchetto[self.current_mental_state]:
                return self.generate_hint_question()  # Riformulo domanda
            else:
                return generated_phrase  # Domanda trabocchetto

    def generate_filler(self):
        return self.nlg_fillers.generate_sentence()


if __name__ == "__main__":
    dm = DialogueManager()
    dm.flow()
