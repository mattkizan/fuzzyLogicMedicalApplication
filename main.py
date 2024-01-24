# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl





if __name__ == '__main__':
    # declaring antecedents and consequents , along with their domain
    temperature = ctrl.Antecedent(np.arange(28.00, 40.1, 0.1), 'Temperature')
    headache_severity = ctrl.Antecedent(np.arange(0, 11, 1), 'Headache Severity')
    age = ctrl.Antecedent(np.arange(0, 131, 1), 'Age')
    urgency = ctrl.Consequent(np.arange(0, 101, 1), 'Urgency')

    #membership function for each term in a input varibale is built with corresponding parameters
    temperature['low'] = fuzz.trapmf(temperature.universe,[28.00,28.00,32.00,36.5])
    temperature['medium'] = fuzz.trapmf(temperature.universe,[35.00,36.5,37.5,39.00])
    temperature['high'] = fuzz.trapmf(temperature.universe,[37.5,39.00,40.00,40.00])

    headache_severity['low'] = fuzz.trimf(headache_severity.universe,[0,0,5])
    headache_severity['moderate'] = fuzz.trimf(headache_severity.universe, [2,5,8 ])
    headache_severity['high'] = fuzz.trimf(headache_severity.universe, [5, 10, 10])

    age['young'] = fuzz.trapmf(age.universe, [0,0 ,25,40])
    age['middle-aged'] = fuzz.trapmf(age.universe, [25, 40, 50, 65])
    age['old'] = fuzz.trapmf(age.universe, [50, 65, 130, 130])

    urgency['low'] = fuzz.trimf(urgency.universe, [0, 0, 50])
    urgency['moderate'] = fuzz.trimf(urgency.universe, [20, 50, 80])
    urgency['high'] = fuzz.trimf(urgency.universe, [50, 100, 100])

    #membership functions of each input varaible is displayed
    temperature.view()
    headache_severity.view()
    age.view()
    urgency.view()

    # # fuzzy rules and declared
    rule1 = ctrl.Rule(temperature['high'] & headache_severity['high'] & age['old'], urgency['high'])
    rule2 = ctrl.Rule(temperature['low'] & headache_severity['high'] & age['old'], urgency['high'])
    rule3 = ctrl.Rule(temperature['medium'] & headache_severity['high'] & age['old'], urgency['high'])
    rule4 = ctrl.Rule(temperature['low'] & headache_severity['moderate'] & age['old'], urgency['high'])
    rule5 = ctrl.Rule(temperature['high'] & headache_severity['moderate'] & age['old'], urgency['high'])
    rule6 = ctrl.Rule(temperature['low'] & headache_severity['low'] & age['old'], urgency['high'])
    rule7 = ctrl.Rule(temperature['high'] & headache_severity['low'] & age['old'], urgency['moderate'])
    rule8 = ctrl.Rule(temperature['medium'] & headache_severity['low'] & age['old'], urgency['low'])
    rule9 = ctrl.Rule(temperature['medium'] & headache_severity['moderate'] & age['old'], urgency['moderate'])

    rule10 = ctrl.Rule(temperature['high'] & headache_severity['high'] & age['middle-aged'], urgency['high'])
    rule11 = ctrl.Rule(temperature['low'] & headache_severity['high'] & age['middle-aged'], urgency['high'])
    rule12 = ctrl.Rule(temperature['medium'] & headache_severity['high'] & age['middle-aged'], urgency['moderate'])
    rule13 = ctrl.Rule(temperature['low'] & headache_severity['moderate'] & age['middle-aged'], urgency['moderate'])
    rule14 = ctrl.Rule(temperature['high'] & headache_severity['moderate'] & age['middle-aged'], urgency['moderate'])
    rule15 = ctrl.Rule(temperature['low'] & headache_severity['low'] & age['middle-aged'], urgency['moderate'])
    rule16 = ctrl.Rule(temperature['high'] & headache_severity['low'] & age['middle-aged'], urgency['moderate'])
    rule17 = ctrl.Rule(temperature['medium'] & headache_severity['low'] & age['middle-aged'], urgency['low'])
    rule18 = ctrl.Rule(temperature['medium'] & headache_severity['moderate'] & age['middle-aged'], urgency['low'])

    rule19 = ctrl.Rule(temperature['high'] & headache_severity['high'] & age['young'], urgency['high'])
    rule20 = ctrl.Rule(temperature['low'] & headache_severity['high'] & age['young'], urgency['high'])
    rule21 = ctrl.Rule(temperature['medium'] & headache_severity['high'] & age['young'], urgency['moderate'])
    rule22 = ctrl.Rule(temperature['low'] & headache_severity['moderate'] & age['young'], urgency['moderate'])
    rule23 = ctrl.Rule(temperature['high'] & headache_severity['moderate'] & age['young'], urgency['moderate'])
    rule24 = ctrl.Rule(temperature['low'] & headache_severity['low'] & age['young'], urgency['moderate'])
    rule25 = ctrl.Rule(temperature['high'] & headache_severity['low'] & age['young'], urgency['moderate'])
    rule26 = ctrl.Rule(temperature['medium'] & headache_severity['low'] & age['young'], urgency['low'])
    rule27 = ctrl.Rule(temperature['medium'] & headache_severity['moderate'] & age['young'], urgency['low'])

    #sk fuzzy control systems are defined here
    urgency_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,
                                       rule12,rule13,rule14, rule15,rule16,rule17,rule18,rule19,rule20,rule21,
                                       rule22,rule23,rule24,rule25,rule26,rule27])

    severity = ctrl.ControlSystemSimulation(urgency_ctrl)

    #input is taken from the user interface
    while True:
        try:
            temperature = float(input("Please enter a number between 28.00 and 40.00 for temperature of the patient: "))
            temperature = round(temperature,2)
            if 28.00 <= temperature <= 40.00:
                break
            else:
                print("Please enter a number within the specified range.")
        except ValueError:
            print("Invalid input. Please try again.")

    while True:
        try:
            age = int(input("Please enter a number between 0 and 130 for  the age of the patient: "))

            if 0 <= age <= 130:
                break
            else:
                print("Please enter a number within the specified range.")
        except ValueError:
            print("Invalid input. Please try again.")

    while True:
        try:
            headache_score = int(input("Please enter a number between 0 and 10 : "))

            if 0 <= headache_score <= 10:
                break
            else:
                print("Please enter a number within the specified range.")
        except ValueError:
            print("Invalid input. Please try again.")

    #inpu is passed to the control system via the antecdent labels
    severity.input['Temperature'] = temperature
    severity.input['Age'] = age
    severity.input['Headache Severity'] = headache_score

    # sk fuzzy performs fuzzification , inference  and defuzzification ( centroid is the deafult method used in sk fuzz
    #for defuzzification.
    severity.compute()
    # crisp output value is printed aswell as teh output membership function.
    result = round(severity.output['Urgency'],2)
    print(f"urgency score: {result}")
    urgency.view(sim=severity)






