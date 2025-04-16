import sys
import platform
import ctypes
from typing import Optional, Union

ANSI_COLORS = {
    "BLACK": "\033[0;30m", 
    "RED": "\033[0;31m", 
    "GREEN": "\033[0;32m", 
    "BROWN": "\033[0;33m",
    "BLUE": "\033[0;34m", 
    "PURPLE": "\033[0;35m", 
    "CYAN": "\033[0;36m", 
    "LIGHT_GRAY": "\033[0;37m",
    "DARK_GRAY": "\033[1;30m", 
    "LIGHT_RED": "\033[1;31m", 
    "LIGHT_GREEN": "\033[1;32m", 
    "YELLOW": "\033[1;33m",
    "LIGHT_BLUE": "\033[1;34m", 
    "LIGHT_PURPLE": "\033[1;35m", 
    "LIGHT_CYAN": "\033[1;36m", 
    "LIGHT_WHITE": "\033[1;37m",
    "BG_BLACK": "\033[40m", 
    "BG_RED": "\033[41m", 
    "BG_GREEN": "\033[42m", 
    "BG_YELLOW": "\033[43m",
    "BG_BLUE": "\033[44m", 
    "BG_PURPLE": "\033[45m", 
    "BG_CYAN": "\033[46m", 
    "BG_LIGHT_GRAY": "\033[47m",
    "BG_DARK_GRAY": "\033[100m", 
    "BG_LIGHT_RED": "\033[101m", 
    "BG_LIGHT_GREEN": "\033[102m", 
    "BG_LIGHT_YELLOW": "\033[103m",
    "BG_LIGHT_BLUE": "\033[104m", 
    "BG_LIGHT_PURPLE": "\033[105m", 
    "BG_LIGHT_CYAN": "\033[106m", 
    "BG_WHITE": "\033[107m",
    "BOLD": "\033[1m", 
    "FAINT": "\033[2m", 
    "ITALIC": "\033[3m", 
    "UNDERLINE": "\033[4m", 
    "CROSSED": "\033[9m",
    "END": "\033[0m"
}

def enable_windows_ansi():
    if platform.system() == "Windows":
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 4)

def rgb(r: int, g: int, b: int, background: bool = False) -> str:
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    code = 48 if background else 38
    return f"\033[{code};2;{r};{g};{b}m"

def hex_color(hexcode: str, background: bool = False) -> str:
    hexcode = hexcode.lstrip("#")
    if len(hexcode) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in hexcode):
        raise ValueError("hex code must be in format '#RRGGBB' or 'RRGGBB'")
    
    r = int(hexcode[0:2], 16)
    g = int(hexcode[2:4], 16)
    b = int(hexcode[4:6], 16)
    
    return rgb(r, g, b, background)

def color(text: str, 
          fg: Optional[str] = None, 
          bg: Optional[str] = None, 
          style: Optional[Union[str, list]] = None) -> str:
    result = ""
    
    if style:
        if isinstance(style, list):
            for s in style:
                result += ANSI_COLORS.get(s.upper(), "")
        else:
            result += ANSI_COLORS.get(style.upper(), "")
    
    if fg:
        if fg.startswith("#"):
            result += hex_color(fg)
        else:
            result += ANSI_COLORS.get(fg.upper(), "")
    
    if bg:
        if bg.startswith("#"):
            result += hex_color(bg, background=True)
        else:
            bg_key = "BG_" + bg.upper() if not bg.upper().startswith("BG_") else bg.upper()
            result += ANSI_COLORS.get(bg_key, "")
    
    return result + text + ANSI_COLORS["END"]

def disable_colors_if_needed():
    if not sys.stdout.isatty():
        for key in ANSI_COLORS:
            ANSI_COLORS[key] = ""

def demo():
    print("\nText Colors:")
    for color_name in ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "CYAN"]:
        print(color(f"  this is {color_name}", fg=color_name))
    
    print("\nBackground Colors:")
    for bg_color in ["RED", "GREEN", "BLUE", "YELLOW"]:
        print(color(f"  this has {bg_color} background", bg=bg_color, fg="LIGHT_WHITE"))
    
    print("\nText Styles:")
    styles = ["BOLD", "ITALIC", "UNDERLINE", "CROSSED"]
    for style_name in styles:
        print(color(f"  this is {style_name}", style=style_name))
    
    print("\nHex Colors:")
    hex_samples = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1"]
    for hex_code in hex_samples:
        print(color(f"  hex color {hex_code}", fg=hex_code))
    
    print("\nCombinations:")
    print(color("  bold Red on Yellow", fg="RED", bg="YELLOW", style="BOLD"))
    print(color("  hex foreground with background", fg="#FF5733", bg="BLUE"))
    print(color("  multiple styles", style=["BOLD", "UNDERLINE"], fg="GREEN"))

enable_windows_ansi()
disable_colors_if_needed()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        print(color("wow i love color", fg="#df15c0", style="BOLD"))
        print("\nrun with --demo to see more stuff")
