from flask import Flask
from flask_cors import CORS
import functions
import global_variables
import story
import endings

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Resets backend global values, in case the player starts a new game without restarting the server
@app.route('/reset_values')
def reset_values():
    functions.reset_basevalues()
    return {
        'result': 'gg'
    }


# Returns all story and ending texts
@app.route('/get_story')
def get_story():
    return {
        'story': story.story,
        'goodend': endings.goodend,
        'badend': endings.badend,
        'neutralend': endings.neutralend,
        'crashlanding': endings.explosion,
        'firstevent': story.firstevent
    }


# Creates a new player with the name received from the user, also checks if user with the same name already exists
@app.route('/newuser/<name>')
def create_user(name):
    global_variables.g_name = name
    return functions.create_new_user(name)


# Returns names of all users on the database for loading an old game
@app.route('/userlist')
def get_userlist():
    return functions.get_names()


# Fetch data associated with {username} from database, sets correct stats to the backend and returns stats displayed
# on the game window
@app.route('/olduser/<name>')
def load_game(name):
    info = functions.get_player_info(name)
    location = functions.get_location_info(info[4])
    global_variables.g_name = name
    global_variables.g_first_round = False
    global_variables.g_money = info[0]
    global_variables.g_charge_left = info[1]
    global_variables.g_karma = info[2]
    global_variables.g_rounds_left = info[3]
    global_variables.g_location = info[4]
    global_variables.g_visited_airports.append(global_variables.g_location)
    return {
        'money': info[0],
        'charge_left': info[1],
        'rounds_left': info[3],
        'location': location
    }


# Sends event texts and possible choices to front and processes event choices made by the player
@app.route('/event/<playerinput>/<process>')
def event(process, playerinput):
    if process == 'start':
        event, choice = functions.start_event()
        if choice:
            return {
                'eventtext': event[0],
                'choices':   event[1]
            }
        else:
            return {
                'eventtext': event[0],
                'choices': ''
            }

    if process == 'choice':
        functions.event_choice(playerinput)
        return {
            'result': 'choice completed'
        }


# Sends randomized airports and freights, processes choices made by the player regarding airports and freights, handles
# charging the plane's battery
@app.route('/airport/<playerinput>/<process>')
def airport_services(playerinput, process):
    if process == 'get_airports':
        airports = functions.get_airports()
        return airports
    if process == 'chosen_airport':
        global_variables.g_next_location = playerinput
        return {
            'success': 'True'
        }
    if process == 'get_freight':
        freights = functions.get_freight()
        return freights
    if process == 'chosen_freight':
        global_variables.g_profit = playerinput.split(',')[0]
        karma_to_add = playerinput.split(',')[1]
        global_variables.g_karma += int(karma_to_add)
        return {
            'success': 'True'
        }
    if process == 'charge_battery':
        battery_charge = functions.charge_battery()
        return battery_charge


# Handles ending the round, calculates battery usage, updates player's stats and checks if any game over condition has
# been triggered
@app.route('/endround')
def end_round():
    current_coords = functions.get_location_info(global_variables.g_location)[1:]
    next_coords = functions.get_location_info(global_variables.g_next_location)[1:]
    global_variables.g_charge_left = functions.calculate_battery_usage(global_variables.g_charge_left,
                                                                       current_coords,
                                                                       next_coords)
    global_variables.g_location = global_variables.g_next_location
    global_variables.g_money += int(global_variables.g_profit)
    global_variables.g_rounds_left -= 1

    if global_variables.g_charge_left <= 0:
        functions.player_deletion(global_variables.g_name)
        return {
            'result': 'crashed'
        }

    if global_variables.g_rounds_left == 0:
        functions.player_deletion(global_variables.g_name)
        # neutral ending
        if 75 >= global_variables.g_karma >= 25:
            return {
                'result': 'neutralend'
            }
        # bad ending
        elif global_variables.g_karma < 25:
            return {
                'result': 'badend'
            }
        # good ending
        elif global_variables.g_karma > 75:
            return {
                'result': 'goodend'
            }

    functions.update_database(global_variables.g_name, global_variables.g_money, global_variables.g_charge_left,
                              global_variables.g_rounds_left, global_variables.g_karma,
                              global_variables.g_location)
    return {
        'result': 'Game saved'
    }


# Sends player's stats displayed in the game window
@app.route('/getdata')
def getdata():
    return {
        'money': global_variables.g_money,
        'charge_left': global_variables.g_charge_left,
        'rounds_left': global_variables.g_rounds_left,
        'location': global_variables.g_location
    }


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)


# Address for testing 127.0.0.1:3000/
