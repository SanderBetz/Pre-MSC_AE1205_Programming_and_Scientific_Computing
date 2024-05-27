# AUTHOR:   SANDER BETZ
# ST-NR:    6070000
# ST-MAIL:  S.H.R.Betz@student.tudelft.nl

# Put imports here
import pygame as pg
import math
import time

import pygame.key


# Main gameplay rules:
#   ---->   Red init Pos    : 100 px left of Center
#   ---->   Red init Dir    : 180 deg (Pointing Left)
#   ---->   Red init Vel    : 200 px / s
#   ---->   Blue init Pos   : 100 px right of Center
#   ---->   Blue init Dir   : 90 deg (Pointing Right)
#   ---->   Blue init Vel   : 200 px / s
#   ---->   Edges don't exist, when an edge is found, its teleported to the other side of screen

# Main code

RESOLUTION = (1000, 800)
screen = pg.display.set_mode(RESOLUTION)
scrrect = screen.get_rect()

aircraft_speed = 200
aircraft_rotation = math.pi
missile_speed = 1000
spawn_protection = 0.


class Airplane:
    def __init__(self, aircraft_type: str, location: tuple, direction: float, velocity: int, controller: str, owner = None):
        self.aircraft_type : str    = aircraft_type
        self.x             : int    = location[0]
        self.y             : int    = location[1]
        self.theta         : float  = direction
        self.velocity      : int    = velocity
        self.vx            : float  = velocity * math.cos(self.theta)
        self.vy            : float  = velocity * math.sin(self.theta)
        self.controller    : str    = controller
        self.alive_time    : float  = 0.
        self.owner         : any    = owner

        if self.aircraft_type == 'Red':
            img = pg.image.load('Visual_Files/redship.png')
        elif self.aircraft_type == 'Blue':
            img = pg.image.load('Visual_Files/blueship.png')
        elif self.aircraft_type == 'Missile':
            img = pg.image.load('Visual_Files/missile.png')

        img = pg.transform.scale(img, (img.get_width() * 0.12, img.get_height() * 0.12))
        self.img_list = {angle : pg.transform.rotate(img, angle) for angle in range(361)}
        img = self.img_list[int(math.degrees(self.theta))]

        self.plane = img
        self.plane_rect = img.get_rect()

        self.x_to_draw = self.x * RESOLUTION[0]
        self.y_to_draw = RESOLUTION[1] - self.y * RESOLUTION[1]

    def update(self, dt):
        self.x_to_draw = self.x * RESOLUTION[0]
        self.y_to_draw = RESOLUTION[1] - self.y * RESOLUTION[1]
        self.alive_time += dt

    def rotate(self):
        if math.degrees(self.theta) >= 359:
            self.theta = math.degrees(0)
        elif math.degrees(self.theta) <= 1:
            self.theta = math.radians(360)

        self.plane = self.img_list[int(math.degrees(self.theta))]
        self.plane_rect = self.plane.get_rect()

class Explosion:
    def __init__(self):
        self.explode_audio = pg.mixer.Sound('Audio_Files/explosion.wav')

    def explode(self):
        self.explode_audio.play()

