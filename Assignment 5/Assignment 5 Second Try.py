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

aircraft_speed = 100
aircraft_rotation = math.pi
computer_rotation = math.pi - 0.7
missile_speed = 1000
spawn_protection = 1

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

    # This list will contain all flying objects in the air at all times
    objects_in_air = []

    # Create aircraft
    red_plane = Airplane('Red', red_start_pos, math.pi,  aircraft_speed, 'Player_A')
    blue_plane = Airplane('Blue', blue_start_pos, 0.0, aircraft_speed, 'Player_B')

    # Put aircraft in the objects in air list
    objects_in_air.append(red_plane)
    objects_in_air.append(blue_plane)

    # Initialize the main game
    pg.init()

    # Colours to draw
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)

    # Time settings
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

                def calculate_turn(self: Airplane, other: Airplane) -> float:

                    # This function is called ONLY when one or more of the aircraft is a COMPUTER.
                    # This is just an autopilot function to direct the aircraft towards the other one

                    offset = 2
                    distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y)**2 )
                    print(self.theta)
                    # pg.draw.line(screen, green, (self.x_to_draw, self.y_to_draw), (self.x_to_draw + distance * math.cos(-self.theta) * RESOLUTION[0], self.y_to_draw + distance * math.sin(-self.theta) * RESOLUTION[1]))

                    if self.y_to_draw + distance * math.sin(-self.theta) * RESOLUTION[1] > other.y_to_draw + offset:
                        if self.x_to_draw < other.x_to_draw - offset:
                            return computer_rotation * dt
                        elif self.x_to_draw > other.x_to_draw + offset:
                            return - computer_rotation * dt
                        else:
                            return 0
                    elif self.y_to_draw + distance * math.sin(-self.theta) * RESOLUTION[1] < other.y_to_draw - offset:
                        if self.x_to_draw < other.x_to_draw - offset:
                            return - computer_rotation * dt
                        elif self.x_to_draw > other.x_to_draw + offset:
                            return computer_rotation * dt
                        else:
                            return 0
                    else:
                        return 0


                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    print('ESCAPE KEY HAS BEEN PRESSED, EXITING GAME')
                    pg.quit()

                # Checks the current aircraft for which keys they should be pressing to control the aircraft
                if aircraft.controller == 'Player_A':
                    if keys[pygame.K_a]:
                        aircraft.theta += math.pi * dt
                    elif keys[pygame.K_d]:
                        aircraft.theta -= math.pi * dt
                    if keys[pygame.K_s]:
                        # If the A key is pressed, spawn a missile in the direction and location of the aircraft
                        # Check if there is already a missile from Player A, if so -> Don't spawn
                        if sum(checker.owner == aircraft for checker in objects_in_air) <= 0 and tsim > spawn_protection:
                            objects_in_air.append(Airplane('Missile', (aircraft.x, aircraft.y), aircraft.theta,  missile_speed, 'Missile', aircraft))
                    if keys[pygame.K_SPACE]:
                        time.sleep(1000)
                elif aircraft.controller == 'Player_B':
                    if keys[pygame.K_k]:
                        aircraft.theta += math.pi * dt
                    elif keys[pygame.K_SEMICOLON]:
                        aircraft.theta -= math.pi * dt
                    if keys[pygame.K_l]:
                        # If the A key is pressed, spawn a missile in the direction and location of the aircraft
                        # Check if there is already a missile from Player B, if so -> Don't spawn
                        if sum(checker.owner == aircraft for checker in objects_in_air) <= 0 and tsim > spawn_protection:
                            objects_in_air.append(Airplane('Missile', (aircraft.x, aircraft.y), aircraft.theta, missile_speed, 'Missile', aircraft))
                    if keys[pygame.K_SPACE]:
                        time.sleep(1000)
                elif aircraft.controller == 'Computer':
                    # This is the autopilot function, it directs the computer to the player, then fires if it's in the
                    # direction and a steering input of 0 is detected (aka facing the opponent)
                    aircraft.theta += calculate_turn(aircraft, [other_aircraft for other_aircraft in objects_in_air if other_aircraft != aircraft and other_aircraft.controller != 'Missile'][0])
                    if sum(checker.owner == aircraft for checker in objects_in_air) <= 0 and tsim > spawn_protection and calculate_turn(aircraft, red_plane) == 0:
                        objects_in_air.append(Airplane('Missile', (aircraft.x, aircraft.y), aircraft.theta, missile_speed, 'Missile', aircraft))
                elif aircraft.controller == 'Missile':
                    # Not implemented, missiles only go in a straight line. No missile steering implemented
                    ...

                # Update the aircraft parameters
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

                # Update the direction of the aircraft image
                aircraft.rotate()

                aircraft.plane_rect.centerx = aircraft.x_to_draw
                aircraft.plane_rect.centery = aircraft.y_to_draw

                aircraft.update(dt)

                # Check if the missile is within explosion distance of the fired-upon object
                # It does this by checking if:
                #   - Other object is not self
                #   - Other object is not a missile
                #   - Other object is not the owner of the missile (otherwise it would instantly explode)
                #   - Other object is the OTHER aircraft (Only option left at this point, passing all NOT statements)
                if aircraft.controller == 'Missile':
                    for checker in objects_in_air:
                        if checker != aircraft.owner and checker != aircraft and checker.controller != 'Missile':
                            distance = math.sqrt((aircraft.x - checker.x) ** 2 + (aircraft.y - checker.y)**2)
                            if distance < 0.05:
                                print(f"{checker.controller} Destroyed!")

                                final_x, final_y = checker.x, checker.y
                                explosion = True
                                running = True
                                objects_in_air.remove(checker)
                                objects_in_air.remove(aircraft)

                    # Delete the missile from the screen and aircraft list so it's not slowing down the game
                    # You can see this by printing the list of the aircraft
                    if aircraft.alive_time > 1.:
                        objects_in_air.remove(aircraft)

            # Increment time
            tsim += dt

        # Draw all objects in the objects_in_air list.
        for aircraft in objects_in_air:
            screen.blit(aircraft.plane, aircraft.plane_rect)

        pg.display.flip()
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
            time.sleep(2)
            explosion = False

    # A very pythonist way of getting only the aircraft that has won, and filtering out all missiles
    remaining_player = str([player.controller for player in objects_in_air if player.controller != 'Missile']).replace('[', '').replace(']', '')
    print(f'The game is over, {remaining_player} has won!')
    # Stop the game based on parameters
    pg.quit()


if __name__ == '__main__':
    main()
