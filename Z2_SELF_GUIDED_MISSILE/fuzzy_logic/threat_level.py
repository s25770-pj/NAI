import json
import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl
from Z2_SELF_GUIDED_MISSILE.config import Settings


# Antecedents
motion = ctrl.Antecedent(np.array([0, 1]), 'motion')  # 0: Stationary, 1: Moving
motion['stationary'] = fuzz.trimf(motion.universe, [0, 0, 0])
motion['moving'] = fuzz.trimf(motion.universe, [1, 1, 1])

weapon = ctrl.Antecedent(np.array([0, 1]), 'weapon')  # 0: Unarmed, 1: Armed
weapon['unarmed'] = fuzz.trimf(weapon.universe, [0, 0, 0])
weapon['armed'] = fuzz.trimf(weapon.universe, [1, 1, 1])

distance = ctrl.Antecedent(np.arange(0, 100001, 1), 'distance')
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 5000])
distance['medium'] = fuzz.trimf(distance.universe, [5000, 20000, 50000])
distance['far'] = fuzz.trimf(distance.universe, [20000, 100000, 100000])

# Consequent
threat_level = ctrl.Consequent(np.arange(0, 101, 1), 'threat_level')
threat_level['low'] = fuzz.trimf(threat_level.universe, [0, 0, 50])
threat_level['medium'] = fuzz.trimf(threat_level.universe, [25, 50, 75])
threat_level['high'] = fuzz.trimf(threat_level.universe, [50, 100, 100])

# Rules
formatted_rules = []

# Get rules from json file
with open(Settings().fuzzy_settings.fuzzy_rules.threat['url'], 'r') as file:
    rules = json.load(file)

    for rule in rules:
        conditions = rule['conditions']
        action = rule['action']

        formatted_rules.append(
            ctrl.Rule(motion[conditions['motion']] &
                      weapon[conditions['weapon']] &
                      distance[conditions['distance']], threat_level[action]))


def calculate_threat_level(motion: float, weapon: float, distance: float) -> float:
    '''
    Function that calculates threat level
    :param motion: does object move
    :param weapon: does object has weapon
    :param distance: distance between launcher and the object
    :return: threat level
    '''
    # Simulate threat level
    threat_level_ctrl = ctrl.ControlSystem(formatted_rules)
    threat_level_sim = ctrl.ControlSystemSimulation(threat_level_ctrl)

    # Pin inputs to simulation
    threat_level_sim.input['motion'] = motion
    threat_level_sim.input['weapon'] = weapon
    threat_level_sim.input['distance'] = distance

    # Process simulation data
    threat_level_sim.compute()

    return threat_level_sim.output['threat_level']


