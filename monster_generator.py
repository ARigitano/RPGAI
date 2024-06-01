import call_openai as co

# Function to generate a list of actions for the player toward the monster
def generate_player_actions(monster):
    prompt = ("The player is in front of this monster: {monster}."
                "List three actions he can choose between to deal with the monster."
                "Each time the description contains an action for the player, add the action as a string in the python list actions "
                "Finish the description with the list: actions = ['action1', ..., 'actionn']")
    return co.call_openai_api(prompt, max_tokens=100)

