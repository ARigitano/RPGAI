from flask import Flask, render_template, request
import room_generator as rg
import character_sheet as cs

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'object' in request.form:
            obj_name = request.form['object']
            obj_description = rg.generate_object_description(obj_name)
            return render_template('index.html', room_description=rg.description_current, objects=rg.objects_current, doors=rg.doors_current, objDescription=obj_description, inventory=cs.inventory)
        elif 'pickup' in request.form:
            obj_name = request.form['pickup']
            cs.add_to_inventory(obj_name)
            rg.objects_current.remove(obj_name)
            return render_template('index.html', room_description=rg.description_current, objects=rg.objects_current, doors=rg.doors_current, inventory=cs.inventory)
        elif 'adoor' in request.form:
            rg.prepare_room()
            return render_template('index.html', room_description=rg.description_current, objects=rg.objects_current,
                                   doors=rg.doors_current, objDescription=None, inventory=cs.inventory)
    else:
        rg.prepare_room()
        return render_template('index.html', room_description=rg.description_current, objects=rg.objects_current, doors=rg.doors_current, objDescription=None)


if __name__ == "__main__":
    app.run(debug=True)
