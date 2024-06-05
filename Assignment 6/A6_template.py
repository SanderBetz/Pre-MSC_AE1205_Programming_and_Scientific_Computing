''' Load an image from file and print as ASCII art to the screen! '''
import numpy as np
import pygame as pg
   
# This script creates an ASCII image from a JPG file supplied.
# In the IMAGE_NAME variable you can put the string of the file name
# In the FONTSIZE variable you can put the resolution you want the image to be represented in

# The file will create a picture in the "Screenshots" directory with the following name:
#   ---> IMAGE_NAME + Scaled_ + FONTSIZE + .jpg

also_view_photo = False

fontSize = 10
font_antiAliasing = False

image_name = 'swarm_of_drones'

# A list of characters that you can use in your ASCII art...
characters = ['M', 'W', 'Q', 'B', 'E', 'R', 'N', '@', 'H', 'q', 'p', 'g', 'K', 'A', '#', 'm', 'b', '8', '0', 'd', 'X', 'D', 'G', 'F', 'P', 'e', 'h', 'U', '9', '6', 'k', 'Z', '%', 'S', '4', 'O', 'x', 'y', 'T', '5', 'w', 'f', 'a', 'V', 's',
                '2', 'L', '$', 'Y', '&', 'n', '3', 'C', 'J', 'u', 'o', 'z', 'I', 'j', 'v', 'c', 'r', 't', 'l', 'i', '1', '=', '?', '7', '>', '<', ']', '[', '(', ')', '+', '*', ';', '}', '{', ':', '/', '\\', '!', '|', '_', ',', '^', '-', '~', '.', ' ']
n_characters = len(characters)

# ... and the corresponding grayscale values
grayscale = [217.56944444, 218.82291667, 219.89236111, 220.19444444,
                      222.14583333, 222.94097222, 223.0625, 223.17361111,
                      223.22222222, 223.23958333, 223.45486111, 223.60416667,
                      224.05208333, 224.09722222, 224.33333333, 225.25,
                      225.59722222, 225.62152778, 225.91666667, 225.96180556,
                      226.10763889, 226.74305556, 226.80208333, 227.04861111,
                      227.42361111, 228.45833333, 228.61458333, 228.73958333,
                      228.76736111, 228.80555556, 228.8125, 228.90625,
                      228.98611111, 229.06597222, 229.28472222, 229.61805556,
                      229.96527778, 230.07291667, 230.17361111, 230.21875,
                      230.60416667, 230.62847222, 230.84375, 231.03472222,
                      231.05555556, 231.46875, 231.55555556, 231.9375,
                      232.04861111, 232.07291667, 232.64583333, 232.68055556,
                      233.16319444, 233.53472222, 233.70138889, 234.20833333,
                      234.40625, 234.76388889, 234.93055556, 235.30208333,
                      235.36805556, 235.44791667, 235.5, 236.53472222,
                      237.32986111, 237.67361111, 237.70138889, 238.61458333,
                      238.61805556, 238.78125, 238.78472222, 238.79166667,
                      238.98611111, 239.07638889, 239.08680556, 239.97569444,
                      240.32291667, 240.78125, 241.50694444, 241.57291667,
                      242.25694444, 243.13194444, 243.18055556, 243.31944444,
                      244.30208333, 244.61805556, 245.03819444, 246.62847222,
                      247.58333333, 247.60763889, 248.62847222, 255.0]

char_map = {key: value for key, value in zip(grayscale, characters)}
# Start writing your code here!
class Character:
    def __init__(self, x, y, width, height):
        # X and Y are location identifiers, not pixel coordinates
        self.x = x
        self.y = y

        # Character width and height
        self.width = width
        self.height = height

        # Create the lists of pixel values that are to be used
        self.rvals = []
        self.gvals = []
        self.bvals = []

    def calc_average(self):
        def avg(vals):
            return sum(vals) / len(vals) if len(vals) != 0 else min(grayscale)
        # Create the variables to work with
        self.r_avg = avg(self.rvals)
        self.g_avg = avg(self.gvals)
        self.b_avg = avg(self.bvals)

    def greyscale_pixel_NTSC(self):
        self.greyscale_value = 0.299 * self.r_avg + 0.587 * self.g_avg + 0.114 * self.b_avg
        self.greyscale_value_normalized = 217.56944444 + (self.greyscale_value / 255.) * (255. - 217.56944444)

    def letter(self):
        self.character = None
        for i, key in enumerate(grayscale[:-1]):
            # print(abs(self.greyscale_value_normalized - grayscale[i + 1]) , abs(self.greyscale_value_normalized - key))
            if abs(self.greyscale_value_normalized - grayscale[i + 1]) > abs(self.greyscale_value_normalized - key):
                self.character = char_map[key]
                break
        if self.character == None:
            self.character = char_map[255.0]
def main():
    image = pg.image.load(f'Photos/{image_name}.jpg')

    RESOLUTION = image.get_size()
    screen = pg.display.set_mode(RESOLUTION)

    black = (0, 0, 0)
    white = (255, 255, 255)

    pg.draw.rect(screen, black, screen.get_rect())
    pg.init()

    font = pg.font.SysFont('Courier New', fontSize, black)
    txt = font.render(' ', False, white)

    if also_view_photo:
        screen.blit(image, image.get_rect())

    # Get the pixel information from the pygame image
    r_array = pg.surfarray.pixels_red(image)
    g_array = pg.surfarray.pixels_green(image)
    b_array = pg.surfarray.pixels_blue(image)

    char_width = txt.get_width()
    char_height = txt.get_height()

    image_width = screen.get_width()
    image_height = screen.get_height()

    num_chars_hor = image_width // char_width
    num_chars_ver = image_height // char_height

    # Create Character objects to put the pixel information in
    char_list = [[Character(x, y, char_width, char_height) for y in range(num_chars_ver + 1)] for x in range(num_chars_hor + 1)]

    # Put all pixel values in their corresponding character, which have a fixed width and height
    i = -1
    for x, (column_r, column_g, column_b) in enumerate(zip(r_array, g_array, b_array)):
        j = -1
        if x % char_width == 0:
            i += 1
        for y, (pixel_r, pixel_g, pixel_b) in enumerate(zip(column_r, column_g, column_b)):
            if y % char_height == 0:
                j += 1
            (char_list[i][j].rvals).append(pixel_r)
            (char_list[i][j].gvals).append(pixel_g)
            (char_list[i][j].bvals).append(pixel_b)

    # We now have all characters' pixel values stored in a Character object char_list
    # Just put all characters in a single line list for ease of programming later
    characters_1D = [y for x in char_list for y in x]

    # Calculate the averages and greyscale values for each pixel

    for char in characters_1D:
        # Use all functions in the object, now that the lists have been filled with information
        char.calc_average()
        char.greyscale_pixel_NTSC()
        char.letter()

        # Display the letter to the screen on the location where the object points it to
        text = font.render(char.character, font_antiAliasing, white)
        textRect = text.get_rect()

        textRect.centerx = char.x * char_width + char_width // 2
        textRect.centery = char.y * char_height + char_width // 2

        screen.blit(text, textRect)

    pg.image.save(screen, f'Screenshots/{image_name}GreyScaled_{str(fontSize)}.jpg')
    pg.quit()

if __name__ == '__main__':
    main()