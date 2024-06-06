from flask import Flask, render_template, request
import room_generator as rg
import character_sheet as cs
import monster_generator as mg
import rpg_tool as rt

app = Flask(__name__)

# Global variable to hold the current Room instance and the list of rooms
current_room = None
entered_rooms = []
current_monster = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_room, entered_rooms, current_monster

    # Handles the actions of the player
    if request.method == 'POST':
        if 'object' in request.form:
            obj_name = request.form['object']
            obj_description = current_room.generate_object_description(obj_name)
            return render_page(objDescription=obj_description)
        elif 'pickup' in request.form:
            obj_name = request.form['pickup']
            cs.add_to_inventory(obj_name)
            current_room.objects_current.remove(obj_name)
            return render_page()
        elif 'adoor' in request.form:
            door_name = request.form['adoor']
            if door_name in current_room.connections:
                current_room = current_room.connections[door_name]
            else:
                new_room = rg.Room()
                new_room.prepare_room()
                current_room.connections[door_name] = new_room
                entered_rooms.append(new_room)
                current_room = new_room
            return render_page()
        elif 'previous_room' in request.form:
            room_index = int(request.form['previous_room'])
            current_room = entered_rooms[room_index]
            return render_page()
        elif 'aplayer_monster_action' in request.form:
            characteristic = cs.characteristics[request.form['aplayer_monster_action']]
            result_dice = rt.roll_dice_without_characteristic(20)
            bonus = rt.get_characterictic_bonus(characteristic)
            total = result_dice + bonus
            result_str = f"You roll the dice: {result_dice} + {bonus} = {total}"

            return str(result_str)

    else:
        current_room = rg.Room()
        current_room.prepare_room()
        entered_rooms.append(current_room)
        current_monster = mg.Monster()
        current_monster.monster_name_current = current_room.monster_current
        current_monster.prepare_monster()
        return render_page()

def render_page(objDescription=None):
    return render_template('index.html', room_description=current_room.description_current,
                           objects=current_room.objects_current, doors=current_room.doors_current,
                           objDescription=objDescription, inventory=cs.inventory, entered_rooms=entered_rooms,
                           room_name=current_room.room_name_current, player_monster_actions=current_monster.player_monster_actions_list_current
                           )

if __name__ == "__main__":
    app.run(debug=True)
