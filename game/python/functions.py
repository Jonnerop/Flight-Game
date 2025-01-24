import geopy.distance
import random
from time import sleep
import mysql.connector
from global_variables import (g_freight_name, g_freight_price, g_freight_karma, g_difficulty, usedevents)
import global_variables


databaseconnect = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="lentopeli",
    user="root",
    password="password",
    autocommit=True
)


# Fetches names of all previous players from the database, needed for continuing the game
def get_names():
    sql = "select screen_name from game"
    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    names = cursor.fetchall()
    if len(names) < 1:
        return {
            'success': False
        }
    else:
        return {
            'success': True,
            'names': names
        }


# Deletes player from the database, happens after every type of ending
def player_deletion(screen_name):
    sql = "delete from game where screen_name = '"+screen_name+"'"
    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    return


# Resets global values to default if the player plays several games without resetting the server
def reset_basevalues():
    global_variables.g_karma = 50
    global_variables.g_rounds_left = 5
    global_variables.g_charge_left = 100
    global_variables.g_full_charge = 100
    global_variables.g_cost_of_charging = 20000
    global_variables.g_money = 0
    global_variables.g_profit = 0
    global_variables.g_location = "efhk"
    global_variables.g_next_location = "ldri"
    global_variables.g_distance = 0
    global_variables.usedevents = []
    global_variables.g_first_round = True
    global_variables.g_player_alive = True
    global_variables.g_visited_airports = []
    return


# Calculates battery usage during the round ending procedures
def calculate_battery_usage(remaining_percentage, current_airport, chosen_airport):
    # calculate the distance in km using coordinates
    distance_km = geopy.distance.distance(current_airport, chosen_airport).km
    # calculate the initial battery capacity, 100% charge lasts for 4000 km
    initial_capacity_km = global_variables.g_maxrange
    # calculate the remaining battery capacity in km
    remaining_capacity_km = (remaining_percentage / 100) * initial_capacity_km
    # calculate the remaining battery capacity after the flight
    remaining_capacity_km = remaining_capacity_km - distance_km
    # calculate the remaining battery percentage after the flight
    remaining_percentage = (remaining_capacity_km / initial_capacity_km) * 100
    remaining_percentage = round(remaining_percentage)
    return remaining_percentage


# Randomizes 5 different numbers (for getting 5 different freights in get_freight() function)
def randomize_freight():
    freight_index = []
    while len(freight_index) < 5:
        random_number = random.randint(0, 9)
        if random_number not in freight_index:
            freight_index.append(random_number)
    return freight_index


# Uses previously randomized 5 numbers to pick 5 freights from list, calculates price for these freights based on
# distance and game difficulty and rounds the number to hundreds, then makes json object of each freight, adds them into
# a list and returns that
def get_freight():
    freights = randomize_freight()
    json_freights = []

    for opt in range(0, len(freights)):
        travel_distance = calc_distance(get_location_info(global_variables.g_location)[1:],
                                        get_location_info(global_variables.g_next_location)[1:])
        adj_freight_price = g_freight_price[freights[opt]]*travel_distance/g_difficulty
        rounded_freight_price = round(adj_freight_price/100)*100

        one_freight = {
            'name': g_freight_name[freights[opt]],
            'price': rounded_freight_price,
            'karma': g_freight_karma[freights[opt]]
        }
        json_freights.append(one_freight)

    return json_freights


# Fetches name, lat and lon of an airport from database, used for calculating distances or coordinates for map etc
def get_location_info(icao):
    sql = "select name, latitude_deg, longitude_deg from airport where ident = '"+icao+"'"
    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    location_info = cursor.fetchall()
    return location_info[0]


# Checks whether the player has already full battery or enough money for charging their battery, returns information
# whether the procedure was completed or not
def charge_battery():
    if global_variables.g_charge_left == global_variables.g_full_charge:
        return {
            'money': global_variables.g_money,
            'charge_left': global_variables.g_charge_left,
            'text': "Your battery is already fully charged"
        }
    elif global_variables.g_money >= global_variables.g_cost_of_charging:
        global_variables.g_money -= global_variables.g_cost_of_charging
        global_variables.g_charge_left = global_variables.g_full_charge
        return {
            'money': global_variables.g_money,
            'charge_left': global_variables.g_charge_left,
            'text': "Battery charged successfully"
        }
    else:
        return {
            'money': global_variables.g_money,
            'charge_left': global_variables.g_charge_left,
            'text': "Insufficient funds"
        }


# Calculates distance with coordinates
def calc_distance(current_airport, other_airport):
    current = (current_airport[0], current_airport[1])
    other = (other_airport[0], other_airport[1])
    distance = geopy.distance.distance(current, other).km

    return distance


