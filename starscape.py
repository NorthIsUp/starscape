#!/bin/python

from random import sample, randint, random

ship = [
"       .---.   ",
" =   _/__~0_\_ ",
"= = (_________)",
]

north = [
"    )                     (",
" ( /(             )   )   )\ )",
"  )\())    (   ( /(( /(  (()/(       (",
"((_)\  (  )(  )\())\())  /(_)|       )\  , )",
" _((_) )\(()\(_))(_))\  (_)) )\   _ ((_)/(/(",
"| \| |((_)((_) |_| |(_) |_ _((_) | | | ((_)_\\",
"| .` / _ \ '_|  _| ' \   | |(_-< | |_| | '_ \)",
"|_|\_\___/_|  \__|_||_| |___/__/  \___/| .__/",
"                                       |_|",
]

stars_1 = [(x,) for x in ",'`.*oXx"]
stars_2 = [(x,) for x in "#!@()-+:;"]
stars_3 = [
("-0-",),
("- ) -",),
(" | ",
 "-O-",
 " | ",),
(" | ",
 "-o-",
 " | ",),
(" - ",
 "|O|",
 " - ",),
]

color = dict(
reset           = "\x1b[0m" , #reset; clears all colors and styles (to white on black)
bold            = "\x1b[1m" , #bold on (see below)
italics         = "\x1b[3m" , #italics on
underline       = "\x1b[4m" , #underline on
inverse         = "\x1b[7m" , #inverse on; reverses foreground & background colors
strike          = "\x1b[9m" , #strikethrough on

no_bold         = "\x1b[22m", #bold off (see below)
no_italics      = "\x1b[23m", #italics off
no_underline    = "\x1b[24m", #underline off
no_inverse      = "\x1b[27m", #inverse off
no_strike       = "\x1b[29m", #strikethrough off
)

fg = dict(
black           = "\x1b[30m", #set foreground color to black
red             = "\x1b[31m", #set foreground color to red
green           = "\x1b[32m", #set foreground color to green
yellow          = "\x1b[33m", #set foreground color to yellow
blue            = "\x1b[34m", #set foreground color to blue
magenta         = "\x1b[35m", #set foreground color to magenta (purple)
cyan            = "\x1b[36m", #set foreground color to cyan
white           = "\x1b[37m", #set foreground color to white
default         = "\x1b[39m", #set foreground color to default (white)
)

bg = dict(
black           = "\x1b[40m", #set background color to black
red             = "\x1b[41m", #set background color to red
green           = "\x1b[42m", #set background color to green
yellow          = "\x1b[43m", #set background color to yellow
blue            = "\x1b[44m", #set background color to blue
magenta         = "\x1b[45m", #set background color to magenta (purple)
cyan            = "\x1b[46m", #set background color to cyan
white           = "\x1b[47m", #set background color to white
default         = "\x1b[49m", #set background color to default (black)
)

reset = color['reset']
Y = 15
X = 200

empty_space = lambda x, y, z: [[z]*y for foo in xrange(0, x)]
print_scape = lambda s: "|"+"|\n|".join(["".join(y) for y in s])+"|"
loaded_dice = lambda w: True if random() <= w else False
border_top = lambda edge, fill: edge+fill*X+edge
wrap_x = lambda w:w%X
wrap_y = lambda w:w%Y
def write_char(replace, char):
    if char in fg.values() or char in bg.values():
        return char+replace
    else:
        if "\x1b" in replace:
            return replace
        else:
            return char

invisible = lambda char: True if char in fg.values() or char in bg.values() else False


scape = empty_space(Y, X, " ")
def get_star():
    roll = random()
    if roll < .6:
        stars = stars_1
    elif roll < .95:
        stars = stars_1
    elif roll < 1:
        stars = stars_3
    return stars[int(roll*100%len(stars))]

def add_star(x, y, star):
    # star = colorize(star)
    i = 0
    for col in star:
        j = 0
        jp = 0
        for row in col:
            s = star[i][j]
            scape[wrap_y(y+i)][wrap_x(x+jp)] = write_char(scape[wrap_y(y+i)][wrap_x(x+jp)], s)
            if not invisible(s):
                jp += 1
            j+=1
        i += 1

def rand_color():
    return fg.values()[randint(0, len(fg)-1)]


def colorize(scape):
    s2=""
    for i, x in enumerate(scape):
        if x == "|":
            s2 += reset + x
        elif x != " ":
            s2 += rand_color() + x
        else:
            s2 += x
    # for s in (stars_1, stars_2, stars_3):
    #     for x in s:
    #         for row in x:
    #             for col in row:
    #                 c1 = rand_color()
    #                 scape = scape.replace(col,c1+col)
    return s2
def main(count=100):
    for x in xrange(0, count):
        x, y = (randint(0, X), randint(0, Y))
        star = get_star()
        add_star(x, y, star)

    print border_top(".","=")
    print colorize(print_scape(scape))
    print border_top(":","=")
    print border_top("'","=")
    print fg['red']+"that's all folks!"+reset

if __name__ == "__main__":
    main()
