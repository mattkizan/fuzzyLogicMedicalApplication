import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def get_user_input(category,min_range, max_range): # function to process and return user input (interval) as a start point  and end point
    while True:
        user_input = input(f"enter interval within the range of: {min_range} - {max_range}. For patient {category}")


        if '-' in user_input and user_input.count('-') == 1:
            numbers = user_input.split('-')
        else:
            print("Invalid input. Please use the format '34-40'.")
            continue

        try:
            startpoint = float(numbers[0])
            endpoint = float(numbers[1])
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        temperature_startpoint = round(startpoint, 1)
        temperature_endpoint = round(endpoint, 1)


        if min_range <= startpoint <= max_range and min_range <= endpoint <= max_range:
            return temperature_startpoint, temperature_endpoint
        else:
            print(f"Numbers should be within the range {min_range} to {max_range}.")



def return_temperature_fuzzyset(startpoint,endpoint): # function to generate a fuzzy set, using temperature membership functions, for all of the values between the start point and endpoint of an interval

    x_temperature = np.arange(28.0, 40.0, 0.1)


    temperature_low = fuzz.trapmf(x_temperature, [28.0, 28.0, 32.0, 36.5])
    temperature_md = fuzz.trapmf(x_temperature, [35.0, 36.5, 37.5, 39.0])
    temperature_high = fuzz.trapmf(x_temperature, [37.5, 39.0, 40.0, 40.0])

    temperature_low_dic = {}
    for i in range(280, 401, 1):
        value = i / 10.0
        if 28.0 <= value <= 36.5:
            temp_level_lo = fuzz.interp_membership(x_temperature, temperature_low, value)
            temperature_low_dic[value] = temp_level_lo
        else:
            temperature_low_dic[value] = 0.0

    temperature_md_dic = {}
    for i in range(280, 401, 1):
        value = i / 10.0
        if 35.0 <= value <= 39.0:
            temp_level_md = fuzz.interp_membership(x_temperature, temperature_md, value)
            temperature_md_dic[value] = temp_level_md
        else:
            temperature_md_dic[value] = 0.0
    #membership value of all of the values within the interval of the membership function high temperature is taken
    temperature_hi_dic = {}
    for i in range(280, 401, 1):
        value = i / 10.0
        if 37.5 <= value <= 40.0:
            temp_level_hi = fuzz.interp_membership(x_temperature, temperature_high, value)
            temperature_hi_dic[value] = temp_level_hi
        else:
            temperature_hi_dic[value] = 0.0

    fuzzy_set_values = []
    x_values = []

    #loop iterates over values of three fuzzy sets , high , low and medium stored in the dictionary, to find the max value for values values within the interval
    for key1, value1, key2, value2, key3, value3 in zip(temperature_low_dic.keys(), temperature_low_dic.values(), temperature_md_dic.keys(),temperature_md_dic.values(),temperature_hi_dic.keys(),temperature_hi_dic.values()):

        # only memberships of values withing the given inteval ( within the start point and endpoint) are taken and sorted to a seprate list

        if startpoint <= key1 <= endpoint and startpoint <= key2 <= endpoint and startpoint <= key3 <= endpoint:
            fuzzy_set_values.append(max(value1, value2, value3))
            x_values.append(key1)

    return fuzzy_set_values,x_values

