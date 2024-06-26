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

class Airplane:
    def __init__(self, aircraft_type: str, location: tuple, direction: float, velocity: int, controller: str):
        self.aircraft_type : str    = aircraft_type
        self.x             : int    = location[0]
        self.y             : int    = location[1]
        self.theta         : float  = direction
        self.velocity      : int    = velocity
        self.vx            : float  = velocity * math.cos(self.theta)
        self.vy            : float  = velocity * math.sin(self.theta)
        self.controller    : str    = controller

        if self.aircraft_type == 'Red':
            img = pg.image.load('Visual_Files/redship.png')
        elif self.aircraft_type == 'Blue':
            img = pg.image.load('Visual_Files/blueship.png')
        elif self.aircraft_type == 'Missile':
            img = pg.image.load('Visual_Files/missile.png.png')

        img = pg.transform.scale(img, (img.get_width() * 0.12, img.get_height() * 0.12))
        self.img_list = {angle : pg.transform.rotate(img, -angle) for angle in range(361)}
        img = self.img_list[int(math.degrees(self.theta))]

        self.plane = img
        self.plane_rect = img.get_rect()

    def rotate(self):
        if math.degrees(self.theta) >= 360:
            self.theta = math.degrees(0)
        elif math.degrees(self.theta) <= 0:
            self.theta = math.radians(360)

        self.plane = self.img_list[int(math.degrees(self.theta))]
        self.plane_rect = self.plane.get_rect()

def main():

    # Initialize the game setup

    RESOLUTION = (1000, 800)
    screen = pg.display.set_mode(RESOLUTION)
    scrrect = screen.get_rect()

    # Put planes 100 px of center
    red_start_pos   = (((RESOLUTION[0] / 2) - 100) / RESOLUTION[0],
                     int(RESOLUTION[1] / 2) / RESOLUTION[1])

    blue_start_pos  = (((RESOLUTION[0] / 2) + 100) / RESOLUTION[0],
                     int(RESOLUTION[1] / 2) / RESOLUTION[1])

    print(red_start_pos)
    
    red_plane = Airplane('Red', red_start_pos, math.pi,  100, 'Player')
    blue_plane = Airplane('Blue', blue_start_pos, 0.1, 100, 'Computer')

    print(f'Red Plane: \n'
          f'x, y: {red_plane.x}, {red_plane.y} \n'
          f'vx, vy: {red_plane.vx}, {red_plane.vy}')

    r_plane = red_plane.plane.get_rect()
    b_plane = blue_plane.plane.get_rect()

    # Initialize the main game
    pg.init()

    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    dt = 0.01
    tsim = 0.0
    tstart = 0.001 * pg.time.get_ticks()

    running = False
    # Main game loop
    while not running:
        # Draw black background, so all objects are hidden
        pg.draw.rect(screen, black, scrrect)
        trun = 0.001 * pg.time.get_ticks() - tstart

        if trun + dt >= tsim:
            red_plane.vx = red_plane.velocity * math.cos(red_plane.theta)
            red_plane.vy = red_plane.velocity * math.sin(red_plane.theta)

            blue_plane.vx = blue_plane.velocity * math.cos(blue_plane.theta)
            blue_plane.vy = blue_plane.velocity * math.sin(blue_plane.theta)

            red_plane.x += red_plane.vx * dt / RESOLUTION[0]
            red_plane.y += red_plane.vy * dt / RESOLUTION[1]

            blue_plane.x += blue_plane.vx * dt / RESOLUTION[0]
            blue_plane.y += blue_plane.vy * dt / RESOLUTION[1]

            r_plane.centerx = red_plane.x * RESOLUTION[0]
            r_plane.centery = red_plane.y * RESOLUTION[1]

            b_plane.centerx = blue_plane.x * RESOLUTION[0]
            b_plane.centery = blue_plane.y * RESOLUTION[1]

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                red_plane.theta -= math.pi * dt
            elif keys[pygame.K_d]:
                red_plane.theta += math.pi * dt
            if keys[pygame.K_SPACE]:
                print(f'pausing sim: \n'
                      f'red x, y : {red_plane.x * RESOLUTION[0], red_plane.y * RESOLUTION[1]} \n'
                      f'blue x, y : {blue_plane.x * RESOLUTION[0], blue_plane.y * RESOLUTION[1]} \n'
                      f'blue Theta: {math.degrees(blue_plane.theta)}')
                time.sleep(100)

            def move_to_target(self: Airplane, other: Airplane):
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if self.theta < math.pi:
                    selfangle = self.theta
                elif self.theta > math.pi:
                    selfangle = - (2 * math.pi - self.theta)

                # print(math.degrees(math.atan2(dy, dx)), math.degrees(selfangle))
                angleDiff = math.atan2(dy, dx) - selfangle
                print(angleDiff)

                if angleDiff > math.radians(5) or angleDiff < - math.pi:
                    if angleDiff > math.pi:
                        return - math.pi * dt / 2
                    return math.pi * dt / 2
                elif angleDiff < -math.radians(5) or angleDiff > math.pi:
                    return - math.pi * dt / 2
                else:
                    return 0

            turn_to_do = move_to_target(blue_plane, red_plane)

            blue_plane.theta += turn_to_do
            if turn_to_do == 0:
                missile = Airplane('Missile', (blue_plane.x * RESOLUTION[0], blue_plane.y * RESOLUTION[1]), blue_plane.theta,  1000, 'Computer')
                m_plane = red_plane.plane.get_rect()

            red_plane.rotate()
            blue_plane.rotate()

            tsim += dt

        """
        pg.draw.line(screen, white, (blue_plane.x * RESOLUTION[0], blue_plane.y * RESOLUTION[1]),
                     (red_plane.x * RESOLUTION[0], red_plane.y * RESOLUTION[1]))
        pg.draw.line(screen, white, (0, blue_plane.y * RESOLUTION[1]),
                     (RESOLUTION[0], blue_plane.y * RESOLUTION[1]))

        pg.draw.line(screen, green,
                     (blue_plane.x * RESOLUTION[0], blue_plane.y * RESOLUTION[1]),
                     (blue_plane.x * RESOLUTION[0] + math.cos(blue_plane.theta) * 1000,
                      blue_plane.y * RESOLUTION[1] + math.sin(blue_plane.theta) * 1000))
        """

        screen.blit(red_plane.plane, r_plane)
        screen.blit(blue_plane.plane, b_plane)

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = True

    # Stop the game based on parameters
    pg.quit()


if __name__ == '__main__':
    main()
