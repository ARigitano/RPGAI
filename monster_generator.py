import call_openai as co
import generation_tools as gt

class Monster:

    def __init__(self):
        self.player_monster_actions_current = ""
        self.player_monster_actions_list_current = []
        self.monster_name_current = ""

    def prepare_monster(self):
        self.player_monster_actions_current = self.generate_player_actions(self.monster_name_current)
        self.player_monster_actions_current = self.player_monster_actions_current.replace("Actions", "actions")
        self.player_monster_actions_list_current = gt.extract_elements(self.player_monster_actions_current, "actions")

    # Function to generate a list of actions for the player toward the monster
    def generate_player_actions(self, monster):
        prompt = ("The player is in front of this monster: {monster}."
                    "List three actions he can choose between to deal with the monster."
                    "Each time the description contains an action for the player, add the action as a string in the python list actions "
                    "Finish the description with the list: actions = ['action1', ..., 'actionn']")
        return co.call_openai_api(prompt, max_tokens=100)