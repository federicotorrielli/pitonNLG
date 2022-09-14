import math
import random

from colored import fg, stylize

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

    def __init__(self):
        self.analized_phrase: analisys.PhraseAnalisys = None
        self.current_answer = None
        self.potions = [polyjuice_potion, invisibility_potion, forgetfulness_potion]
        self.current_potion = random.choice(self.potions)
        self.max_turns = len(self.current_potion.ingredients) * 3
        self.memory = []
        self.user_memory = []
        self.current_frame = frame.Frame(self.current_potion, [])
        self.current_state = "intro"
        self.current_mental_state = random.choices(["neutral", "happy", "angry"], weights=[0.2, 0.1, 0.7])[0]
        self.__ingredient = ""
        self.hint = {"neutral": 0.5, "happy": 0.8, "angry": 0.2}
        self.trabocchetto = {"neutral": 0.5, "happy": 0.2, "angry": 0.7}
        self.turn = 1
        self.nlg_questions = language_generator.NaturalLanguageGenerator(self.current_mental_state, corpus_path=True)
        self.nlg_fillers = language_generator.NaturalLanguageGenerator(self.current_mental_state, corpus_path=False)
        self. neutral_intro_phrases = ["Welcome to the potions exam...\nI will ask you some questions about the potions you studied.",
                         "Welcome to the potion exam,\nI will ask you some "
                         "question about what i explained during the course"]
        self.happy_intro_phrases = ["I hope you enjoyed my potions course.\nI saw you very confident and I am glad "
                       "to see you are ready for the exam.\nLet's get started!",
                       "hello welcome to the potion exam,\nI've always seen you in class you "
                       "will surely be prepared, let's start with this question... "]
        self.angry_intro_phrases = ["Let's get this done quicky. I never saw you to my lessons, "
                       "so I don't see how you're going to pass this exam, but will give you one try only!",
                       "I can recognize an unprepared student right away,"
                       "\nI'll give you a chance this time, but let's hurry..."]

    def flow(self) -> None:
        """
        The main flow of the dialogue manager
        The dialogue ends when the frame is complete or after a certain number of turns (or time passed)
        """
        self.intro()
        self.wait_for_user_input()
        while not self.check_ending_condition():
            self.questions()
            self.wait_for_user_input()
            self.check_for_mood_change()
            self.turn += 1
        self.end()

    def intro(self) -> None:
        """
        Introduce the system
        """
        self.__print_and_mem("Hello, I'm Professor Piton.")
        if self.current_mental_state == "neutral":
            self.__print_and_mem(random.choice(self.neutral_intro_phrases))
        elif self.current_mental_state == "happy":
            self.__print_and_mem(random.choice(self.happy_intro_phrases))
        elif self.current_mental_state == "angry":
            self.__print_and_mem(random.choice(self.angry_intro_phrases))
        self.current_state = "questions"
        self.intro_generation()

    def intro_generation(self) -> None:
        """
        Generate the intro phrase for the current potion, then print it
        :return: None
        """
        if self.current_mental_state == "neutral":
            self.__print_and_mem(
                f"Tell me the ingredients of the {self.current_potion.get_name()}."
                f"\nYou should also tell me about the quantities... But it's up to you.")
        elif self.current_mental_state == "happy":
            self.__print_and_mem(
                f"As you will remember the training we did, the {self.current_potion.get_name()} "
                f"contains what ingredients?")
            self.__print_and_mem(f"I can give you an hint, if you want...")
        elif self.current_mental_state == "angry":
            self.__print_and_mem(
                f"Give me all the ingredients and the quantities of the {self.current_potion.get_name()}.")
    
    def __print_and_mem(self, phrase: str, user=False) -> None:
        """
        Print the phrase and memorize it
        """
        current_color = "light_blue" if self.current_mental_state == "neutral" else "green" \
            if self.current_mental_state == "happy" else "light_red"
        print(stylize(phrase, fg(current_color)))
        if user:
            self.user_memory.append(phrase)
        else:
            self.memory.append(phrase)
    
    def wait_for_user_input(self) -> None:
        """
        Wait for the user to input a phrase, and analyze it
        :return: None
        """
        self.current_answer = input()
        self.analized_phrase = analisys.PhraseAnalisys(self.current_answer)
        if self.current_state == "hint" or self.current_state == "trabocchetto":
            self.current_state = "not useful"
            while self.analized_phrase.yesno != "yes" and self.analized_phrase.yesno != "no":
                print("The question is easy, YOU MUST ANSWER YES OR NO!")
                self.current_answer = input()
                self.analized_phrase = analisys.PhraseAnalisys(self.current_answer)
            self.analized_phrase = analisys.PhraseAnalisys(self.resolve_yesno())
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

    def check_ending_condition(self) -> bool:
        """
        Check if the dialogue is over
        :return: True if the dialogue is over, False otherwise
        """
        return self.current_frame.check_complete() or self.turn > self.max_turns or self.doesnt_know()

    def doesnt_know(self) -> bool:
        """
        Check if the user doesn't know the ingredients
        :return: True if the user doesn't know the ingredients
        """
        not_know = False
        if not self.analized_phrase.polarity and not self.analized_phrase.is_useful:
            for w in ending_words:
                if w in self.analized_phrase.tokenized_phrase:
                    not_know = True
                    self.turn = self.max_turns  # We want to end the dialogue with the lowest score possible
        return not_know
    
    def questions(self) -> None:
        """
        Start the first question about a random potion, expect the first (incomplete,complete) answer
        """
        if self.analized_phrase.is_question:
            self.__print_and_mem("The only person here that can make the questions is me.")
            self.__print_and_mem(self.memory[len(self.memory) - 2])
        else:
            if self.current_state == "not useful":
                self.__print_and_mem("Silence. This is not what you are supposed to say to me.")
                self.__print_and_mem(self.memory[len(self.memory) - 2])
            else:
                self.__print_and_mem(self.generate_phrase())

    def generate_phrase(self) -> str:
        """
        Generates a phrase based on the current frame.
        It's either a question or a statement (filler).
        :return: the generated phrase
        """
        #self.current_frame.debug()
        choice = random.uniform(0, 1)
        if choice < 0.33:
            return self.generate_hint_pitfall_question()
        else:
            self.current_state = "questions"
            return self.generate_normal_question()

    def generate_hint_pitfall_question(self) -> str:
        """
        Generates a hint question for the user
        :return: the hint question
        """
        generated_phrase = self.nlg_questions.generate_sentence()
        temp_counter = 0
        for ingredient in useful_words:
            # If there's more than one ingredient, regenerate the sentence
            if ingredient.lower() in generated_phrase.lower():
                temp_counter += 1
            if temp_counter > 1:
                return self.generate_hint_pitfall_question()
        phrase_validity = False
        phrase_ingredient = False
        current_ingredient = ""
        for ingredient in useful_words:
            if ingredient in generated_phrase.lower():
                current_ingredient = ingredient
                if ingredient in self.current_potion.get_ingredients():
                    phrase_ingredient = True
                break
        if current_ingredient not in self.current_frame.ingredients and current_ingredient not \
                in self.current_frame.error_ingredients:
            phrase_validity = True
        if phrase_ingredient:
            choice = random.uniform(0, 1)
            if phrase_validity and choice < self.hint[self.current_mental_state]:
                self.current_state = "hint"
                self.__ingredient = current_ingredient
                return generated_phrase
            else:
                return self.generate_hint_pitfall_question()
        else:
            choice = random.uniform(0, 1)
            if choice < self.trabocchetto[self.current_mental_state]:
                return self.generate_hint_pitfall_question()  # Question him again
            else:
                self.current_state = "trabocchetto"
                self.__ingredient = current_ingredient
                return generated_phrase  # Trick question

    def generate_normal_question(self) -> str:
        """
        Generate a normal question for the user
        :return: the generated sentence
        """
        return self.nlg_fillers.generate_sentence()

    def end(self) -> None:
        """
        Calculate the grade with the following formula:
        grade = 31 - alpha * p where:
        - alpha = penalty multiplier (1.5 if the user is angry, 1 if neutral, 0.75 if happy)
        - p = #err + (#ext + #plur) / 2 + (3 * t - 3)
        - #err = # of errors
        - #ext = # of ingredients that are external to the potion (valid ingredients BUT not in the potion)
        - #plur = # of ingredients that the user wrongly said singular when they were plural (ex. spider -> spiders)
        - t = # of turns calculated as: # total turns / # of perfect turns (where the user said the correct ingredients)
        :return: None
        """
        if self.max_turns == self.turn:
            print("I will see you the next time. You did not pass the test.")
        else:
            t = self.current_frame.number_of_operations_made / len(self.current_frame.potion.ingredients)
            p = len(self.current_frame.error_ingredients) + (
                    len(self.current_frame.external_ingredients) + self.current_frame.wrongnumber) / 2 + (3 * t - 3)
            alpha = 1.5 if self.current_mental_state == "neutral" else (
                1.0 if self.current_mental_state == "happy" else 2)
            grade = math.floor(31 - alpha * p)
            if grade > 15:
                self.__print_and_mem(f"Your grade is {grade}...")
            self.generate_comment(grade)

    def resolve_yesno(self) -> str:
        self.current_state = "fill the frame"
        if self.analized_phrase.yesno == "yes":
            return f"I think that {self.__ingredient} is in the potion."
        elif self.analized_phrase.yesno == "no":
            return f"I don't think {self.__ingredient} is in the potion."

    def generate_comment(self, grade: int) -> None:
        """
        Generate a comment based on the grade and on the self.current_mental_state of piton
        :param grade: 
        :return: 
        """
        if self.current_mental_state == "happy":
            if grade > 27:
                self.__print_and_mem("Excellent job, my student. You are a genius!")
            elif grade >= 18:
                self.__print_and_mem("Good job, my student. You are a good one.\nI know you can do better but..."
                                     " well done.")
            elif grade < 18:
                self.__print_and_mem("Not your lucky day, I guess. I'm sorry. I hope you'll try again: you did not "
                                     "pass the exam.")
        elif self.current_mental_state == "neutral":
            if grade > 27:
                self.__print_and_mem("Good job. As required from a magic student.")
            elif grade >= 18:
                self.__print_and_mem("I don’t expect you will really understand the beauty of the softly "
                                     "simmering cauldron with its shimmering fumes, the delicate power of "
                                     "liquids that creep through human veins,"
                                     " bewitching the mind, ensnaring the senses...\n But you passed the test.")
            elif grade < 18:
                self.__print_and_mem("You have no subtlety, Student, You do not understand fine distinctions. "
                                     "It is one of the shortcomings that makes you such a lamentable potion-maker. "
                                     "Get out.")
        elif self.current_mental_state == "angry":
            if grade > 27:
                self.__print_and_mem("As required. You passed.")
            elif grade >= 18:
                self.__print_and_mem("You passed. Get out. The cauldron is not for you.")
            elif grade < 18:
                self.__print_and_mem("You failed. Get out. The cauldron is not for you.")

    def check_for_mood_change(self) -> None:
        """
        Change the current mental state (taken from the current_frame) of Piton if
        one of the following conditions is met:
        - Piton is happy and the number of operations made is greater then the potions ingredients number and the errors
          are greater than one --> neutral
        - Piton is neutral and he got right at least half of the potion's ingredients without
          making an error --> happy
        - Piton is neutral and he got (rightly or wrongly) at least half of the potion's ingredients and the sum
          of errors are at least half of the potions ingredients number --> angry
        - Piton is angry and he did nothing wrong --> neutral
        :return: None
        """
        if self.current_mental_state == "happy":
            if self.turn >= len(self.current_frame.potion.ingredients) \
                    and len(self.current_frame.error_ingredients) + len(self.current_frame.external_ingredients) > 1:
                self.current_mental_state = "neutral"

        elif self.current_mental_state == "neutral":
            if (len(self.current_frame.ingredients) * 2) > len(self.current_frame.potion.ingredients) + 1 and \
                    len(self.current_frame.error_ingredients) + len(self.current_frame.external_ingredients) == 0:
                self.current_mental_state = "happy"
            elif (self.turn * 2) > len(self.current_frame.potion.ingredients) + 1 and \
                    len(self.current_frame.error_ingredients) + len(self.current_frame.external_ingredients) \
                    >= len(self.current_frame.potion.ingredients) / 2:
                self.current_mental_state = "angry"

        else:
            if (len(self.current_frame.ingredients) + 1) == len(self.current_frame.potion.ingredients) and \
                    len(self.current_frame.error_ingredients) + len(self.current_frame.external_ingredients) == 0:
                self.current_mental_state = "neutral"

if __name__ == "__main__":
    dm = DialogueManager()
    dm.flow()
