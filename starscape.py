#!/usr/bin/python
from random import sample, randint, random
import string
import platform
import os,sys
import subprocess
from optparse import OptionParser

ship = [
    # A = red
    # B = black
    # C = bold yellow
    # D = cyan
    # E = blue
    # Z = reset
    "       B.---.Z   ",
    " A=   B_/__D~0B_E\B_Z ",
    "A= A= B(C_________ZB)Z",
]

north = [
    # A = color 1
    # B = color 2
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

stars_1 = [("A%sZ"%x,) for x in ",'`."]
stars_2 = [("A%sZ"%x,) for x in "*oXx#"]
stars_3 = [("A%sZ"%x,) for x in "!-+:;@()"]
stars_4 = [
    ("A-B0A-Z",),
    ("A- B) A-Z",),
    (" A|Z ",
     "A-BOA-Z",
     " A|Z ",),
    (" A|Z ",
     "A-BoA-Z",
     " A|Z ",),
    (" A|Z ",
     "A-BxA-Z",
     " A|Z ",),
    ("A - Z",
     "A|BoA|Z",
     "A - Z",),
]

class IColor(type):
    __color = dict(
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
    __fg = dict(
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
    __bg = dict(
        black          = "\x1b[40m", #set background color to black
        red            = "\x1b[41m", #set background color to red
        green          = "\x1b[42m", #set background color to green
        yellow         = "\x1b[43m", #set background color to yellow
        blue           = "\x1b[44m", #set background color to blue
        magenta        = "\x1b[45m", #set background color to magenta (purple)
        cyan           = "\x1b[46m", #set background color to cyan
        white          = "\x1b[47m", #set background color to white
        default        = "\x1b[49m", #set background color to default (black)
    )

    def __getattr__(cls, name):
        if name.startswith("bg_"):
            if name[3:] in cls.__bg:
                return cls.__bg[name[3:]]
        elif name in cls.__fg:
            return cls.__fg[name]
        elif name in cls.__bg:
            return cls.__bg[name]
        elif name in cls.__color:
            return cls.__color[name]
        elif name == "fgs":
            return cls.__fg.values()
        elif name == "bgs":
            return cls.__bg.values()
        elif name == "colors":
            return cls.__color.values()
        elif name.startswith("rand"):
            if name.endswith("fg"):
                return cls.__fg.values()[randint(0, len(cls.__fg)-1)]
            elif name.endswith("bg"):
                return cls.__bg.values()[randint(0, len(cls.__bg)-1)]
        else:
            raise AttributeError(name)

class C(object):
    __metaclass__ = IColor

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


def sys_info():
    nun = ('', '', '')
    linux = platform.linux_distribution() #('Ubuntu', '9.10', 'karmic')
    mac = platform.mac_ver() # ('10.6.7', ('', '', ''), 'i386')
    sys = ""
    if mac != nun:
        sys = "Mac OS X " + mac[0]
    if linux != nun:
        sys = linux

    uptime = subprocess.Popen(["uptime"], stdout=subprocess.PIPE).communicate()[0]
    d = dict(
        user=os.environ.get("USER"),
        shell=os.environ.get("SHELL"),
        home=os.environ.get("HOME"),
        uptime=uptime,
        sys=sys,
    )
    info = "%(shell)s || %(user)s@%(home)s || %(sys)s || uptime:%(uptime)s"%d
    info = info.replace("\n", "")
    return info


def colorize(chars, *colors):
    """Rplaces the [A-Z] flags with respective colors in the *colors list"""
    AZ = string.uppercase[:-1]
    out = chars
    ittr = zip(AZ, colors)
    for i in ittr:
        out = out.replace(i[0], i[1])
    out = out.replace("Z", C.reset)
    return out


def format_scape(s, simple=False):
    """Prints out the scape in a border of pipes"""
    out = []
    for x in s:
        line = ""
        for y in x:
            line = line + (" " if len(y) == 0 else "".join(y))
        out.append(line+C.reset)

    ret = C.black+                                                         \
      border_top(".","=")+"\n"+                                            \
      "|"+("%(bl)s|\n%(bl)s|"%{'bl':C.black}).join(out)+C.black+"|\n"+     \
      ( border_top(":","=")+"\n"+                                          \
        "| "+C.red+C.bold+sys_info().ljust(width - 3, " ")+C.black+"|\n"   \
        if not simple else "" ) +                                          \
        border_top("'","=")+C.reset

    return ret


def write_char(replace, char):
    if invisible(char):
        replace.append(char)
        return replace
    else:
        return [char]


def get_star():
    roll = random()
    if roll < .60:
        stars = (stars_1, 1)
    elif roll < .80:
        stars = (stars_2, 2)
    elif roll < .96:
        stars = (stars_3, 3)
    elif roll < 1:
        stars = (stars_4, 4)
    return (stars[0][int(roll*100%len(stars))], stars[1])


def add_star(scape, x, y, star, color_func=colorize):
    i = 0
    j = 0
    jp = 0

    c1 = C.rand_fg
    c2 = C.rand_fg
    c3 = C.rand_fg

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


def opts(args):
    parser = OptionParser()
    parser.add_option("-c", "--cols", dest="cols", type="int")
    parser.add_option("-r", "--rows", dest="rows", type="int")
    parser.add_option("--simple", dest="simple", action="store_true")
    return parser.parse_args()

(width, height) = getTerminalSize()

Y = 15
X = width - 2

wrap_x = lambda w:w%X
wrap_y = lambda w:w%Y


empty_space = lambda x, y, z: [[z]*y for foo in xrange(0, x)]
loaded_dice = lambda w: True if random() <= w else False
border_top = lambda edge, fill: edge+fill*X+edge
invisibles = "ABCDEFGHIJKLMNPQRSTUVWXYZ"
invisible = lambda char: True if char in invisibles else False
colors_ship = [C.red, C.black, C.yellow+C.bold, C.cyan, C.blue]
colors_north = [C.rand_fg, C.rand_fg]
colorize_ship = lambda x, *args: colorize(x, *colors_ship)
colorize_north = lambda x, *args: colorize(x, *colors_north)


def main(args=None, count=200):
    global X, Y

    if args is None:
        args = sys.argv

    (options, args) = opts(args)

    if options.rows:
        Y = options.rows

    if options.cols:
        X = options.cols

    simple = False
    if options.simple:
        simple = True

    scape = empty_space(Y, X, [])
    for x in xrange(0, count):
        x, y = (randint(0, X), randint(0, Y))
        star = get_star()[0]
        add_star(scape, x, y, star)

    add_star(scape, 2, 8, ship, colorize_ship)
    add_star(scape, width - 52, 2, north, colorize_north)
    add_star(scape, width -19, 2, stars_3[3])

    print format_scape(scape, simple=simple)

if __name__ == "__main__":
    main()

