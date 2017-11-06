#!/usr/bin/python3
import argparse
import json

CUSTOM_COLOR_PATH = '/home/pi/lights/custom_colors'

parser = argparse.ArgumentParser()
parser.add_argument("color", help="Specify which color to modify.", type=str)
parser.add_argument("number", help="Specify if modifying color 1 or 2.", type=int)
parser.add_argument("direction", help="Specify if color value should be modified up or down.", type=str)

def get_color_values():
    with open(CUSTOM_COLOR_PATH, 'r') as f:
        data = json.load(f)
        return data

def decrement_color(color, green, red, blue):
    if color == 'green':
        green = max(green - 60, 0)
    elif color == 'red':
        red = max(red - 60, 0)
    elif color == 'blue':
        blue = max(blue - 60, 0)
    else:
        parser.print_help()
    return green, red, blue

def increment_color(color, green, red, blue):
    if color == 'green':
        green = min(green + 60, 255)
    elif color == 'red':
        red = min(red + 60, 255)
    elif color == 'blue':
        blue = min(blue + 60, 255)
    else:
        parser.print_help()
    return green, red, blue

def set_colors(color, number, direction):
    color_data = get_color_values()
    green, red, blue = color_data["color" + str(number)]
    if direction.lower() == 'up':
        green, red, blue = increment_color(color, green, red, blue)
    elif direction.lower() == 'down':
        green, red, blue = decrement_color(color, green, red, blue)
    with open(CUSTOM_COLOR_PATH, 'w') as f:
        color_data["color" + str(number)] = green, red, blue
        json.dump(color_data, f)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.color and args.number and args.direction:
        set_colors(args.color, args.number, args.direction)
    else:
        parser.print_help()