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

    return response.choices[0].text.strip()

app = Flask(__name__)

@app.route('/')
def index():
    room_description = describe_dungeon_room()
    return render_template("index.html", room_description = room_description)

if __name__ == "__main__":
    app.run(debug=True)
