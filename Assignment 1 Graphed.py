# Put imports here
import math
import matplotlib.pyplot as plt

"This is done from home!"

# Main code
"Universal constants"
base_gravity        : float = 9.80665
gas_constant        : float = 287.0

"Sea level values"
base_temperature    : float = 288.15
base_pressure       : float = 101325

"Conversions"
ft_to_m = 0.3048
FL_to_m = 0.3048 * 1000

"""
Layers for geopotential altitude h

T1 = T0 + a(h1 - h0)

Troposphere     0    < h <= 11 km    a = -6.5 K/km = -0.0065 K/m
Tropopause      11 km < h <= 20 km   isotherm (a = 0)
Stratosphere    20 km < h <= 32 km   a = +1.0 K/km = +0.0010 K/m 
Stratosphere    32 km < h <= 47 km   a = +2.8 K/km = +0.0028 K/m
Stratopause     47 km < h <= 51 km   isotherm (a = 0)
Mesosphere      51 km < h <= 71 km   a = -2.8 K/km = -0.0028 K/m
Mesosphere      71 km < h <= 86 km   a = -2.0 K/km = -0.0020 K/m
"""


class Layer:
    def __init__(self, min_height: int, max_height: int, coefficient: float, layer_name: str, layer_type: str):
        self.min_height     : int = min_height
        self.max_height     : int = max_height
        self.coefficient    : float = coefficient
        self.layer_name     : str = layer_name
        self.layer_type     : str = layer_type


layers = [
    Layer(0, 11000, -0.0065, 'Troposphere', 'non-isothermal'),
    Layer(11001, 20000, 0, 'Troposphere', 'isothermal'),
    Layer(20001, 32000, 0.0010, 'Stratosphere', 'non-isothermal'),
    Layer(32001, 47000, 0.0028, 'Stratosphere', 'non-isothermal'),
    Layer(47001, 51000, 0, 'Stratopause', 'isothermal'),
    Layer(51001, 71000, -0.0028, 'Mesosphere', 'non-isothermal'),
    Layer(71001, 86000, -0.0020, 'Mesosphere', 'non-isothermal'),
]


def initialize_program() -> float:
    print("***** ISA calculator *****")
    print('1. Calculate ISA for altitude in meters')
    print('2. Calculate ISA for altitude in feet')
    print('3. Calculate ISA for altitude in FL')

    type_list = {
        1: 'm',
        2: 'ft',
        3: 'FL'
    }

    def height_type() -> int:
        type_height = int(input('Enter your choise (number from list): '))
        if type_height > 3:
            print('Please input a valid selection')
            type_height = height_type()
        return type_height

    def inp_height(check_type: int) -> float:
        inp = int(input(f'Enter altitude [{type_list[check_type]}]: '))
        if inp > 86000:
            print("You're in space now! Congrats! However please input a valid altitude in the atmosphere")
            inp = initialize_program()
        return inp

    check_type = height_type()
    inp = inp_height(check_type)

    if check_type == 2:
        inp *= ft_to_m
    elif check_type == 3:
        inp *= FL_to_m

    return inp


def calc_height_temperature(height: int, t0: float, layer: Layer) -> float:
    return t0 + (min(height, layer.max_height) - layer.min_height) * layer.coefficient


def calc_height_pressure(altitude : int, p0 : float, t0 : float, t1: float, layer: Layer) -> float:

    if layer.layer_type == 'non-isothermal':
        return p0 * (t1 / t0) ** (-base_gravity / (layer.coefficient * gas_constant))
    elif layer.layer_type == 'isothermal':
        return p0 * math.e ** (-(base_gravity / (gas_constant * t0)) * (min(altitude, layer.max_height) - layer.min_height))


def calc_density(pressure : float, temperature : float) -> float:
    return pressure / (gas_constant * temperature)


def calc_layer_properties(altitude: int, t0: float, p0: float, layer: Layer):
    temperature = calc_height_temperature(altitude, t0, layer)
    pressure = calc_height_pressure(altitude, p0, t0, temperature, layer)
    density = calc_density(pressure, temperature)

    return temperature, pressure, density


def main():
    "altitude = initialize_program()"


    height_list = []
    pressure_list = []
    temperature_list = []
    density_list = []
    h = 0

    while h <= 86000:

        layer_props = (base_temperature, base_pressure, None)
        for num, layer in enumerate(layers, start=1):

            layer_props = calc_layer_properties(min(layer.max_height, h), layer_props[0], layer_props[1], layer)
            """
            print(f'Computation: {num}, {layer.layer_name} layer\n'
                  f'    Height : {min(altitude, layer.max_height)} m\n'
                  f'    Temperature: {round(layer_props[0], 2)} K\n'
                  f'    Pressure: {round(layer_props[1], 0)} Pa\n'
                  f'    Density : {round(layer_props[2], 4)} kg/m3')"""

            if h <= layer.max_height:
                break

        height_list.append(h)
        temperature_list.append(layer_props[0])
        pressure_list.append(layer_props[1])
        density_list.append(layer_props[2])

        h += 100

    fig, ax = plt.subplots()
    ax.set_ylabel('Height [m]')
    ax.set_xlabel('Temperature [K]')
    ax.set_xlim(0, max(temperature_list))
    ax.scatter(temperature_list, height_list, marker='.', color='r')

    ax1 = ax.twiny()
    ax1.set_xlabel('Pressure [Pa]')
    ax1.set_xlim(min(pressure_list), max(pressure_list))
    ax1.scatter(pressure_list, height_list, marker='o', color='y')

    ax2 = ax.twiny()
    ax2.set_xlabel('Density [kg/m3]')
    ax2.set_xlim(min(density_list), max(density_list))
    ax2.scatter(density_list, height_list, color='b')

    ax1.spines.top.set_position(("axes", 1.2))
    ax2.spines.top.set_position(("axes", 2.4))

    plt.show()


if __name__ == '__main__':
    main()
