from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

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
    text = response.choices[0].text.strip()
    room_description, objects_text = text.rsplit("objects = ", 1)
    objects = eval(objects_text)  # Assuming the format is always correct
    return room_description, objects

# Function to generate object description
def generate_object_description(obj_name):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Describe the following item the player found in a RPG dungeon: {obj_name}",
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        obj_name = request.form['object']
        obj_description = generate_object_description(obj_name)
        room_description = request.form['room_description']
        objects = eval(request.form['objects'])
        return render_template('index.html', room_description=room_description, objects=objects, objDescription=obj_description)
    else:
        room_description, objects = generate_room()
        return render_template('index.html', room_description=room_description, objects=objects, objDescription=None)

if __name__ == "__main__":
    app.run(debug=True)
