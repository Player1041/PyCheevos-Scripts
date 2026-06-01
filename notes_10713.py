# Code Notes for Game ID 10713
# Source: Smart Importer Sync

from pycheevos.core.helpers import *

# 0x014c: [8-bit] Main Menu
main_menu = byte(0x014c)
#0x00 - Menu
#0x01 - In game

# 0x0181: [8-bit] Used to check board loading
used_to_check_board_loading = byte(0x0181)
#0x01 - Loading into board

# 0x0182: [Array of 400 Bytes] Grid Bounds
grid_bounds = byte(0x0182)
#[0x000182 -> 0x0001c9] Small Grid Bounds [72 Bytes]
#[0x000182 -> 0x000245] Medium Grid Bounds [196 Bytes]
#[0x000182 -> 0x000311] Large Grid Bounds [400 Bytes]
#bit4 - Flagged
#bit5 - Question Mark
#bit4 and bit5 set - Revealed
#bit7 - Blank

# 0x031d: [16-bit BCD] Tile Counter
tile_counter = word(0x031d)

# 0x031f: [8-bit Bitflags] Input
input = byte(0x031f)
#bit0 - Up
#bit1 - Down
#bit2 - Left
#bit3 - Right
#bit4 - Button 1 - Reveal
#bit5 - Button 2 - Flag/Question
#bit6 -
#bit7 -

# 0x032c: [8-bit] Win condition
win_condition = byte(0x032c)
#0x0d - Win
#0x09 - Loss
