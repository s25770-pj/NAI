from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz


# inputs
temperature = ctrl.Antecedent(np.arange(0, 131, 1), 'temperature')
temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 30])
temperature['medium'] = fuzz.trimf(temperature.universe, [25, 50, 80])
temperature['high'] = fuzz.trimf(temperature.universe, [70, 100, 130])

distance = ctrl.Antecedent(np.arange(0, 100001, 1), 'distance')
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 5000])
distance['medium'] = fuzz.trimf(distance.universe, [2000, 5000, 20000])
distance['far'] = fuzz.trimf(distance.universe, [15000, 100000, 100000])

threat_level = ctrl.Antecedent(np.arange(0, 101, 1), 'threat_level')
threat_level['low'] = fuzz.trimf(threat_level.universe, [0, 0, 30])
threat_level['medium'] = fuzz.trimf(threat_level.universe, [20, 50, 80])
threat_level['high'] = fuzz.trimf(threat_level.universe, [70, 100, 100])

motion = ctrl.Antecedent(np.arange(0, 2, 1), 'motion')
motion['no'] = fuzz.trimf(motion.universe, [0, 0, 1])
motion['yes'] = fuzz.trimf(motion.universe, [0, 1, 1])

speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

altitude = ctrl.Antecedent(np.arange(0, 20001, 1), 'altitude')
altitude['low'] = fuzz.trimf(altitude.universe, [0, 0, 1000])
altitude['medium'] = fuzz.trimf(altitude.universe, [500, 1000, 5000])
altitude['high'] = fuzz.trimf(altitude.universe, [4000, 20000, 20000])

# output
do_shot = ctrl.Consequent(np.arange(0, 101, 1), 'fire_missile')
do_shot['no'] = fuzz.trimf(do_shot.universe, [0, 0, 50])
do_shot['yes'] = fuzz.trimf(do_shot.universe, [40, 100, 100])

# rules
do_shot_rules = [ctrl.Rule(motion['no'] & temperature['low'] & threat_level['low'], do_shot['no']),

                ctrl.Rule(motion['yes'] & speed['slow'] & altitude['low'] & distance['close'], do_shot['yes']),
                ctrl.Rule(motion['yes'] & speed['medium'] & temperature['medium'] & threat_level['medium'], do_shot['yes']),
                ctrl.Rule(motion['yes'] & speed['medium'] & altitude['high'] & distance['medium'], do_shot['no']),
                ctrl.Rule(motion['yes'] & speed['medium'] & altitude['high'] & distance['far'], do_shot['no']),

                ctrl.Rule(motion['yes'] & speed['fast'] & altitude['high'] & distance['far'], do_shot['no']),
                ctrl.Rule(motion['yes'] & speed['fast'] & altitude['medium'] & threat_level['high'], do_shot['yes']),

                ctrl.Rule(motion['yes'] & speed['medium'] & altitude['low'] & distance['medium'], do_shot['yes'])]

do_shot_ctrl = ctrl.ControlSystem(do_shot_rules)
do_shot_sim = ctrl.ControlSystemSimulation(do_shot_ctrl)

def test_do_shot(speed_input, temperature_input, motion_input, altitude_input, distance_input, threat_level_input):
    do_shot_sim.input['speed'] = speed_input
    do_shot_sim.input['temperature'] = temperature_input
    do_shot_sim.input['motion'] = motion_input
    do_shot_sim.input['altitude'] = altitude_input
    do_shot_sim.input['distance'] = distance_input
    do_shot_sim.input['threat_level'] = threat_level_input

    # Compute the output
    do_shot_sim.compute()

    # Return the decision
    return do_shot_sim.output['fire_missile']