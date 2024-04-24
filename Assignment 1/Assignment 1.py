# Imports
import math


# Universal constants
base_gravity        : float = 9.80665
gas_constant        : float = 287.0

# Sea level values
base_temperature    : float = 288.15
base_pressure       : float = 101325

# Conversions
ft_to_m = 0.3048
FL_to_m = 0.3048 * 1000


# Layers for Geopotential altitude h

# T1 = T0 + a(h1 - h0)

# Troposphere     0    < h <= 11 km    a = -6.5 K/km = -0.0065 K/m
# Tropopause      11 km < h <= 20 km   isotherm (a = 0)
# Stratosphere    20 km < h <= 32 km   a = +1.0 K/km = +0.0010 K/m
# Stratosphere    32 km < h <= 47 km   a = +2.8 K/km = +0.0028 K/m
# Stratopause     47 km < h <= 51 km   isotherm (a = 0)
# Mesosphere      51 km < h <= 71 km   a = -2.8 K/km = -0.0028 K/m
# Mesosphere      71 km < h <= 86 km   a = -2.0 K/km = -0.0020 K/m

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
    # This function is used to initialize the program, see it as a "MAIN MENU" of the program
    # First a change in base temperature is requested, then a menu for which type of height [m, ft, FL] you want.
    # Then the requested height is input into the calculation
    # All calculations are performed in Metric ISA, so requests in ft and FL are first converted to meters, then the calculation is performed

    print("***** ISA calculator *****")

    type_list = {1: 'm', 2: 'ft', 3: 'FL'}

    def define_standard_SLTemp() -> None:
        global base_temperature     # Modify the base temperature though global (soft const) variable change
        ent = input('Would you like to change the starting sea level temperature? \n'
                    'If no change is requested, press ENTER, otherwise enter temperature: ')
        if ent == '':
            print(f'--> No change requested, standard ISA (T: {base_temperature} K) used')
            return
        else:
            print(f'--> Change in base ISA requested from T[0 m]: {base_temperature} K to T[0 m]: {float(ent)} K')
            base_temperature = float(ent)

    def height_type() -> int:
        print('1. Calculate ISA for altitude in meters \n'
              '2. Calculate ISA for altitude in feet \n'
              '3. Calculate ISA for altitude in FL')
        type_height = int(input('Enter your choise (number from list): '))
        if abs(type_height) > 3:
            print('--> Please input a valid selection')

            # If a non-valid option is chosen, rerun (recursion safety) the function with a returned value
            # This ensures that a valid option is finally passed through the program
            type_height = height_type()
        return type_height

    def inp_height(check_type: int) -> float:
        inp = float(input(f'Enter altitude [{type_list[check_type]}]: '))
        if inp > 86000 or inp < 0:
            if inp < 0:
                print("--> You're under water... Please choose a value above water")
            else:
                print("--> You're in space now! Congrats! However please input a valid altitude in the atmosphere")

            # If a non-valid option is chosen, rerun (recursion safety) the function with a returned value
            # This ensures that a valid option is finally passed through the program
            inp = inp_height(check_type)
        return inp

    # Actual menu loop
    define_standard_SLTemp()
    check_type = height_type()
    inp = inp_height(check_type)

    # Conversion from ft, FL to meters
    if check_type == 2:
        inp *= ft_to_m
    elif check_type == 3:
        inp *= FL_to_m

    return inp


def calc_height_temperature(height: float, t0: float, layer: Layer) -> float:
    """Standard calculation of temperature based on input temperature"""
    return t0 + (min(height, layer.max_height) - layer.min_height) * layer.coefficient

def calc_height_pressure(altitude : float, p0 : float, t0 : float, t1: float, layer: Layer) -> float:
    # Calculation of pressure based on earlier calculation of temperature
    # The calculation is split in a non-isothermal and an isothermal calculation based on the layer.type, defined in original parameters from assignment
    if layer.layer_type == 'non-isothermal':
        return p0 * (t1 / t0) ** (-base_gravity / (layer.coefficient * gas_constant))
    elif layer.layer_type == 'isothermal':
        return p0 * math.e ** (-(base_gravity / (gas_constant * t0)) * (min(altitude, layer.max_height) - layer.min_height))


def calc_density(pressure : float, temperature : float) -> float:
    """Calculation of density based on earlier calculation of temperature and pressure"""
    return pressure / (gas_constant * temperature)

def calc_layer_properties(altitude: float, t0: float, p0: float, layer: Layer) -> tuple[float, float, float]:
    # This calculation performs the calculations of the actual layer, so that the main loop remains clean
    temperature = calc_height_temperature(altitude, t0, layer)
    pressure = calc_height_pressure(altitude, p0, t0, temperature, layer)
    density = calc_density(pressure, temperature)

    return temperature, pressure, density

def main():
    # initialize program and get the wanted altitude for the calculation
    altitude = initialize_program()

    # initialize the layer properties for first calculation. This could be seen as a layer from 0m to 0m
    # This initial property is used in the first for loop calculation in the function input
    layer_props = (base_temperature, base_pressure, None)

    for num, layer in enumerate(layers, start=1):
        # The for loop will run for as long as the calculated height is below the maximum height of the layer the calculation is performed in
        # When the maximum height layer exceeds the requested height, the for loop is terminated

        # Calculate the layer properties of the current layer, then insert these into the next for loop calculation through function parameters
        # This could also probably be done without a for loop, instead though recursion, however for clarity sake this is done here
        # Within recursion the passed calculations are passed lines down, here it's loop starts -> function called (right) -> into variable (left) -> end loop
        layer_props = calc_layer_properties(min(layer.max_height, altitude), layer_props[0], layer_props[1], layer)
        """print(f'Computation: {num}, {layer.layer_name} layer\n'
              f'    Height : {min(altitude, layer.max_height)} m\n'
              f'    Temperature: {round(layer_props[0], 2)} K\n'
              f'    Pressure: {round(layer_props[1], 0)} Pa\n'
              f'    Density : {round(layer_props[2], 4)} kg/m3')"""

        if altitude <= layer.max_height:
            # Terminate the for loop when the maximum layer height exceeds the input altitude
            print(f'Computation up to: {layer.layer_name} layer\n'
                  f'    Height :        {min(altitude, layer.max_height)} m\n'
                  f'    Temperature:    {round(layer_props[0], 2)} K\n'
                  f'    Pressure:       {round(layer_props[1], 0)} Pa\n'
                  f'    Density :       {round(layer_props[2], 4)} kg/m3')

            break


if __name__ == '__main__':
    main()
