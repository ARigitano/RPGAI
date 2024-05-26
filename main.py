from flask import Flask, render_template, request
import room_generator as rg
import character_sheet as cs

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        room_description = request.form['room_description']
        objects = eval(request.form['objects'])
        if 'object' in request.form:
            obj_name = request.form['object']
            obj_description = rg.generate_object_description(obj_name)
            inventory = cs.get_inventory()
            return render_template('index.html', room_description=room_description, objects=objects, objDescription=obj_description, inventory=inventory)
        elif 'pickup' in request.form:
            obj_name = request.form['pickup']
            cs.add_to_inventory(obj_name)
            inventory = cs.get_inventory()
            objects.remove(obj_name)
            return render_template('index.html', room_description=room_description, objects=objects, inventory=inventory)
    else:
        room_description = rg.generate_room()
        room_description = room_description.replace("Objects", "objects")
        room_description = room_description.replace("Doors", "doors")
        objects = rg.extract_objects(room_description)
        doors = rg.extract_doors(room_description)
        return render_template('index.html', room_description=room_description, objects=objects, doors=doors, objDescription=None)


if __name__ == "__main__":
    app.run(debug=True)