def return_head_sev_fuzzyset(startpoint,endpoint):# function to generate a fuzzy set, using headaceh severity membership functions, for all of the values between the start point and endpoint of an interval

    x_head_sev_range = np.arange(0, 11, 1)

    headache_sev_low = fuzz.trimf(x_head_sev_range, [0, 0, 5])
    headache_sev_md = fuzz.trimf(x_head_sev_range, [2, 5, 8])
    headache_sev_hi = fuzz.trimf(x_head_sev_range, [5, 10, 10])

    head_sev_low_dic = {}
    for i in range(0, 10, 1):
        if 0 <= i <= 5:
            head_level = fuzz.interp_membership(x_head_sev_range, headache_sev_low, i)
            head_sev_low_dic[i] = head_level
        else:
            head_sev_low_dic[i] = 0

    head_sev_md_dic = {}
    for i in range(0, 10, 1):
        if 2 <= i <= 8:
            head_level = fuzz.interp_membership(x_head_sev_range, headache_sev_md, i)
            head_sev_md_dic[i] = head_level
        else:
            head_sev_md_dic[i] = 0

    head_sev_hi_dic = {}
    for i in range(0, 10, 1):
        if 5 <= i <= 10:
            head_level = fuzz.interp_membership(x_head_sev_range, headache_sev_hi, i)
            head_sev_hi_dic[i] = head_level
        else:
            head_sev_hi_dic[i] = 0



    fuzzy_set_values = []
    x_values = []
    for key1, value1, key2, value2, key3, value3 in zip(head_sev_low_dic.keys(), head_sev_low_dic.values(), head_sev_md_dic.keys(),head_sev_md_dic.values(),head_sev_hi_dic.keys(),head_sev_hi_dic.values()):

        # Check if the key is in the range 35.2 to 35.8
        if startpoint <= key1 <= endpoint and startpoint <= key2 <= endpoint and startpoint <= key3 <= endpoint:
            fuzzy_set_values.append(max(value1, value2, value3))
            x_values.append(key1)

    return fuzzy_set_values,x_values



def return_age_fuzzyset(startpoint,endpoint):# function to generate a fuzzy set, using age membership functions, for all of the values between the start point and endpoint of an interval

    x_age_range = np.arange(0, 130, 1)

    age_low = fuzz.trapmf(x_age_range, [0, 0, 25, 40])
    age_md = fuzz.trapmf(x_age_range, [25, 40, 50, 65])
    age_hi = fuzz.trapmf(x_age_range, [50, 65, 130, 130])


    age_low_dic = {}
    for i in range(0, 130, 1):
        if 0 <= i <= 40:
            age_level = fuzz.interp_membership(x_age_range, age_low, i)
            age_low_dic[i] = age_level
        else:
            age_low_dic[i] = 0

    age_md_dic = {}
    for i in range(0, 130, 1):
        if 23 <= i <= 65:
            age_level = fuzz.interp_membership(x_age_range, age_md, i)
            age_md_dic[i] = age_level
        else:
            age_md_dic[i] = 0

    age_hi_dic = {}
    for i in range(0, 130, 1):
        if 50 <= i <= 130:
            age_level = fuzz.interp_membership(x_age_range, age_hi, i)
            age_hi_dic[i] = age_level
        else:
            age_hi_dic[i] = 0



    fuzzy_set_values = []
    x_values = []
    for key1, value1, key2, value2, key3, value3 in zip(age_low_dic.keys(), age_low_dic.values(), age_md_dic.keys(),age_md_dic.values(),age_hi_dic.keys(),age_hi_dic.values()):

        # Check if the key is in the range 35.2 to 35.8
        if startpoint <= key1 <= endpoint and startpoint <= key2 <= endpoint and startpoint <= key3 <= endpoint:
            fuzzy_set_values.append(max(value1, value2, value3))
            x_values.append(key1)

    return fuzzy_set_values,x_values




def plot_fuzzy_set(x_values,y_values,y_startpoint,y_endpoint,x_startpoint,x_endpoint,title): # plots fuzzy set of values within an interval
    # Add extra points for connecting to the x-axis
    x_values_extended = [x_values[0]] + x_values + [x_values[-1]]
    y_values_extended = [0.0] + y_values + [0.0]
    # Plotting
    plt.plot(x_values_extended, y_values_extended, marker='o', linestyle='-')
    plt.title(f'{title} fuzzyset')
    plt.xlabel('X Axis ')
    plt.ylabel('Y Axis (degree of membership)')

    plt.ylim(y_startpoint, y_endpoint)  # Set y-axis range
    plt.xlim(x_startpoint, x_endpoint)  # Set x-axis range

    plt.show()



def defuzzify(fuzzy_values, x_values): # defuzzifies a fuzzy set using centriod method

    summed_values = []
    for y , x in zip(fuzzy_values,x_values):
        summed_values.append(x * y)
    centriod = sum(summed_values)/ sum(fuzzy_values)
    return centriod





