# AUTHOR:   SANDER BETZ
# ST-NR:    6070000
# ST-MAIL:  S.H.R.Betz@student.tudelft.nl

# Put imports here
import pygame as pg

# Main code
class Game:
    def __init__(self):
        self.RESOLUTION : tuple = (600, 500)
        self.screen     : any   = pg.display.set_mode(self.RESOLUTION)
        


class Airplane:
    def __init__(self, aircraft_type: str, location: tuple, velocity: tuple):
        self.aircraft_type : str = aircraft_type
        self.x             : int = location[0]
        self.y             : int = location[1]
        self.vx            : int = velocity[0]
        self.vy            : int = velocity[1]
        
class Missile():
    def __init__(self, location, velocity, target: Airplane):
        self.x             : int = location[0]
        self.y             : int = location[1]
        self.vx            : int = velocity[0]
        self.vy            : int = velocity[1]
        self.target = target

def main():

    # Initialize the game setup
    game = Game()
    
    red_plane = Airplane('Red', (0.1, 0.1), (0.1, 0))
    blue_plane = Airplane('Blue', (0.9, 0.9), (-0.1, 0))

    # Initialize the main game
    pg.init()

    # Main game loop



    # Stop the game based on parameters
    pg.quit()


if __name__ == '__main__':
    main()
