import json
import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl


# Antecedents
distance = ctrl.Antecedent(np.arange(0, 10001, 1), 'distance')
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 1500])
distance['medium'] = fuzz.trimf(distance.universe, [1400, 1800, 2200])
distance['far'] = fuzz.trimf(distance.universe, [2000, 3000, 3000])

speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

altitude = ctrl.Antecedent(np.arange(0, 20001, 1), 'altitude')
altitude['low'] = fuzz.trimf(altitude.universe, [0, 0, 1000])
altitude['medium'] = fuzz.trimf(altitude.universe, [500, 1000, 5000])
altitude['high'] = fuzz.trimf(altitude.universe, [4000, 20000, 20000])

# Consequent
missile_type = ctrl.Consequent(np.arange(0, 6, 1), 'fire_missile')
missile_type['short'] = fuzz.trimf(missile_type.universe, [0, 0, 1])
missile_type['medium'] = fuzz.trimf(missile_type.universe, [0, 1, 2])
missile_type['long'] = fuzz.trimf(missile_type.universe, [1, 2, 2])

# Rules
formatted_rules = []

# Get rules from json file
with open('./fuzzy_logic/rules/missile_choice.json', 'r') as file:
    rules = json.load(file)

    for rule in rules:
        conditions = rule['conditions']
        action = rule['action']

        formatted_rules.append(
            ctrl.Rule(distance[conditions['distance']] &
                      speed[conditions['speed']] &
                      altitude[conditions['altitude']], missile_type[action]))

def missile_choice(distance_input: float, speed_input: float, altitude_input: float) -> float:
    '''
    Function that calculates threat level
    :param distance_input: distance between launcher and the object
    :param speed_input: speed of the object
    :param altitude_input: altitude of the object
    :return: missile choice
    '''
    # Simulate threat level
    fire_missile_ctrl = ctrl.ControlSystem(formatted_rules)
    fire_missile_sim = ctrl.ControlSystemSimulation(fire_missile_ctrl)

    # Pin inputs to simulation
    fire_missile_sim.input['distance'] = distance_input
    fire_missile_sim.input['speed'] = speed_input
    fire_missile_sim.input['altitude'] = altitude_input

    # Process simulation data
    fire_missile_sim.compute()

    return fire_missile_sim.output['fire_missile']
