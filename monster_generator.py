import call_openai as co
import generation_tools as gt

class Monster:

    def __init__(self):
        self.player_monster_actions_current = ""
        self.player_monster_actions_list_current = []
        self.monster_name_current = ""
        self.health = 0
        self.armor_save = 0

    def prepare_monster(self):
        self.player_monster_actions_current = self.generate_player_actions(self.monster_name_current)
        self.player_monster_actions_current = self.player_monster_actions_current.replace("Actions", "actions")
        self.player_monster_actions_list_current = gt.extract_actions_and_characteristics(self.player_monster_actions_current)

    def generate_monster_caracteristics(self, monster):
        prompt = (f"Generate the following caracteristics of this monster from Dungeons & Dragons 3: {monster}."
                  "Write health = [Give the appropriate number of health]"
                  "Write armor class = [Give the appropriate number of armor class]"
                  )
        return co.call_openai_api(prompt, max_tokens=100)

    # Function to generate a list of actions for the player toward the monster
    def generate_player_actions(self, monster):
        prompt = (f"The player is in front of this monster: {monster}."
                    "List three actions he can choose between to deal with the monster."
                    "Each time the description contains an action for the player, add the action as a string in the python list actions."
                    "At the end of each action, write in parenthesis if the action which characteristic from the player will be used for that action,"
                    "between strength, constitution, dexterity,  intelligence, wisdom or charisma."
                    "Finish the description with the list: actions = ['action1', ..., 'actionn']")
        return co.call_openai_api(prompt, max_tokens=100)

    def generate_player_action_effect(self, monster, action, player_dice_roll, monster_dice_roll):
        prompt = (f"The player did {action} on the {monster}."
                  f"The player rolled a dice and got this result: {player_dice_roll}."
                  f"The {monster} rolled a resistance dice and go this result: {monster_dice_roll}."
                  f"If the player's dice roll is superior to the {monster} dice roll, the player's 'action succeeds."
                  f"But if the {monster}'s dice roll is superior to the player's dice roll, then the player's action fails."
                  f"Considering these dice rolls, describe what happens."
                  f"Don not describe more than a single action from the player."
                  )
        return co.call_openai_api(prompt, max_tokens=100)

