from openai import OpenAI
import os


class Room:
    def __init__(self):
        # Read the API key from the text file
        api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
        with open(api_key_file, 'r') as f:
            self.OPENAI_API_KEY = f.read().strip()

        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.description_current = ""
        self.objects_current = []
        self.doors_current = []

    def prepare_room(self):
        self.description_current = self.generate_room()
        self.description_current = self.description_current.replace("Objects", "objects")
        self.description_current = self.description_current.replace("Doors", "doors")
        self.objects_current = self.extract_objects(self.description_current)
        self.doors_current = self.extract_doors(self.description_current)

    # Function to generate room description and objects
    def generate_room(self):
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="The player enters a dungeon room. "
                   "Describe the room in 75 to 100 words. "
                   "Each time the description contains an object the player could put in his inventory, add the object as a string in the python list objects. "
                   "Finish the description with the list: objects = ['item1', ..., 'itemn']"
                   "Each time the description contains a door the player could go through, add the door as a string in the python list doors. "
                   "Finish the description with the list: doors = ['door1', ..., 'doorn']",
            max_tokens=400,
            temperature=0.7
        )

        return response.choices[0].text.strip()

    # Extract a list of pickable objects from the room description.
    def extract_objects(self, description):
        start_index = description.find("objects = [")
        end_index = description.find("]", start_index)

        if start_index != -1 and end_index != -1:
            objects_str = description[start_index + len("objects = ["):end_index]
            objects = [obj.strip("'\" ") for obj in objects_str.split(",")]
            return objects
        else:
            return []

    # Extract a list of doors from the room description.
    def extract_doors(self, description):
        start_index = description.find("doors = [")
        end_index = description.find("]", start_index)

        if start_index != -1 and end_index != -1:
            doors_str = description[start_index + len("doors = ["):end_index]
            doors = [door.strip("'\" ") for door in doors_str.split(",")]
            return doors
        else:
            return []

    # Function to generate object description
    def generate_object_description(self, obj_name):
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Very briefly describe the following item the player found in a RPG dungeon: {obj_name}",
            max_tokens=100,
            temperature=0.7
        )

        return response.choices[0].text.strip()




