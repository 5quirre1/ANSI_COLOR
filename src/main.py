import sys
import platform
import ctypes

ANSI_COLORS = {
    "BLACK": "\033[0;30m", "RED": "\033[0;31m", "GREEN": "\033[0;32m", "BROWN": "\033[0;33m",
    "BLUE": "\033[0;34m", "PURPLE": "\033[0;35m", "CYAN": "\033[0;36m", "LIGHT_GRAY": "\033[0;37m",
    "DARK_GRAY": "\033[1;30m", "LIGHT_RED": "\033[1;31m", "LIGHT_GREEN": "\033[1;32m", "YELLOW": "\033[1;33m",
    "LIGHT_BLUE": "\033[1;34m", "LIGHT_PURPLE": "\033[1;35m", "LIGHT_CYAN": "\033[1;36m", "LIGHT_WHITE": "\033[1;37m",

    "BG_BLACK": "\033[40m", "BG_RED": "\033[41m", "BG_GREEN": "\033[42m", "BG_YELLOW": "\033[43m",
    "BG_BLUE": "\033[44m", "BG_PURPLE": "\033[45m", "BG_CYAN": "\033[46m", "BG_LIGHT_GRAY": "\033[47m",
    "BG_DARK_GRAY": "\033[100m", "BG_LIGHT_RED": "\033[101m", "BG_LIGHT_GREEN": "\033[102m", "BG_LIGHT_YELLOW": "\033[103m",
    "BG_LIGHT_BLUE": "\033[104m", "BG_LIGHT_PURPLE": "\033[105m", "BG_LIGHT_CYAN": "\033[106m", "BG_WHITE": "\033[107m",

    "BOLD": "\033[1m", "FAINT": "\033[2m", "ITALIC": "\033[3m", "UNDERLINE": "\033[4m", "CROSSED": "\033[9m",
    "END": "\033[0m"
}

def rgb(r, g, b, background=False):
    code = 48 if background else 38
    return f"\033[{code};2;{r};{g};{b}m"

def hex_color(hexcode, background=False):
    hexcode = hexcode.lstrip("#")
    if len(hexcode) != 6:
        raise ValueError("Hex code must be in format RRGGBB")
    r, g, b = int(hexcode[0:2], 16), int(hexcode[2:4], 16), int(hexcode[4:6], 16)
    return rgb(r, g, b, background)

def color(text, fg=None, bg=None, style=None):
    result = ""
    if style:
        result += ANSI_COLORS.get(style.upper(), "")
    if fg:
        result += hex_color(fg) if fg.startswith("#") else ANSI_COLORS.get(fg.upper(), "")
    if bg:
        result += hex_color(bg, background=True) if bg.startswith("#") else ANSI_COLORS.get("BG_" + bg.upper(), "")
    return result + text + ANSI_COLORS["END"]

if not sys.stdout.isatty():
    for key in ANSI_COLORS:
        ANSI_COLORS[key] = ""
elif platform.system() == "Windows":
    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)

if __name__ == '__main__':
    print(color("wow", fg="#df15c0"))
