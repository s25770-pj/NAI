from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz

# Antecedents
distance = ctrl.Antecedent(np.arange(0, 100001, 1), 'distance')
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 5000])
distance['medium'] = fuzz.trimf(distance.universe, [5000, 20000, 50000])
distance['far'] = fuzz.trimf(distance.universe, [20000, 100000, 100000])

speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

altitude = ctrl.Antecedent(np.arange(0, 20001, 1), 'altitude')
altitude['low'] = fuzz.trimf(altitude.universe, [0, 0, 1000])
altitude['medium'] = fuzz.trimf(altitude.universe, [1000, 2500, 5000])
altitude['high'] = fuzz.trimf(altitude.universe, [4001, 20000, 20000])

weapon = ctrl.Antecedent(np.array([0, 1]), 'weapon')  # 0: Unarmed, 1: Armed
weapon['unarmed'] = fuzz.trimf(weapon.universe, [0, 0, 0])
weapon['armed'] = fuzz.trimf(weapon.universe, [1, 1, 1])

motion = ctrl.Antecedent(np.array([0, 1]), 'motion')  # 0: Stationary, 1: Moving
motion['stationary'] = fuzz.trimf(motion.universe, [0, 0, 0])
motion['moving'] = fuzz.trimf(motion.universe, [1, 1, 1])

# output
threat = ctrl.Consequent(np.arange(0, 101, 1), 'threat_level')
threat['low'] = fuzz.trimf(threat.universe, [0, 0, 50])
threat['medium'] = fuzz.trimf(threat.universe, [25, 50, 75])
threat['high'] = fuzz.trimf(threat.universe, [50, 100, 100])

# Rules
threat_rules = [
    ctrl.Rule(distance['close'] & speed['fast'] & weapon['armed'], threat['high']),
    ctrl.Rule(distance['medium'] & speed['medium'] & weapon['armed'], threat['medium']),
    ctrl.Rule(distance['far'] & speed['slow'] & weapon['unarmed'], threat['low']),
    ctrl.Rule(motion['moving'] & altitude['high'], threat['high']),
]

# Control System
threat_ctrl = ctrl.ControlSystem(threat_rules)
threat_sim = ctrl.ControlSystemSimulation(threat_ctrl)

# Test Function
def calculate_threat_test(distance_input, speed_input, altitude_input, weapon_input, motion_input):
    threat_sim.input['distance'] = distance_input
    threat_sim.input['speed'] = speed_input
    threat_sim.input['altitude'] = altitude_input
    threat_sim.input['weapon'] = weapon_input
    threat_sim.input['motion'] = motion_input

    threat_sim.compute()

    return threat_sim.output['threat_level']