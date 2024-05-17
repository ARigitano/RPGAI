from openai import OpenAI
import os
from flask import Flask, render_template, url_for, request, redirect

# Read the API key from the text file
api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
with open(api_key_file, 'r') as f:
    OPENAI_API_KEY = f.read().strip()

client = OpenAI(api_key=OPENAI_API_KEY)


# Function to describe a dungeon room
def describe_dungeon_room():
    # Prompt the AI to describe the room the player just entered
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model as needed
        prompt="The player enters a dungeon room. "
               "Describe the room. "
               "Each time the description contains an object the player could put in his inventory, add the object as a string in the python list objects. "
               "Finish the description with the list: objects = ['item1', ..., 'itemn']",
        max_tokens=300,
        temperature=0.5
    )

    # Function to describe an object
    def generate_object_description(object_name):
        # Prompt the AI to describe the room the player just entered
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  # Adjust the model as needed
            prompt=""
                   f"Describe the following item the player found in a RPG dungeon: {object_name}",
            max_tokens=100,
            temperature=0.5
        )

    return response.choices[0].text.strip()

#Extract a list of pickable objects from the room description.
def extract_objects(description):
    start_index = description.find("objects = [")
    end_index = description.find("]", start_index)

    if start_index != -1 and end_index != -1:
        objects_str = description[start_index + len("objects = ["):end_index]
        objects = [obj.strip("'\" ") for obj in objects_str.split(",")]
        return objects
    else:
        return None


app = Flask(__name__)

@app.route('/')
def index():
    room_description = describe_dungeon_room()
    objects = extract_objects(room_description)
    return render_template("index.html", room_description = room_description, objects=objects)

@app.route('/description', methods=['POST'])
def get_description():
    # Get the object name from the request
    object_name = request.json['objectName']
    # Generate the description for the object using the AI (replace this with your actual AI logic)
    object_description = generate_object_description(object_name)
    # Return the description as a response
    return object_description

if __name__ == "__main__":
    app.run(debug=True)
