from flask import Flask, render_template, request
from room_generator import Room
import character_sheet as cs

app = Flask(__name__)

# Create a global variable to hold the current Room instance
current_room = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global current_room

    if request.method == 'POST':
        if 'object' in request.form:
            obj_name = request.form['object']
            obj_description = current_room.generate_object_description(obj_name)
            return render_template('index.html', room_description=current_room.description_current, objects=current_room.objects_current, doors=current_room.doors_current, objDescription=obj_description, inventory=cs.inventory)
        elif 'pickup' in request.form:
            obj_name = request.form['pickup']
            cs.add_to_inventory(obj_name)
            current_room.objects_current.remove(obj_name)
            return render_template('index.html', room_description=current_room.description_current, objects=current_room.objects_current, doors=current_room.doors_current, inventory=cs.inventory)
        elif 'adoor' in request.form:
            current_room = Room()
            current_room.prepare_room()
            return render_template('index.html', room_description=current_room.description_current, objects=current_room.objects_current, doors=current_room.doors_current, objDescription=None, inventory=cs.inventory)
    else:
        current_room = Room()
        current_room.prepare_room()
        return render_template('index.html', room_description=current_room.description_current, objects=current_room.objects_current, doors=current_room.doors_current, objDescription=None)


if __name__ == "__main__":
    app.run(debug=True)
