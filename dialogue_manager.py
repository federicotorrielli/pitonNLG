from known_potions import *
import potion


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
        self.memory = []  # TODO: add a memory of the previous phrases
        self.current_frame = {}
        self.current_grade = 0
        self.current_comment = ""
