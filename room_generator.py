import call_openai as co

class Room:
    room_counter = 0

    def __init__(self):
        self.id = Room.room_counter
        Room.room_counter += 1
        self.room_name_current = ""
        self.description_current = ""
        self.objects_current = []
        self.doors_current = []
        self.monster_current = []
        self.connections = {}

    def prepare_room(self):
        self.description_current = self.generate_room()
        self.room_name_current = self.generate_room_name(self.description_current)
        self.description_current = self.description_current.replace("Objects", "objects")
        self.description_current = self.description_current.replace("Doors", "doors")
        self.description_current = self.description_current.replace("Monster", "monster")
        self.objects_current = self.extract_elements(self.description_current, "objects")
        self.doors_current = self.extract_elements(self.description_current, "doors")
        self.monster_current = self.extract_elements(self.description_current, "monster")

    def generate_room(self):
        prompt = ("The player enters a dungeon room. "
                  "Describe the room in 75 to 100 words. "
                  "Each time the description contains an object the player could put in his inventory, add the object as a string in the python list objects. "
                  "Finish the description with the list: objects = ['item1', ..., 'itemn']"
                  "Each time the description contains a door the player could go through, add the door as a string in the python list doors. "
                  "Finish the description with the list: doors = ['door1', ..., 'doorn']"
                  "If the description contains a monster, add the monster as a string in the python list monster. "
                  "Finish the description with the list: monster = ['monster']")
        return co.call_openai_api(prompt, max_tokens=400)

    def generate_room_name(self, description):
        prompt = f"Generate a name for a dungeon room that fits that description: {description}"
        return co.call_openai_api(prompt, max_tokens=50)

    def extract_elements(self, description, element_name):
        start_index = description.find(f"{element_name} = [")
        end_index = description.find("]", start_index)

        if start_index != -1 and end_index != -1:
            elements_str = description[start_index + len(f"{element_name} = ["):end_index]
            elements = [elem.strip("'\" ") for elem in elements_str.split(",")]
            return elements
        else:
            return []

    def generate_object_description(self, obj_name):
        prompt = f"Very briefly describe the following item the player found in a RPG dungeon: {obj_name}"
        return co.call_openai_api(prompt, max_tokens=100)






