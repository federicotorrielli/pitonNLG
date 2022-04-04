from knowledge_base import *
import potion
import random


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
        self.potions = [polyjuice_potion, invisibility_potion, forgetfulness_potion]
        self.memory = []  # TODO: add a memory of the previous phrases
        self.current_frame = {}
        self.current_state = "intro"
        self.current_mental_state = "neutral"
        self.current_grade = 1
        self.current_comment = ""
        self.current_potion = None

    def intro(self):
        """
        Introduce the system
        """
        print("Hello, I'm Professor Piton.")
        self.set_mental_state()
        if self.current_mental_state == "neutral":
            print(random.choice(neutral_intro_phrases))
        elif self.current_mental_state == "happy":
            print(random.choice(happy_intro_phrases))
        elif self.current_mental_state == "angry":
            print(random.choice(angry_intro_phrases))
        self.current_state = "questions"

    def questions(self):
        """
        Start the first question about a random potion, expect the first (incomplete,complete) answer
        """
        self.current_potion = random.choice(self.potions)
        if self.current_mental_state == "neutral":
            print(f"Tell me the ingredients of the {self.current_potion.get_name()}.\nYou should also tell me about the quantities... But it's up to you.")
        elif self.current_mental_state == "happy":
            print(f"As you will remember the training we did, the {self.current_potion.get_name()} contains what ingredients?")
            print(f"I can give you an hint, if you want...")
        elif self.current_mental_state == "angry":
            print(f"Give me all the ingredients and the quantities of the {self.current_potion.get_name()}.")

    def hint(self):
        """
        Give a hint about the missing ingredients
        """
        a_missing_ingredient = random.choice(self.current_potion.get_missing_ingredients(self.current_frame.keys()))
        if self.current_mental_state == "happy":
            print(f"Here is a hint... one of the missing ingredients is: {a_missing_ingredient}")
        elif self.current_mental_state == "neutral":
            print(random.choice([f"Here is a hint... one of the missing ingredients is: {a_missing_ingredient}",
                                 "I'm sure you can guess what is missing..."]))
        elif self.current_mental_state == "angry":
            print("No. I will not.")


    def set_mental_state(self):
        """
        Set the mental state of the DM taken randomly from a string list
        """
        self.current_mental_state = random.choices(["neutral", "happy", "angry"], weights=[0.2, 0.1, 0.7])
