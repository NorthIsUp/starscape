#!/usr/bin/python
from random import sample, randint, random
import string
import platform
import os
ship = [
# A = red
# B = black
# C = bold yellow
# D = cyan
# E = blue
"       B.---.Z   ",
" A=   B_/__D~0B_E\B_Z ",
"A= A= B(C_________ZB)Z",
]

north = [
"A    )                     (Z",
"A ( /(             )   )   )\ )Z",
"A  )\())    (   ( /(( /(  (()/(       (Z",
"A((_)\  (  )(  )\())\())  /(_)|       )\  , )Z",
"B _A((B_A) )\(()\(B_A))(B_A))\  A(B_A)) )\   B_A ((B_A)/(/(Z",
"B| \| |A((B_A)((B_A) B|_| |A(_) B|_ _A((B_A) B| | | A((B_A)B_A\\Z",
"B| .` / _ \ '_|  _| ' \   | |(_-< | |_| | '_ \)Z",
"B|_|\_\___/_|  \__|_||_| |___/__/  \___/| .__/Z",
"B                                       |_|Z",
]

stars_1 = [(x,) for x in ",'`.*oXx"]
stars_2 = [(x,) for x in "#!@()-+:;"]
stars_3 = [
("A-B0A-Z",),
("A- B) A-Z",),
(" A|Z ",
 "A-BOA-Z",
 " A|Z ",),
(" A|Z ",
 "A-BoA-Z",
 " A|Z ",),
("A - Z",
 "A|BoA|Z",
 "A - Z",),
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

def getTerminalSize():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

(width, height) = getTerminalSize()

reset = color['reset']
Y = 15
X = width - 2

empty_space = lambda x, y, z: [[z]*y for foo in xrange(0, x)]
loaded_dice = lambda w: True if random() <= w else False
border_top = lambda edge, fill: edge+fill*X+edge
invisibles = "ABCDEFGHIJKLMNPQRSTUVWXYZ"
invisible = lambda char: True if char in invisibles else False
wrap_x = lambda w:w%X
wrap_y = lambda w:w%Y
rand_color = lambda: fg.values()[randint(0, len(fg)-1)]

colors_ship = [fg['red'], fg['black'], fg['yellow']+color['bold'], fg['cyan'], fg['blue']]
colors_north = [rand_color(), rand_color()]
colorize_ship = lambda x, *args: colorize(x, *colors_ship)
colorize_north = lambda x, *args: colorize(x, *colors_north)

def sys_info():
    nun = ('', '', '')
    linux = platform.linux_distribution() #('Ubuntu', '9.10', 'karmic')
    mac = platform.mac_ver() # ('10.6.7', ('', '', ''), 'i386')
    sys = ""
    if mac != nun:
        sys = "Mac OS X " + mac[0]
    if linux != nun:
        sys = linux

    d = dict(
        user=os.environ.get("USER"),
        shell=os.environ.get("SHELL"),
        home=os.environ.get("HOME"),
        sys=sys,
    )
    info = "%(shell)s || %(user)s@%(home)s || %(sys)s"%d
    return info

def colorize(chars, *colors):
    AZ = string.uppercase[:-1]
    out = chars
    ittr = zip(AZ, colors)
    for i in ittr:
        out = out.replace(i[0], i[1])
    out = out.replace("Z", reset)
    return out


def print_scape(s):
    out = []

    for x in s:
        line = ""
        for y in x:
            line = line + (" " if len(y) == 0 else "".join(y))
        out.append(line+reset)
    return "|"+"|\n|".join(out)+"|"


def write_char(replace, char):
    if invisible(char):
        replace.append(char)
        return replace
    else:
        return [char]


scape = empty_space(Y, X, [])
def get_star():
    roll = random()
    if roll < .6:
        stars = stars_1
    elif roll < .95:
        stars = stars_1
    elif roll < 1:
        stars = stars_3
    return stars[int(roll*100%len(stars))]


def add_star(x, y, star, color_func=colorize):
    i = 0
    j = 0
    jp = 0

    c1 = rand_color()
    c2 = rand_color()
    c3 = rand_color()
    
    while True:
        s = ""
        while True:
            if jp >= len(star[i]):
                i += 1
                jp = 0
                j = 0
            if i >= len(star):
                return
            next = star[i][jp]
            jp += 1
            s += next
            if not invisible(next):
                break
        s = color_func(s, c1, c2, c3)
        scape[wrap_y(y+i)][wrap_x(x+j)] = [s]
        j += 1


def main(count=200):
    for x in xrange(0, count):
        x, y = (randint(0, X), randint(0, Y))
        star = get_star()
        add_star(x, y, star)

    add_star(2, 8, ship, colorize_ship)
    add_star(width - 52, 2, north, colorize_north)
    add_star(width -19, 2, stars_3[3])
    print border_top(".","=")
    # print scape
    print print_scape(scape)
    print border_top(":","=")
    print "| " + sys_info().ljust(width - 3, " ") + "|"
    print border_top("'","=")
if __name__ == "__main__":
    main()
