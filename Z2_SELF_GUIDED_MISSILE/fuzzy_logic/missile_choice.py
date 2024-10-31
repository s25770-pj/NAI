from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz


# inputs
distance = ctrl.Antecedent(np.arange(0, 10001, 1), 'distance')
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 1500])
distance['medium'] = fuzz.trimf(distance.universe, [1400, 1800, 2200])
distance['far'] = fuzz.trimf(distance.universe, [2000, 3000, 3000])
distance['out_of_range'] = fuzz.trimf(distance.universe, [2900, 7000, 10000])

speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

# outputs
missile_type = ctrl.Consequent(np.arange(0, 6, 1), 'fire_missile')
missile_type['no'] = fuzz.trimf(missile_type.universe, [0, 0, 1])
missile_type['short'] = fuzz.trimf(missile_type.universe, [1, 1, 2])
missile_type['medium'] = fuzz.trimf(missile_type.universe, [1, 2, 3])
missile_type['long'] = fuzz.trimf(missile_type.universe, [2, 3, 4])

# rules
missile_choice_rules = [ctrl.Rule(distance['close'] & speed['slow'], missile_type['short']),
                        ctrl.Rule(distance['close'] & speed['medium'], missile_type['short']),
                        ctrl.Rule(distance['close'] & speed['fast'], missile_type['short']),
                        ctrl.Rule(distance['medium'] & speed['slow'], missile_type['medium']),
                        ctrl.Rule(distance['medium'] & speed['medium'], missile_type['medium']),
                        ctrl.Rule(distance['medium'] & speed['fast'], missile_type['medium']),
                        ctrl.Rule(distance['far'] & speed['slow'], missile_type['long']),
                        ctrl.Rule(distance['far'] & speed['medium'], missile_type['long']),
                        ctrl.Rule(distance['far'] & speed['fast'], missile_type['long'])]

# Control system
fire_missile_ctrl = ctrl.ControlSystem(missile_choice_rules)
# print(f'fire_missile_ctrl: {fire_missile_ctrl}')
fire_missile_sim = ctrl.ControlSystemSimulation(fire_missile_ctrl)
# print(f'fire_missile_sim: {fire_missile_sim}')


def test_missile_choice(distance_input, speed_input, temperature_input=None, motion_input=None):
    # Wprowadzenie danych do logiki rozmytej
    fire_missile_sim.input['distance'] = distance_input
    fire_missile_sim.input['speed'] = speed_input
    # Print input values
    # print(f"Inputs - Temperature: {temperature_input}, Motion: {motion_input}, Distance: {distance_input}")
    # print(f"Distance - Speed: {speed['slow'].mf[speed_input]}, Medium: {speed['medium'].mf[speed_input]}, Far: {speed['fast'].mf[speed_input]}")
    # Check membership values
    # print(f"Distance - Close: {distance['close'].mf[distance_input]}, Medium: {distance['medium'].mf[distance_input]}, Far: {distance['far'].mf[distance_input]}")

    # Compute output
    fire_missile_sim.compute()

    # Print the output
    print(fire_missile_sim.output['fire_missile'])  # Check if there's any output
    missile_type = fire_missile_sim.output['fire_missile']
    # print(f'missile_type: {missile_type}')
    # print(f'missile_type round: {round(missile_type)}')

    # Sprawdzanie, czy należy strzelać
    # if missile_type > 0 and len(launcher.loaded_missiles) > 0:
    if missile_type > 0:
        if missile_type <= 1:
            print("Strzel krótki pocisk!")
            # launcher.loaded_missiles[0].launch()
        elif missile_type <= 2:
            print("Strzel średni pocisk!")
            # launcher.loaded_missiles[0].launch()
        elif missile_type <= 3:
            print("Strzel długi pocisk!")
            # launcher.loaded_missiles[0].launch()