# Randomizes 5 airports not yet visited by the player, makes a json object of each airport's information and adds them
# into a list and returns that
def get_airports():
    while True:
        sql = "SELECT ident, name, continent, country_name, latitude_deg, longitude_deg "
        sql += "FROM airport WHERE continent = 'EU' AND type='large_airport' "
        sql += "AND country_name NOT LIKE 'Russia'"
        sql += "AND name NOT LIKE '%?%' ORDER by RAND() limit 5;"
        cursor = databaseconnect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in global_variables.g_visited_airports:
            if i in result:
                continue
        break
    full_result = []
    for row in result:
        distance = calc_distance(get_location_info(global_variables.g_location)[1:], (row[4], row[5]))
        rounded_distance = round(distance * 1000) / 1000
        one_result = {
            'ident': row[0],
            'name': row[1],
            'continent': row[2],
            'country_name': row[3],
            'lat': row[4],
            'lon': row[5],
            'distance_km': rounded_distance
        }
        full_result.append(one_result)

    return full_result


# Picks an unseen event for the player and returns event text, effects (and choices where applicable)
def start_event():

    kmultiplier = global_variables.g_karma - 50
    if kmultiplier >= 0:
        kmultiplier = random.randint(0, 100 + kmultiplier)
    else:
        kmultiplier = random.randint(0 + kmultiplier, 100)

    if kmultiplier > 75:
        eventtype = "good"
    elif kmultiplier < 25:
        eventtype = "bad"
    else:
        eventtype = "neutral"

    event = random.choice(global_variables.events[eventtype])
    while event in usedevents:
        event = random.choice(global_variables.events[eventtype])

    global_variables.usedevents.append(event)

    choices = []
    if event[1][0] == "":
        choice = False
    else:
        choice = True

    if choice:

        for i in event[1]:
            choices.append(i)

    return event, choice


# Processes players choices if player had an event with choices, changes player's stats if there were changes
def event_choice(playerinput):

    event = global_variables.usedevents[-1]

    if playerinput == "1":
        eventeffect = event[1][0][1].split(" ")
    elif playerinput == "2":
        eventeffect = event[1][1][1].split(" ")
    elif playerinput == "3":
        eventeffect = event[1][2][1].split(" ")

    else:
        eventeffect = event[1][1].split(" ")

    if eventeffect[0] == "karma":
        global_variables.g_karma += int(eventeffect[1])
    if eventeffect[0] == "rounds":
        global_variables.g_rounds_left += int(eventeffect[1])
    if eventeffect[0] == "money":
        global_variables.g_money += int(eventeffect[1])
    if eventeffect[0] == "charge":
        global_variables.g_charge_left += int(eventeffect[1])
    return


# Updates the player's information in the database (saves the game)
def update_database(screen_name, money, charge_left, rounds_left, karma, location):

    sql = "update game "
    sql += "set money ='"+str(money)+"', "
    sql += "charge_left ='"+str(charge_left)+"', "
    sql += "rounds_left ='"+str(rounds_left)+"', "
    sql += "karma ='"+str(karma)+"', "
    sql += "location ='"+location+"' where screen_name = '"+screen_name+"'"

    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    return


# Adds a new player into the database (part of create_new_user() function)
def add_new_user(screen_name):

    sql = "insert into game(screen_name, location) "
    sql += "values('"+screen_name+"', 'efhk')"

    cursor = databaseconnect.cursor()
    cursor.execute(sql)

    return


# Checks if there already exists a player with a certain name in the database
def check_username_list():
    sql = "select screen_name from game"
    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0:
        if len(result) == 1:
            return result[0]
        return result
    return False


# Fetches player information from the database
def get_player_info(player):
    sql = "select money, charge_left, karma, rounds_left, location from game where screen_name ='" + player + "'"
    cursor = databaseconnect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0:
        return result[0]


# Function for when a new player is created, checks if playername already exists in the database, creates player,
# updates the player's start values, returns player's stats displayed in the game window
def create_new_user(username):
    username_list = check_username_list()

    if not username_list:
        add_new_user(username)
        update_database(username,
                        global_variables.g_money,
                        global_variables.g_charge_left,
                        global_variables.g_rounds_left,
                        global_variables.g_karma,
                        global_variables.g_location)
        global_variables.g_first_round = True
        global_variables.g_visited_airports.append(global_variables.g_location)
        return {
            'success': 'True',
            'money': global_variables.g_money,
            'charge_left': global_variables.g_charge_left,
            'rounds_left': global_variables.g_rounds_left,
            'location': get_location_info(global_variables.g_location),
            'first_round': global_variables.g_first_round
        }

    if isinstance(username_list, (tuple, list)):
        for i in username_list:
            if username == i[0]:
                return {
                    'success': 'False'
                }

    add_new_user(username)
    update_database(username,
                    global_variables.g_money,
                    global_variables.g_charge_left,
                    global_variables.g_rounds_left,
                    global_variables.g_karma,
                    global_variables.g_location)
    global_variables.g_first_round = True
    global_variables.g_visited_airports.append(global_variables.g_location)
    return {
        'success': 'True',
        'money': global_variables.g_money,
        'charge_left': global_variables.g_charge_left,
        'rounds_left': global_variables.g_rounds_left,
        'location': get_location_info(global_variables.g_location)
    }
