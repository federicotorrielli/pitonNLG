import potion

polyjuice_potion = potion.Potion("Polyjuice Potion",
                                 {"Fluxweed": 1, "Knotgrass": 1, "Lacewing Fly": 3, "Leeches": 2, "Horn of Bicorn": 1,
                                  "Boomslang Skin": 1, "Hair": 1})
invisibility_potion = potion.Potion("Invisibility Potion", {"Cherry": 5, "Chicken": 1, "Spider": 3})
forgetfulness_potion = potion.Potion("Forgetfulness Potion",
                                     {"Lether River Water": 2, "Valierian Spring": 2, "Standard Ingredient": 2,
                                      "Mistletoe Berry": 4})

neutral_intro_phrases = ["Welcome to the potions exam...\nI will ask you some questions about the potions you studied.", "Welcome to the potion exam,\n i will ask you some question about what i explained during the course"]
happy_intro_phrases = ["I hope you enjoyed my potions course.\nI saw you very confident and I am glad to see you are ready for the exam.\nLet's get started!", "hello welcome to the potion exam,\n i've always seen you in class you will surely be prepared, let's start with this question... "]
angry_intro_phrases = ["Let's get this done quicky. I never saw you to my lessons, so I don't see how you're going to pass this exam, but will give you one try only.", "I can recognize an unprepared student right away,\n I'll give you a chance this time, but let's hurry..."]