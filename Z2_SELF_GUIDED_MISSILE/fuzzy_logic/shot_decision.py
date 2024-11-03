import json
import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl


with open('./config.json', 'r') as file:
    config = json.load(file)

# Antecedents
# TODO: przenieść do sterowania pociskiem
# temperature = ctrl.Antecedent(np.arange(0, 131, 1), 'temperature')
# temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 30])
# temperature['medium'] = fuzz.trimf(temperature.universe, [25, 50, 80])
# temperature['high'] = fuzz.trimf(temperature.universe, [70, 100, 130])/

threat_level = ctrl.Antecedent(np.arange(0, 101, 1), 'threat_level')
threat_level['low'] = fuzz.trimf(threat_level.universe, [0, 0, 30])
threat_level['medium'] = fuzz.trimf(threat_level.universe, [20, 50, 80])
threat_level['high'] = fuzz.trimf(threat_level.universe, [70, 100, 100])

speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

altitude = ctrl.Antecedent(np.arange(0, 20001, 1), 'altitude')
altitude['low'] = fuzz.trimf(altitude.universe, [0, 0, 1000])
altitude['medium'] = fuzz.trimf(altitude.universe, [500, 1000, 5000])
altitude['high'] = fuzz.trimf(altitude.universe, [4000, 20000, 20000])

# Consequent
do_shot = ctrl.Consequent(np.arange(0, 101, 1), 'fire_missile')
do_shot['no'] = fuzz.trimf(do_shot.universe, [0, 0, 0.5])
do_shot['yes'] = fuzz.trimf(do_shot.universe, [0.5, 1, 1])

# Rules
formatted_rules = []

# Get rules from json file
# TODO: Można dorobić funkcję statyczną do tego
with open(config['RULES']['SHOT_DECISION']['URL'], 'r') as file:
    rules = json.load(file)

    for rule in rules:
        conditions = rule['conditions']
        action = rule['action']

        formatted_rules.append(
            ctrl.Rule(threat_level[conditions['threat_level']] &
                      speed[conditions['speed']] &
                      altitude[conditions['altitude']], do_shot[action]))

def calculate_shot_rightness(threat_level_input: float, speed_input: float, altitude_input: float) -> float:
    '''
    Function that calculates rightness of launching the missile at the moment
    :param threat_level_input: threat level that object exerts
    :param speed_input: object speed
    :param altitude_input: object altitude
    :return: does launcher should launch the missile
    '''
    # Simulate threat level
    do_shot_ctrl = ctrl.ControlSystem(formatted_rules)
    do_shot_sim = ctrl.ControlSystemSimulation(do_shot_ctrl)

    # Pin inputs to simulation
    do_shot_sim.input['threat_level'] = threat_level_input
    do_shot_sim.input['speed'] = speed_input
    do_shot_sim.input['altitude'] = altitude_input

    # Process simulation data
    do_shot_sim.compute()

    return do_shot_sim.output['fire_missile']