def main():

    # Put planes 100 px of center
    red_start_pos   = (((RESOLUTION[0] / 2) - 100) / RESOLUTION[0],
                     int(RESOLUTION[1] / 2) / RESOLUTION[1])

    blue_start_pos  = (((RESOLUTION[0] / 2) + 100) / RESOLUTION[0],
                     int(RESOLUTION[1] / 2) / RESOLUTION[1])

    objects_in_air = []
    
    red_plane = Airplane('Red', red_start_pos, math.pi,  aircraft_speed, 'Player_A')
    blue_plane = Airplane('Blue', blue_start_pos, 0., aircraft_speed, 'Player_B')

    objects_in_air.append(red_plane)
    objects_in_air.append(blue_plane)

    # Initialize the main game
    pg.init()

    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    dt = 0.01
    tsim = 0.0
    tstart = 0.001 * pg.time.get_ticks()
    explosion = False

    running = False
    # Main game loop
    while not running:
        # Draw black background, so all objects are hidden
        pg.draw.rect(screen, black, scrrect)
        trun = 0.001 * pg.time.get_ticks() - tstart

        if trun + dt >= tsim:

            # Movement handler
            for aircraft in objects_in_air:
                def calculate_turn(self: Airplane, other: Airplane):
                    print(self.theta, math.atan2((self.x - other.x) , (self.y - other.y)))
                    return math.pi * dt

                keys = pygame.key.get_pressed()
                if aircraft.controller == 'Player_A':
                    if keys[pygame.K_a]:
                        aircraft.theta += math.pi * dt
                    elif keys[pygame.K_d]:
                        aircraft.theta -= math.pi * dt
                    if keys[pygame.K_s]:
                        # Check if there is already a missile from Player A, if so -> Don't spawn
                        if sum(checker.owner == aircraft for checker in objects_in_air) <= 0 and tsim > spawn_protection:
                            objects_in_air.append(Airplane('Missile', (aircraft.x, aircraft.y), aircraft.theta,  missile_speed, 'Missile', aircraft))
                        elif tsim < spawn_protection:
                            print('Spawn protection!')
                    if keys[pygame.K_SPACE]:
                        time.sleep(1000)
                elif aircraft.controller == 'Player_B':
                    if keys[pygame.K_k]:
                        aircraft.theta += math.pi * dt
                    elif keys[pygame.K_SEMICOLON]:
                        aircraft.theta -= math.pi * dt
                    if keys[pygame.K_l]:
                        # Check if there is already a missile from Player B, if so -> Don't spawn
                        if sum(checker.owner == aircraft for checker in objects_in_air) <= 0 and tsim > spawn_protection:
                            objects_in_air.append(Airplane('Missile', (aircraft.x, aircraft.y), aircraft.theta, missile_speed, 'Missile', aircraft))
                        elif tsim < spawn_protection:
                            print('Spawn protection!')
                    if keys[pygame.K_SPACE]:
                        time.sleep(1000)
                elif aircraft.controller == 'Computer':
                    aircraft.theta += calculate_turn(aircraft, red_plane)
                elif aircraft.controller == 'Missile':
                    ...

                aircraft.vx = aircraft.velocity * math.cos(aircraft.theta)
                aircraft.vy = aircraft.velocity * math.sin(aircraft.theta)

                aircraft.x += aircraft.vx * dt / RESOLUTION[0]
                aircraft.y += aircraft.vy * dt / RESOLUTION[1]

                if aircraft.x < 0:
                    aircraft.x = 1
                elif aircraft.x > 1:
                    aircraft.x = 0

                if aircraft.y < 0:
                    aircraft.y = 1
                elif aircraft.y > 1:
                    aircraft.y = 0

                aircraft.rotate()

                aircraft.plane_rect.centerx = aircraft.x_to_draw
                aircraft.plane_rect.centery = aircraft.y_to_draw

                aircraft.update(dt)

                if aircraft.controller == 'Missile':
                    for checker in objects_in_air:
                        if checker != aircraft.owner and checker != aircraft and checker.controller != 'Missile':
                            distance = math.sqrt((aircraft.x - checker.x) ** 2 + (aircraft.y - checker.y)**2)
                            print(checker.controller, checker.x, checker.y, aircraft.x, aircraft.y, distance)
                            if distance < 0.1:
                                print(f"{checker.controller} Destroyed!")

                                final_x, final_y = checker.x, checker.y
                                explosion = True
                                running = True
                                objects_in_air.remove(checker)

                    if aircraft.alive_time > 1.:
                        objects_in_air.remove(aircraft)

            tsim += dt

        for aircraft in objects_in_air:
            screen.blit(aircraft.plane, aircraft.plane_rect)

        pg.display.flip()
        # print(len(objects_in_air))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = True

    frame = 0
    frames = [pg.image.load('Visual_Files/ex1.gif'),
              pg.image.load('Visual_Files/ex2.gif'),
              pg.image.load('Visual_Files/ex3.gif'),
              pg.image.load('Visual_Files/ex4.gif')]

    Explosion().explode()

    while explosion:
        frames_rect = frames[frame].get_rect()
        frames_rect.centerx = final_x * RESOLUTION[0]
        frames_rect.centery = RESOLUTION[1] - final_y * RESOLUTION[1]
        screen.blit(frames[frame], frames_rect)
        pg.display.flip()
        time.sleep(0.25)
        frame += 1
        if frame >= len(frames):
            time.sleep(5)
            explosion = False

    remaining_player = str([player.controller for player in objects_in_air if player.controller != 'Missile']).replace('[', '').replace(']', '')
    print(f'The game is over, {remaining_player} has won!')
    # Stop the game based on parameters
    pg.quit()


if __name__ == '__main__':
    main()
