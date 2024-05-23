from openai import OpenAI
import os

# Read the API key from the text file
api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
with open(api_key_file, 'r') as f:
    OPENAI_API_KEY = f.read().strip()

client = OpenAI(api_key=OPENAI_API_KEY)


# Function to generate room description and objects
def generate_room():
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="The player enters a dungeon room. "
               "Describe the room. "
               "Each time the description contains an object the player could put in his inventory, add the object as a string in the python list objects. "
               "Finish the description with the list: objects = ['item1', ..., 'itemn']",
        max_tokens=256,
        temperature=0.7
    )

    return response.choices[0].text.strip()


# Extract a list of pickable objects from the room description.
def extract_objects(description):
    start_index = description.find("objects = [")
    end_index = description.find("]", start_index)

    if start_index != -1 and end_index != -1:
        objects_str = description[start_index + len("objects = ["):end_index]
        objects = [obj.strip("'\" ") for obj in objects_str.split(",")]
        return objects
    else:
        return []


# Function to generate object description
def generate_object_description(obj_name):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Very briefly describe the following item the player found in a RPG dungeon: {obj_name}",
        max_tokens=100,
        temperature=0.7
    )

    return response.choices[0].text.strip()
