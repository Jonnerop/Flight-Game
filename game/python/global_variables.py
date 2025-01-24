import events

# Start values:
g_karma = 50
g_rounds_left = 5
g_charge_left = 100
g_full_charge = 100
g_cost_of_charging = 20000
g_money = 0
g_profit = 0
g_location = "efhk"
g_next_location = "ldri"
g_distance = 0
events = events.add_events()
usedevents = []
g_first_round = True
g_player_alive = True
g_visited_airports = []
g_name = ' '
g_maxrange = 4000


# Freights in lists
g_freight_name = ["Aid and Relief Supplies", "Wildlife and Conservation Supplies", "Medical Supplies",
                  "Food and Perishables", "Electronics", "Historical Artifacts", "Valuables",
                  "Non-Renewable Fuel and Resources", "Dangerous goods (you're not certified)", "Illegal Cargo"]
g_freight_price = [100, 105, 120, 150, 170, 180, 185, 200, 210, 250]
g_freight_karma = [7, 5, 5, 0, 0, 0, 0, -6, -8, -10]
g_difficulty = 10