if __name__ == '__main__':


    # # retrieving temperature input
    temperature_startpoint,temperature_endpoint = get_user_input('Temperature',28.0,40.0)

    #retrieving fuzzy set for each value within an interval and the corresponding x value

    temperature_fuzzy_set, temp_x_values= return_temperature_fuzzyset(temperature_startpoint,temperature_endpoint)

    #plotting the fuzzy set of the values within an interval

    plot_fuzzy_set(temp_x_values, temperature_fuzzy_set, 0.0, 1.0, 28.0, 40.0,'temperature interval')

    #defuzzifying the value to recieve crisp ouput which is used as the input for the fuzzy inference system
    temperature_input = defuzzify(temperature_fuzzy_set,temp_x_values)


    #retrieving head severity input
    headache_sev_startpoint, headache_sev_endpoint = get_user_input('Headache severity', 0, 10)
    headache_sev_startpoint = round(headache_sev_startpoint)
    headache_sev_endpoint = round(headache_sev_endpoint)



    head_sev_fuzzy_set, head_sev_x_values = return_head_sev_fuzzyset(headache_sev_startpoint, headache_sev_endpoint)

    plot_fuzzy_set(head_sev_x_values, head_sev_fuzzy_set, 0.0, 1.0, 0, 10,'headache severity interval')
    head_severity_input = defuzzify(head_sev_fuzzy_set, head_sev_x_values)


    #retreiving age input

    age_startpoint, age_endpoint = get_user_input('Age', 0, 130)
    age_startpoint = round(age_startpoint)
    age_endpoint = round(age_endpoint)



    age_fuzzy_set, age_x_values = return_age_fuzzyset(age_startpoint, age_endpoint)

    plot_fuzzy_set(age_x_values, age_fuzzy_set, 0.0, 1.0, 0, 130, 'age interval')
    age_input = defuzzify(age_fuzzy_set, age_x_values)

    print(f"Temperature input calculated:   {temperature_input}")
    print(f" Headache severity input calculated:    {head_severity_input}")
    print(f" Age input calculated:  {age_input}")

    # fuzzy inference system
    temperature = ctrl.Antecedent(np.arange(28, 40, 0.1), 'temperature')
    headache_severity = ctrl.Antecedent(np.arange(0, 11, 0.1), 'headache_severity')
    age = ctrl.Antecedent(np.arange(0, 131, 0.1), 'age')
    urgency = ctrl.Consequent(np.arange(0, 101, 0.1), 'urgency')

    temperature['low'] = fuzz.trapmf(temperature.universe, [28, 28, 32, 36.5])
    temperature['medium'] = fuzz.trapmf(temperature.universe, [35, 36.5, 37.5, 39])
    temperature['high'] = fuzz.trapmf(temperature.universe, [37.5, 39, 40, 40])

    headache_severity['low'] = fuzz.trimf(headache_severity.universe, [0, 0, 5])
    headache_severity['moderate'] = fuzz.trimf(headache_severity.universe, [2, 5, 8])
    headache_severity['high'] = fuzz.trimf(headache_severity.universe, [5, 10, 10])

    age['young'] = fuzz.trapmf(age.universe, [0, 0, 25, 40])
    age['middle-aged'] = fuzz.trapmf(age.universe, [25, 40, 50, 65])
    age['old'] = fuzz.trapmf(age.universe, [50, 65, 130, 130])

    urgency['low'] = fuzz.trimf(urgency.universe, [0, 0, 50])
    urgency['moderate'] = fuzz.trimf(urgency.universe, [20, 50, 80])
    urgency['high'] = fuzz.trimf(urgency.universe, [50, 100, 100])

    temperature.view()
    headache_severity.view()
    age.view()
    urgency.view()

    # # fuzzy rules


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




    urgency_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,
                                       rule12,rule13,rule14, rule15,rule16,rule17,rule18,rule19,rule20,rule21,
                                       rule22,rule23,rule24,rule25,rule26,rule27])

    severity = ctrl.ControlSystemSimulation(urgency_ctrl)



    severity.input['temperature'] = temperature_input
    severity.input['age'] = age_input
    severity.input['headache_severity'] = head_severity_input

    severity.compute()

    print(f"urgency score: {severity.output['urgency']}")
    urgency.view(sim=severity)







