import random

import analisys
import frame
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
        self.current_grade = 1
        self.current_comment = ""
        self.turn = 1

    def flow(self):
        """
        The main flow of the dialogue manager
        The dialogue ends when the frame is complete or after a certain number of turns (or time passed)
        """
        self.intro()
        while self.current_state != self.check_ending_condition():
            self.wait_for_user_input()
            self.questions()
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
                ingredients_to_add = set([])
                bool_list = []
                for ingredient in self.analized_phrase.useful_list:
                    ingredients_to_add.add(ingredient)
                    bool_list.append(self.analized_phrase.polarity)
                self.current_frame.add_ingredients(ingredients_to_add, bool_list)

                # TODO: qua dobbiamo generare la frase
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

    def hint(self):
        """
        Give a hint about the missing ingredients
        """
        a_missing_ingredient = random.choice(
            self.current_potion.get_missing_ingredients(self.current_frame.ingredients))
        if self.current_mental_state == "happy":
            self.__print_and_mem(f"Here is a hint... one of the missing ingredients is: {a_missing_ingredient}")
        elif self.current_mental_state == "neutral":
            self.__print_and_mem(
                random.choice([f"Here is a hint... one of the missing ingredients is: {a_missing_ingredient}",
                               "I'm sure you can guess what is missing..."]))
        elif self.current_mental_state == "angry":
            self.__print_and_mem("No. I will not.")

    def end(self):
        """
        Gives the user the grade and the comment
        """
        pass

    def check_ending_condition(self):
        # TODO: dovremmo controllare anche magari se l'utente ha detto una cosa del tipo "non so niente..."
        return self.current_frame.is_complete or self.turn > self.max_turns

    def wait_for_user_input(self):
        self.current_answer = input()
        self.analized_phrase = analisys.PhraseAnalisys(self.current_answer)
        if self.analized_phrase.check_if_useful():
            self.current_state = "fill the frame"
        else:
            self.current_state = "not useful"
        self.user_memory.append(self.current_answer)

    def generate_phrase(self):
        # TODO: stub
        self.current_frame.debug()
        return "Are there any spiders in the potion?"


if __name__ == "__main__":
    dm = DialogueManager()
    dm.flow()
