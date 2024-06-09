from flask import Flask, render_template, request
import room_generator as rg
import character_sheet as cs
import monster_generator as mg
import rpg_tool as rt
import action_tools as at

app = Flask(__name__)

# Global variable to hold the current Room instance and the list of rooms
current_room = None
entered_rooms = []
current_monster = None
monster_caracteristics = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_room, entered_rooms, current_monster, monster_caracteristics

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
            prepare_monster_for_current_room()
            return render_page()
        elif 'previous_room' in request.form:
            room_index = int(request.form['previous_room'])
            current_room = entered_rooms[room_index]
            return render_page()
        elif 'aplayer_monster_action' in request.form:
            if request.form['aplayer_monster_action'] in cs.characteristics:
                characteristic = cs.characteristics[request.form['aplayer_monster_action']]
            else:
                characteristic = cs.characteristics['default']
            bonus = rt.get_characteristic_bonus(characteristic)
            result_dice = rt.roll_dice(20, bonus)
            result_num = result_dice[0] # Numerical roll dice result for the game.
            result_str = result_dice[1] # Text roll dice result for the player.
            result_str = result_str
            result_dice_monster = rt.roll_dice(20, 0)
            result_num_monster = result_dice_monster[0]
            effect_on_monster = current_monster.generate_player_action_effect(current_monster.monster_name_current, "Attack with a sword", result_num, result_num_monster)
            return render_template('action_result.html', result_str=result_str, effect_on_monster=effect_on_monster)
    else:
        if current_room is None:
            current_room = rg.Room()
            current_room.prepare_room()
            entered_rooms.append(current_room)
            prepare_monster_for_current_room()
        return render_page()

def prepare_monster_for_current_room():
    global current_monster, monster_caracteristics
    current_monster = mg.Monster()
    current_monster.monster_name_current = current_room.monster_current
    current_monster.prepare_monster()
    monster_caracteristics = current_monster.generate_monster_caracteristics(current_monster.monster_name_current)


def render_page(objDescription=None):
    return render_template('index.html', room_description=current_room.description_current,
                           objects=current_room.objects_current, doors=current_room.doors_current,
                           objDescription=objDescription, inventory=cs.inventory, entered_rooms=entered_rooms,
                           room_name=current_room.room_name_current, player_monster_actions=current_monster.player_monster_actions_list_current,
                           monster_caracteristics = monster_caracteristics
                           )

if __name__ == "__main__":
    app.run(debug=True)
