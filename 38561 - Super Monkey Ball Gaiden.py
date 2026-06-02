import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.rich_presence import RichPresence
from pycheevos.models.leaderboard import Leaderboard
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path
from typing import Union

mySet = AchievementSet(game_id=38561, title="Super Monkey Ball Gaiden")
platform = "GameCube"

# Titles/Descs
world_prog = {
    0: ("So Retro",                     "Complete \"Retro Forest\" in Story Mode", 5),
    1: ("Electric Boogaloo",            "Complete \"Power Plant\" in Story Mode", 5),
    2: ("Dungeon Ball",                 "Complete \"Dungeon Hall\" in Story Mode", 10),
    3: ("Monkey Dinners",               "Complete \"Giant's Table\" in Story Mode", 10),
    4: ("Crystal Chronicles",           "Complete \"Crystal Mine\" in Story Mode", 10),
    5: ("Livin' in the City",           "Complete \"City Skyway\" in Story Mode", 10),
    6: ("Spring in Full Bloom",         "Complete \"Sakura Grove\" in Story Mode", 10),
    7: ("Golden Ratio",                 "Complete \"Golden Station\" in Story Mode", 10),
    8: ("Intergalactic",                "Complete \"Lightspeed Warp\" in Story Mode", 25),
    9: ("Side Story",                   "Complete \"Runic Realm\" in Story Mode", 25),
}

enigma = {
    1: ("Enigma I",      "Find a strange number in \"5-10 Warp Dreams\". Be sure to write it down for later!", 5),
    2: ("Enigma II",     "Find a strange number in \"7-6 Upstream\". Be sure to write it down for later!", 5),
    3: ("Enigma III",    "Find a strange number in \"8-5 Raze\". Be sure to write it down for later!", 3),
    4: ("Enigma IV",     "Find a strange number in \"10-6 Trick Room\". Be sure to write it down for later!", 5)
}

extras = {
    "bananas":   ("Can Never Have Enough",              "Collect 999 bananas in Story Mode", 10),
    "mx":        ("Through the Fire and the Flames",    "Clear World EX", 100),
    "colourful": ("Colorful Collection",                "Enter every green and red goal in one session", 25),
    "enigma":    ("No Turning Back Now!",               "Decipher the secret code and clear the Master level \"Enigma\"", 5)
}

special_clears = {
    "1-1": ("Easy Going",                     "Clear \"1-1 Ease\" with a stage score of 13,000 points or more", 3),
    "1-5": ("Hole In One",                    "Clear \"1-5 Flippers\" without pressing the switch", 10),
    "1-6": ("Skipped A Beat",                 "Clear \"1-6 Pulse\" without pressing any switches", 5),
    "1-7": ("Shifty Bananas",                 "Clear \"1-7 Slopeshift\" after collecting every banana", 3),
    "1-10": ("No Margin For Error",           "Clear \"1-10 Margin\" in 5.5 seconds or less", 5),
    "2-3": ("Equipment Failure",              "Clear \"2-3 Landing Gear\" without entering more than 1 wormhole", 5),
    "2-4": ("Optimal Bounce",                 "Clear \"2-4 Parkour\" without pressing the switch", 3),
    "2-6": ("Speed Skating",                  "Clear \"2-6 Kickflip\" in 10 seconds or less", 4),
    "2-10": ("Big Monkey",                    "Clear \"2-10 Shrink Ray\" without entering more than 3 wormholes", 5),
    "3-1": ("Cycle Of Banana",                "Clear \"3-1 Cycle Hit\" with all 4 banana bunches collected", 5),
    "3-5": ("Misalignment",                   "Clear \"3-5 Aligner\" without collecting any bananas", 5),
    "3-7": ("Extra Life",                     "Clear \"3-7 Ringfield\" with over 100 bananas collected", 5),
    "3-9": ("Victory Royale",                 "Clear \"3-9 Battle Royale\" after hitting all 4 play switches", 5),
    "4-1": ("Cutting Through",                "Clear \"4-1 Mandoline\" with a stage score of 11,000 points or more", 5),
    "4-2": ("Tightrope Tug Timing",           "Clear \"4-2 Tug\" after taking the thin path", 5),
    "4-6": ("King Of Swing",                  "Clear \"4-6 Catenary\" after collecting all bananas", 5),
    #"4-8": ("Button Bouncer",                 "On \"4-8 Turbine\", hit all 3 switches within 5 seconds of each other", 5),
    "5-3": ("Trampoline Technique",           "Clear \"5-3 Jumpplex\" in 15 seconds or less", 5),
    "5-6": ("Bring It Around Town",           "Clear \"5-6 Rotary\" with all 5 banana bunches collected", 3),
    "5-8": ("Bullseye",                       "Clear \"5-8 Range\" going over 400mph", 10),
    "5-9": ("Gonna Miss My Flight",           "Clear \"5-9 Departure\" in 30 seconds or less", 5),
    "6-3": ("Rookie Mistake",                 "Clear \"6-3 Rook\" without collecting any bananas", 10),
    "6-4": ("Rigid Ramps",                    "Clear \"6-4 Rigidify\" with both banana bunches collected", 5),
    "6-6": ("Pyramid Jumps",                  "Clear \"6-6 Pyramid Run\" in 7 seconds or less", 5),
    "6-7": ("No Assembly Required",           "Clear \"6-7 Assembly\" without pressing any switches", 5),
    "7-1": ("Leap Of Faith",                  "Clear \"7-1 Ikaruga\" collecting 1 banana at most", 5),
    "7-3": ("Rule Of Thirds",                 "Clear \"7-3 Polarity\" before the stage flips over for a 4th time", 5),
    "7-5": ("Perfect Cherry Blossom",         "Clear \"7-5 Phantasm\" with all bananas collected", 10),
    "7-8": ("High Speed Castle Siege",        "Clear \"7-8 Siege\" going over 150mph", 3),
    "8-2": ("Crossing The Streams",           "Clear \"8-2 Recoil\" with all 3 banana bunches collected", 5),
    "8-4": ("Sharp Decline",                  "Clear \"8-4 Gradient Descent\" without entering a wormhole", 4),
    "8-8": ("Potassium Pipe",                 "Clear \"8-8 Painted Pipe\" with a stage score of 6,500 points or more", 4),
    "8-9": ("I Can Imagine Anything",         "Clear all 8 different layouts of \"8-9 Visionary\" in one session", 5),
    "8-10": ("Quick Inspection",              "Clear \"8-10 Factory\" in 7 seconds or less", 5),
    "9-2": ("Delicious Duo",                  "Clear \"9-2 Twisty Triad\" with both banana bunches collected", 5),
    "9-6": ("Turbocharger",                   "Clear \"9-6 Axle\" with the fast forward switch active", 5),
    "9-7": ("Banana Of the Colossus",         "Clear \"9-7 Colossus\" with all bananas collected", 10),
    "10-7": ("Speeding Snake",                "Clear \"10-7 Ouroboros\" with the fast forward switch active", 10),
    "MX-7": ("I'll Never Swallow My Pride!",  "Clear \"MX-7 Pride\" by taking the thinner path after the switch", 25),
}

mask = value(0x1fffffff)

# Variables
level_id = dword_be(0x00473118)
world_id = byte(0x0054dbbd)
menu_progress = byte(0x0054df84)

# ingame variables
bananas_collected = dword_be(0x005bca18)
bananas_remaining = dword_be(0x553994)
wormhole_entered = (dword_be(0x0061ba90) & mask)
time = word_be(0x553974)
score = dword_be(0x005bca1c)
level_score = (dword_be(0x005be7d0) & mask) >> dword_be(0x10)
speed_pointer = (dword_be(0x005ed1c4) & mask)
goal_type_entered = byte(0x005539a8)
goal_state = 0x00553973
stage_complete_delta = (bit5(0x00553973).delta() == 0x00)
stage_complete = (bit5(0x00553973) == 0x01)
stage_failed = (bit4(0x00553973) == 0x01)
death_counter = dword_be(0x00969c80)
switch_state = bit2(0x0056e36a)
in_game = dword_be(0x5bc484)

# Modes
main_mode = (byte(0x0054df20) == 0x00)
sub_mode = byte(0x0054df27)
story_mode = (byte(0x0054df27) == 0x00)
challenge_mode = (byte(0x0054df27) == 0x01)
practice_mode = (byte(0x0054df27) == 0x02)

switch_pressed = [
    bit2(0x0056e36a).delta() == 0x00,
    bit2(0x0056e36a) == 0x01
]

x_coord = float32_be(0x005bc9a4)
y_coord = float32_be(0x005bc9a8)
z_coord = float32_be(0x005bc9ac)

def bounding(x1, x2, y1, y2, z1, z2, include_y: bool = True):
    match include_y:
        case True:
            return [
                and_next(x_coord >= x1),
                and_next(x_coord <= x2),
                and_next(y_coord >= y1),
                and_next(y_coord <= y2),
                and_next(z_coord >= z1),
                and_next(z_coord <= z2)
            ]
        case False:
            return [
                and_next(x_coord >= x1),
                and_next(x_coord <= x2),
                and_next(z_coord >= z1),
                and_next(z_coord <= z2)
            ]

LEVEL_TABLE: dict[tuple[Union[int, str], int], tuple[int, str, int]] = {
    (1,  1): (0xc9,  "1-1 Ease", 60),
    (1,  2): (0xca,  "1-2 Interceptor", 60),
    (1,  3): (0xcb,  "1-3 Cornercraft", 60),
    (1,  4): (0xcc,  "1-4 Expedition", 60),
    (1,  5): (0x01,  "1-5 Flippers", 60),
    (1,  6): (0x02,  "1-6 Pulse", 60),
    (1,  7): (0x03,  "1-7 Slopeshift", 60),
    (1,  8): (0x04,  "1-8 Safety Pipe", 60),
    (1,  9): (0x05,  "1-9 Stair Valley", 60),
    (1, 10): (0x06,  "1-10 Margin", 60),
    (2,  1): (0x07,  "2-1 Hidden Hills", 60),
    (2,  2): (0x08,  "2-2 Emergency Brake", 60),
    (2,  3): (0x09,  "2-3 Landing Gear", 60),
    (2,  4): (0x0a,  "2-4 Parkour", 60),
    (2,  5): (0x0b,  "2-5 Whisk", 60),
    (2,  6): (0x0c,  "2-6 Kickflip", 60),
    (2,  7): (0x0d,  "2-7 Multi Spring", 60),
    (2,  8): (0x0e,  "2-8 Cubbyholes", 30),
    (2,  9): (0x67,  "2-9 Unwind", 60),
    (2, 10): (0x10,  "2-10 Shrink Ray", 90),
    (3,  1): (0xe7,  "3-1 Cycle Hit", 90),
    (3,  2): (0xe8,  "3-2 Boost Bridges", 60),
    (3,  3): (0xe9,  "3-3 Suspension", 60),
    (3,  4): (0xea,  "3-4 Quaketray", 60),
    (3,  5): (0xeb,  "3-5 Aligner", 60),
    (3,  6): (0xec,  "3-6 Master of None", 90),
    (3,  7): (0xed,  "3-7 Ringfield", 120),
    (3,  8): (0xee,  "3-8 Trinity", 60),
    (3,  9): (0xef,  "3-9 Battle Royale", 180),
    (3, 10): (0x11,  "3-10 Actual Guillotine", 60),
    (4,  1): (0x12,  "4-1 Mandoline", 60),
    (4,  2): (0x13,  "4-2 Tug", 60),
    (4,  3): (0x14,  "4-3 Whirlers", 60),
    (4,  4): (0x15,  "4-4 Diaphragm", 60),
    (4,  5): (0x16,  "4-5 Roundabout", 60),
    (4,  6): (0x17,  "4-6 Catenary", 60),
    (4,  7): (0x18,  "4-7 Pattern Prism", 60),
    (4,  8): (0x19,  "4-8 Turbine", 120),
    (4,  9): (0x1a,  "4-9 Piercers", 60),
    (4, 10): (0x1b,  "4-10 Emitter", 60),
    (5,  1): (0x1c,  "5-1 Dragonfly", 60),
    (5,  2): (0x1d,  "5-2 Sway", 60),
    (5,  3): (0x1e,  "5-3 Jumpplex", 60),
    (5,  4): (0x1f,  "5-4 Drop of Doom", 90),
    (5,  5): (0x20,  "5-5 Perimeter", 60),
    (5,  6): (0x21,  "5-6 Rotary", 60),
    (5,  7): (0x22,  "5-7 Snakeskin", 60),
    (5,  8): (0x23,  "5-8 Range", 60),
    (5,  9): (0x24,  "5-9 Departure", 60),
    (5, 10): (0x25,  "5-10 Warp Dreams", 180),
    (6,  1): (0x26,  "6-1 Tripwire", 60),
    (6,  2): (0x27,  "6-2 Equilibrium", 60),
    (6,  3): (0x28,  "6-3 Rook", 60),
    (6,  4): (0x29,  "6-4 Rigidify", 60),
    (6,  5): (0x2a,  "6-5 Binary Launchers", 30),
    (6,  6): (0x2b,  "6-6 Pyramid Run", 60),
    (6,  7): (0x2c,  "6-7 Assembly", 90),
    (6,  8): (0x2d,  "6-8 Circus", 60),
    (6,  9): (0x2e,  "6-9 Seismic", 90),
    (6, 10): (0x2f,  "6-10 Slot Machine", 60),
    (7,  1): (0x119, "7-1 Ikaruga", 60),
    (7,  2): (0x11a, "7-2 Focus Breaker", 60),
    (7,  3): (0x11b, "7-3 Polarity", 60),
    (7,  4): (0x11c, "7-4 Carpets", 30),
    (7,  5): (0x11d, "7-5 Phantasm", 120),
    (7,  6): (0x11e, "7-6 Upstream", 60),
    (7,  7): (0x11f, "7-7 Rebuild", 60),
    (7,  8): (0x120, "7-8 Seige", 60),
    (7,  9): (0x121, "7-9 Albatross", 90),
    (7, 10): (0x30,  "7-10 Gaokao", 120),
    (8,  1): (0x31,  "8-1 Lock On", 60),
    (8,  2): (0x32,  "8-2 Recoil", 60),
    (8,  3): (0x33,  "8-3 Derelict", 120),
    (8,  4): (0x34,  "8-4 Gradient Descent", 60),
    (8,  5): (0x35,  "8-5 Raze", 90),
    (8,  6): (0x36,  "8-6 Gyroscope", 60),
    (8,  7): (0x37,  "8-7 Revision", 120),
    (8,  8): (0x38,  "8-8 Painted Pipe", 30),
    (8,  9): (0x39,  "8-9 Visionary", 60),
    (8, 10): (0x3a,  "8-10 Factory", 60),
    (9,  1): (0x3b,  "9-1 Demolition", 60),
    (9,  2): (0x3c,  "9-2 Twisty Triad", 60),
    (9,  3): (0x3d,  "9-3 Spinways", 60),
    (9,  4): (0x3e,  "9-4 Strum", 60),
    (9,  5): (0x3f,  "9-5 Antagonizer", 120),
    (9,  6): (0x40,  "9-6 Axle", 60),
    (9,  7): (0x41,  "9-7 Colossus", 180),
    (9,  8): (0x42,  "9-8 Fallout Zone", 60),
    (9,  9): (0x43,  "9-9 Lightspeed", 60),
    (9, 10): (0x44,  "9-10 Apparatus", 300),
    (10,  1): (0x155, "10-1 Exodus", 120),
    (10,  2): (0x156, "10-2 Pandora's Box", 180),
    (10,  3): (0x157, "10-3 Genesis", 60),
    (10,  4): (0x158, "10-4 Ausdauer", 120),
    (10,  5): (0x159, "10-5 Intermezzo", 60),
    (10,  6): (0x15a, "10-6 Trick Room", 300),
    (10,  7): (0x15b, "10-7 Ouroboros", 60),
    (10,  8): (0x15c, "10-8 Red Sea", 120),
    (10,  9): (0x15d, "10-9 Shadow Tag", 60),
    (10, 10): (0x15e, "10-10 Curtain Call", 240),
    ("M", 1):   (0x141, "M-1 Enigma", 180),
    ("MX", 1):  (0xD3, "MX-1 Master of All", 120),
    ("MX", 2):  (0xD4, "MX-2 Maelstrom", 60),
    ("MX", 3):  (0xD5, "MX-3 Tartarus", 180),
    ("MX", 4):  (0xD6, "MX-4 Sisyphus", 180),
    ("MX", 5):  (0xD7, "MX-5 Acheron", 180),
    ("MX", 6):  (0xD8, "MX-6 Styx", 240),
    ("MX", 7):  (0xD9, "MX-7 Pride", 180),
    ("MX", 8):  (0xDA, "MX-8 Babel", 240),
    ("MX", 9):  (0xDB, "MX-9 Gauntlet", 180),
    ("MX", 10): (0xDC, "MX-10 The Grand Finale", 300)
}
 
def story_level(world: int | str, level: int) -> tuple[int, str, int]:
    if (world, level) not in LEVEL_TABLE:
        raise ValueError(f"No entry for World {world}-{level}")
    return LEVEL_TABLE[(world, level)]

def mode_check(mode):
    logic = []
    logic.append(main_mode)
    match mode:
        case "story":
            logic.append(story_mode)
        case "challenge":
            logic.append(challenge_mode)
        case "practice":
            logic.append(practice_mode)
        case "non-challenge":
            logic.append(or_next(story_mode))
            logic.append(practice_mode)
        case "non-story":
            logic.append(or_next(challenge_mode))
            logic.append(practice_mode)
    return logic

def level_check(world: int, level: int):
    hex_code, _, _ = story_level(world, level)
    return level_id == hex_code

def reset_level_check(world: int, level: int):
    hex_code, _, _ = story_level(world, level)
    return reset_if(level_id != hex_code)

def over_speed(mode, world, level, required_speed):
    logic = [
        *mode_check(mode),
        level_check(world, level),
        add_source(speed_pointer >> (low4(0x720) * 100)), # hundreds
        add_source(speed_pointer >> (low4(0x721) * 10)),  # tens
        speed_pointer >> low4(0x721) >= value(required_speed), # ones = goal
        trigger(stage_complete_delta),
        trigger(stage_complete),
        time != 0x00
    ]

    return logic

def under_speed(mode, world, level, required_speed):
    logic = [
        *mode_check(mode),
        level_check(world, level),
        add_source(speed_pointer >> (low4(0x720) * 100)), # hundreds
        add_source(speed_pointer >> (low4(0x721) * 10)),  # tens
        speed_pointer >> low4(0x721) <= value(required_speed), # ones = goal
        trigger(stage_complete_delta),
        trigger(stage_complete),
        time != 0x00
    ]

    return logic

def all_bananas_collected(mode, world, level):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (bananas_remaining != 0).with_hits(1),
        trigger(bananas_remaining == 0),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ]
    return logic

def banana_bunches_collected(mode, world, level, total_collected):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        add_source(value(1000)),
        trigger((score.delta() == score).with_hits(total_collected)),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ]
    return logic

def minimum_bananas_collected(mode, world, level, required_bananas):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level)
    ]
    for x in range(0, 9):
        logic.append(sub_source(bananas_collected.delta()))
        logic.append(add_hits(bananas_collected == value(0x0a)))
    
    logic.extend([
        measured(bananas_collected > bananas_collected.delta()).with_hits(required_bananas),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ])

    return logic

def maximum_bananas_collected(mode, world, level, starting_time, max_bananas):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1)
    ]

    for x in range(0, 9):
        logic.append(sub_source(bananas_collected.delta()))
        logic.append(add_hits(bananas_collected == value(0x0a)))
    
    logic.extend([
        reset_if(bananas_collected > bananas_collected.delta()).with_hits(max_bananas + 1),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ])

    return logic

def score_clear(mode, world, level, score_required):
    logic = [
        *mode_check(mode),
        level_check(world, level),
        and_next(level_score != 0xffffffff),
        trigger(level_score >= score_required),
        trigger(bit4(goal_state.delta() == 0x00)),
        trigger(bit4(goal_state) == 0x01),
        trigger(stage_complete),
        time != 0x00
    ]
    return logic

def switchless(mode, world, level, starting_time = 60):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        and_next(bit2(0x0056e36a).delta() == 0x00),
        reset_if(bit2(0x0056e36a) == 0x01),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(time == 0x00)
    ]

    return logic

def all_switches(mode, world, level, boxes, starting_time):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1)
    ]

    for box in boxes:
        logic.extend(box)
        logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
        logic.append((bit2(0x0056e36a) == 0x01).with_hits(1))

    logic.append(trigger(stage_complete_delta))
    logic.append(trigger(stage_complete))
    logic.append(reset_if(stage_failed))
    logic.append(reset_if(time == 0x00))

    return logic

def timed(mode, world, level, starting_time, within_time):
    if starting_time == int:
        float(starting_time)
    if within_time == int:
        float(within_time)

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        reset_if(time == ((starting_time - within_time) * 60)),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(time == 0)
    ]

    return logic

def wormhole_limit_clear(mode, world, level, starting_time, max_wormhole_entries):
    if max_wormhole_entries != 0:
        max_wormhole_entries += 1
    print(wormhole_entered)
    print(wormhole_entered >> dword_be(0xd8).delta())
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        add_address(wormhole_entered),
        reset_if(dword_be(0xd8) > dword_be(0xd8).delta()).with_hits(max_wormhole_entries),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ]

    return logic

def bananaless(mode, world, level, starting_time):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (time == starting_time * 60).with_hits(1),
        reset_if(bananas_collected > bananas_collected.delta()),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(time == 0x00)
    ]

    return logic

def special_path(mode, world, level, starting_time, start_reset, start_checkpoint, end_checkpoint):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        *start_reset,
        reset_next_if(value(0x00) == value(0x00)),
        *start_checkpoint,
        (value(0x00) == value(0x00)).with_hits(1),
        *end_checkpoint,
        trigger(value(0x00) == value(0x00)).with_hits(1),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ]
    return logic

def switches_within_time(mode, world, level, starting_time, time_between_switches, total_switches):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        reset_next_if(switch_state != switch_state.delta()),
        and_next
        
        
        ]

    for x in range(0, total_switches):
        logic.extend([
            and_next(switch_state.delta() == 0x00).with_hits(x + 1),
            reset_next_if(switch_state == 0x01).with_hits(x + 1),
            reset_if(switch_state == 0x00).with_hits(time_between_switches * 60),
        ])

    logic.extend([
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_failed),
        reset_if(time == 0x00)
    ])

    return logic

def visionary(mode, world, level, starting_time):
    logic = [
        *mode_check(mode),
        level_check(world, level),
    ]

    lll = bounding(
        -2.0, 2.0,
        -5.0, -4.0,
        -183.0, -179.0
    )

    llr = bounding(
        -30.0, -26.0,
        -6.5, -5.5,
        -95.0, -92.0
    )

    lrr = bounding(
        0.0, 4.0,
        -3.0, -2.0,
        -68.0, -63.0
    )

    rrr = bounding(
        -4.0, 0.0,
        -2.5, -1.5,
        -65.0, -62.0
    )

    rrl = bounding(
        -2.0, 2.0,
        -1.0, 0.0,
        -115.0, -112.0
    )

    rll = bounding(
        -2.0, 2.0,
        -1.0, 0.0,
        -160.0, -156.0
    )

    lrl = bounding(
        -20.0, -16.0,
        -6.0, -5.0,
        -88.0, -85.0
    )

    rlr = bounding(
        -2.0, 2.0,
        -8.5, -7.5,
        -126.0, -124.0
    )

    boxes = [
        lll, llr, lrr, rrr, rrl, rll, lrl, rlr
    ]

    for box in boxes:
        logic.extend(box)
        logic.append(and_next(stage_complete_delta))
        logic.append(trigger(stage_complete).with_hits(1))

    return logic

enigma_switch_locations = {
    1: (story_level(5, 10)[0], bounding(34.0, 38.7, 
                                        40.0, 41.0, 
                                        -1.5, 1.5)),
    2: (story_level(7, 6)[0], bounding(-16.35, -13.5,
                                       3.0, 4.0, 
                                       -91.40, -88.5,)),
    3: (story_level(8, 5)[0], bounding(100.4, 103.25, 
                                       1.0, 2.0, 
                                       -1.4, 1.4)),
    4: (story_level(10, 6)[0], bounding(-60.0, -54.0, 
                                        5.0, 6.0, 
                                        -16.2, -8.5)),
}

for switch in enigma_switch_locations:
    ach = Achievement(enigma[switch][0], enigma[switch][1], enigma[switch][2])
    logic = [
        main_mode,
        story_mode,
        level_id == enigma_switch_locations[switch][0],
        enigma_switch_locations[switch][1],
    ]
    match switch:
        case 4:
            logic.append(bananas_collected != bananas_collected.delta())
        case _:
            logic.append(switch_pressed)
    ach.add_core(logic)
    #mySet.add_achievement(ach)

# Switch test
buttonAch = Achievement("Button Activated", "Button has been pressed", 0)
buttonAch.add_core(switch_pressed)
mySet.add_achievement(buttonAch)

for world, (title, description, points) in world_prog.items():
    ach = Achievement(title, description, points)
    logic = [
        menu_progress != 0xff,
        main_mode,
        story_mode,
    ]
    match world:
        case 9:
            logic.append(level_id.delta() != 0xc5)
            logic.append(level_id == 0xc5)
        case _:
            logic.append(world_id.delta() == world)
            logic.append(world_id == world + 1)
    ach.add_core(logic)
    #mySet.add_achievement(ach)

def clear_level_type(world: int, level: int, goal_type: str):
    hex_code, _, _ = story_level(world, level)
    hex_goal = 0x00
    match goal_type:
        case "blue":
            hex_goal = 0x00
        case "green":
            hex_goal = 0x01
        case "red":
            hex_goal = 0x02
    return [
        and_next(level_id == hex_code),
        and_next(stage_complete_delta),
        and_next(stage_complete),
        add_hits(goal_type_entered == hex_goal).with_hits(1)
    ]

for x in extras:
    ach = Achievement(extras[x][0], extras[x][1], extras[x][2])
    match x:
        case "bananas":
            logic = [
                *mode_check("story"),
                bananas_collected.delta() < 999,
                bananas_collected >= 999
            ]
        case "mx":
            logic = [
                *mode_check("challenge"),
                level_check("MX", 10),
                time != 360 * 60,
                stage_complete_delta,
                stage_complete,
            ]
        case "colourful":
            logic = [
                *mode_check("non-challenge"),
                clear_level_type(1, 3, "green"),
                clear_level_type(1, 6, "red"),
                clear_level_type(3, 10, "red"),
                clear_level_type(5, 2, "green"),
                clear_level_type(5, 2, "red"),
                clear_level_type(5, 5, "red"),
                clear_level_type(5, 8, "green"),
                clear_level_type(5, 8, "red"),
                clear_level_type(9, 3, "green"),
                measured(value(0x00) == value(0x01)).with_hits(9)
            ]    
        case "enigma":
            logic = [
                *mode_check("non-story"),
                level_check("M", 1),
                stage_complete_delta,
                stage_complete,
            ]
    ach.add_core(logic)
    mySet.add_achievement(ach)

for x in special_clears:
    ach = Achievement(special_clears[x][0], special_clears[x][1], special_clears[x][2])
    match x:
        case "1-1": # "Clear "1-1 Ease" with a stage score of 13,000 points or more
            logic = score_clear("non-challenge", 1, 1, 13000)
        case "1-5": # "Clear "1-5 Flippers" without pressing the switch
            #boxes = [bounding(
            #    -62.0, -59.0,
            #    2.0, 3.0,
            #    -1.5, 1.5
            #)] 
            logic = switchless("non-challenge", 1, 5, 60)
        case "1-6": # "Clear "1-6 Pulse" without pressing any switches
            #boxes = [bounding( ## middle
            #    -2.0, 2.0,
            #    0.0, 0.0,
            #    -2.0, 2.0,
            #False), 
            #bounding( ## top
            #    -24.0, -20.0,
            #    0.0, 0.0,
            #    -2.0, 2.0,
            #False),
            #bounding( ## right
            #    -2.0, 2.0,
            #    0.0, 0.0,
            #    -20.0, -16.0,
            #False),
            #bounding( ## left
            #    -2.0, 2.0,
            #    0.0, 0.0,
            #    16.0, 20.0,
            #False)]
            logic = switchless("non-challenge", 1, 6, 60)
        case "1-7": # "Clear "1-7 Slopeshift" after collecting every banana
            logic = all_bananas_collected("non-challenge", 1, 7)
        case "1-10": # "Clear "1-10 Margin" in 5.5 seconds or less
            logic = timed("non-challenge", 1, 10, 60.0, 5.5)
        case "2-3": # "Clear "2-3 Landing Gear" without entering more than 1 wormhole
            logic = wormhole_limit_clear("non-challenge", 2, 3, 60, 1)
        case "2-4": # "Clear "2-4 Parkour" without pressing the switch
            #boxes = [bounding(
            #    -0.5, 3,
            #    14.0, 15.0,
            #    2.5, 6
            #)]
            logic = switchless("non-challenge", 2, 4, 60)
        case "2-6": # "Clear "2-6 Kickflip" in 10 seconds or less
            logic = timed("non-challenge", 2, 6, 60, 10)
        case "2-10": # "Clear "2-10 Shrink Ray" without entering more than 3 wormholes
            logic = wormhole_limit_clear("non-challenge", 2, 10, 90, 3)
        case "3-1": # "Clear "3-1 Cycle Hit" with all 4 banana bunches collected
           logic = banana_bunches_collected("non-challenge", 3, 1, 4)
        case "3-5": # "Clear "3-5 Aligner" without collecting any bananas
            logic = bananaless("non-challenge", 3, 5, 60)
        case "3-7": # "Clear "3-7 Ringfield" with over 100 bananas collected
            logic = minimum_bananas_collected("non-challenge", 3, 7, 100)
        case "3-9": # "Clear "3-9 Battle Royale" after hitting all 4 play switches
           #boxes = [bounding( # bottom left
           #    62.0, 66.0,
           #    1.0, 2.0,
           #    -66.0, -62.0
           #),
           #bounding( # top left
           #    62.0, 66.0,
           #    1.0, 2.0,
           #    30.0, 34.0
           #),
           #bounding( # top right
           #   -66.0, -62.0,
           #    1.0, 2.0,
           #    62.0, 66.0
           #),
           #bounding( # bottom right
           #    -66.0, -62.0,
           #    1.0, 2.0,
           #    -34.0, -30.0
           #),
           #]
            logic = all_switches("non-challenge", 3, 9, boxes, 180)
        case "4-1": # "Clear "4-1 Mandoline" with a stage score of 11,000 points or more
            logic = score_clear("non-challenge", 4, 1, 11000)
        case "4-2": # "Clear "4-2 Tug" after taking the thin path
            logic = special_path("non-story", 4, 2, 60,
                                 bounding(
                                     -14.0, -11.0,
                                     9.0, 10.0,
                                     -21.0, -16.0
                                 ),
                                 bounding(
                                     -15.0, -14.0,
                                     9.0, 11.0,
                                     -20.0, -18.0
                                 ),
                                 bounding(
                                     -25.0, -23.0,
                                     0.0, 0.0,
                                     5.0, 6.0,
                                 False)
                                 )
        case "4-6": # "Clear "4-6 Catenary" after collecting all bananas
            logic = all_bananas_collected("non-challenge", 4, 6)
        case "4-8": # "On "4-8 Turbine", hit all 3 switches within 5 seconds of each other
            continue # broken, need more help with the resetting and permittance once the thing is done
            #logic = switches_within_time("non-challenge", 4, 8, 120, 5, 3)
        case "5-3": # "Clear "5-3 Jumpplex" in 15 seconds or less
            logic = timed("non-challenge", 5, 3, 60, 15)
        case "5-6": # "Clear "5-6 Rotary" with all 5 banana bunches collected
            logic = banana_bunches_collected("non-challenge", 5, 6, 5)
        case "5-8": # "Clear "5-8 Range" going over 400mph
            logic = over_speed("non-challenge", 5, 8, 400)
        case "5-9": # "Clear "5-9 Departure" in 30 seconds or less
            logic = timed("non-practice", 5, 9, 60, 30)
        case "6-3": # "Clear "6-3 Rook" without collecting any bananas
            logic = bananaless("non-practice", 6, 3, 60)
        case "6-4": # "Clear "6-4 Rigidify" with both banana bunches collected
            logic = banana_bunches_collected("non-practice", 6, 4, 2)
        case "6-6": # "Clear "6-6 Pyramid Run" in 7 seconds or less
            logic = timed("non-practice", 6, 6, 60, 7)
        case "6-7": # "Clear "6-7 Assembly" without pressing any switches
            logic = switchless("non-practice", 6, 7, 90)
        case "7-1": # "Clear "7-1 Ikaruga" collecting 1 banana at most
            logic = maximum_bananas_collected("non-challenge", 7, 1, 60, 1)
        case "7-3": # "Clear "7-3 Polarity" before the stage flips over for a 4th time
            logic = timed("non-challenge", 7, 3, 60, 20)
        case "7-5": # "Clear "7-5 Phantasm" with all bananas collected
            logic = all_bananas_collected("non-challenge", 7, 5)
        case "7-8": # "Clear "7-8 Siege" going over 150mph
            logic = over_speed("non-challenge", 7, 8, 150)
        case "8-2": # "Clear "8-2 Recoil" with all 3 banana bunches collected
            logic = banana_bunches_collected("non-challenge", 8, 2, 3)
        case "8-4": # "Clear "8-4 Gradient Descent" without entering a wormhole
            logic = wormhole_limit_clear("non-challenge", 8, 4, 60, 0) # test this
        case "8-8": # "Clear "8-8 Painted Pipe" with a stage score of 6,500 points or more
            logic = score_clear("non-challenge", 8, 8, 6500)
        case "8-9": # "Clear all 8 different layouts of "8-9 Visionary" in one session
            logic = visionary("non-challenge", 8, 9, 60)
        case "8-10": # "Clear "8-10 Factory" in 7 seconds or less
            logic = timed("non-challenge", 8, 10, 60, 7)
        case "9-2": # "Clear "9-2 Twisty Triad" with both banana bunches collected
            logic = banana_bunches_collected("non-challenge", 9, 2, 2)
        case "9-6": # "Clear "9-6 Axle" with the fast forward switch active
            boxes = [bounding(
                16.0, 20.0,
                3.0, 4.0,
                25.0, 29.0
            )]
            logic = all_switches("non-challenge", 9, 6, boxes, 60)
        case "9-7": # "Clear "9-7 Colossus" with all bananas collected  
            logic = all_bananas_collected("non-challenge", 9, 7)
        case "10-7": # "Clear "10-7 Ouroboros" with the fast forward switch active
            boxes = [bounding(
                0.0, 3.0,
                0.0, 1.0,
                -16.0, -13.0
            )]
            logic = all_switches("non-challenge", 10, 7, boxes, 60)
        case "MX-7": # "Clear "MX-7 Pride" by taking the thinner path after the switch
            logic = special_path("non-challenge", "MX", 7, 180,
                                 bounding(
                                     39.0, 45.0,
                                     5.0, 6.0,
                                     -59.0, -53.0
                                 ),
                                 bounding(
                                     43.0, 45.0,
                                     5.0, 6.0,
                                     -61.0, -59.5
                                 ),
                                 bounding(
                                     43.0, 45.0,
                                     5.0, 6.0,
                                     -98.0, -96.0
                                 ))
        case _:
            continue
    ach.add_core(logic)
    mySet.add_achievement(ach)

# Leaderboards

lb = Leaderboard(f"Master Extra - Death Counter", "Complete MX with as few deaths as possible!")
lb.format = LeaderboardFormat.SCORE
lb.lower_is_better = True
lb.set_start([
    *mode_check("non-story"),
    level_check("MX",  10),
    stage_complete_delta,
    stage_complete,
    time != 0x00
])
lb.set_cancel([
    value(0x00) == value(0x01)
])
lb.set_submit([
    value(0x00) == value(0x00)
])
lb.set_value([
    measured(death_counter)
])
mySet.add_leaderboard(lb)

# Times
for (world, level), (hex_code, title, starting_time) in LEVEL_TABLE.items():
    match (world, level):
        case ("M", 1):
            pass # no need for enigma boards
        case ("MX", _):
            lb = Leaderboard(f"{title} - Fastest Time", "Clear this as fast as possible!")
            lb.format = LeaderboardFormat.FRAMES
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-story"),
                level_check(world, level),
                (time != starting_time * 60),
                stage_complete_delta,
                stage_complete,
                time != 0x00
            ])
            lb.set_cancel([
                value(0x00) == value(0x01)
            ])
            lb.set_submit([
                value(0x00) == value(0x00)
            ])
            lb.set_value([
                measured(time)
            ])
            mySet.add_leaderboard(lb)

        case _:
            lb = Leaderboard(f"{title} - Fastest Time", "Clear this as fast as possible!")
            lb.format = LeaderboardFormat.FRAMES
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-challenge"),
                level_check(world, level),
                (time != starting_time * 60),
                stage_complete_delta,
                stage_complete,
                time != 0x00
            ])

            lb.set_cancel([
                value(0x00) == value(0x01)
            ])

            lb.set_submit([
                value(0x00) == value(0x00)
            ])

            lb.set_value([
                measured(time)
            ])

            mySet.add_leaderboard(lb)

            lb = Leaderboard(f"{title} - Highest Score", "Set the highest score!")
            lb.format = LeaderboardFormat.SCORE
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-challenge"),
                level_check(world, level),
                (time != starting_time * 60),
                stage_complete,
                bit4(goal_state).delta() == 0x00,
                bit4(goal_state) == 0x01,
                time != 0x00
            ])

            lb.set_cancel([
                value(0x00) == value(0x01)
            ])

            lb.set_submit([
                value(0x00) == value(0x00)
            ])

            lb.set_value([
                measured(level_score)
            ])

            mySet.add_leaderboard(lb)


rp = RichPresence()
rp.add_lookup("Level", {
    0xc9: "1-1 Ease",
    0xca: "1-2 Interceptor",
    0xcb: "1-3 Cornercraft",
    0xcc: "1-4 Expedition",
    0x01: "1-5 Flippers",
    0x02: "1-6 Pulse",
    0x03: "1-7 Slopeshift",
    0x04: "1-8 Safety Pipe",
    0x05: "1-9 Stair Valley",
    0x06: "1-10 Margin",
    0x07: "2-1 Hidden Hills",
    0x08: "2-2 Emergency Brake",
    0x09: "2-3 Landing Gear",
    0x0a: "2-4 Parkour",
    0x0b: "2-5 Whisk",
    0x0c: "2-6 Kickflip",
    0x0d: "2-7 Multi Spring",
    0x0e: "2-8 Cubbyholes",
    0x67: "2-9 Unwind",
    0x10: "2-10 Shrink Ray",
    0xe7: "3-1 Cycle Hit",
    0xe8: "3-2 Boost Bridges",
    0xe9: "3-3 Suspension",
    0xea: "3-4 Quaketray",
    0xeb: "3-5 Aligner",
    0xec: "3-6 Master of None",
    0xed: "3-7 Ringfield",
    0xee: "3-8 Trinity",
    0xef: "3-9 Battle Royale",
    0x11: "3-10 Actual Guillotine",
    0x12: "4-1 Mandoline",
    0x13: "4-2 Tug",
    0x14: "4-3 Whirlers",
    0x15: "4-4 Diaphragm",
    0x16: "4-5 Roundabout",
    0x17: "4-6 Catenary",
    0x18: "4-7 Pattern Prism",
    0x19: "4-8 Turbine",
    0x1a: "4-9 Piercers",
    0x1b: "4-10 Emitter",
    0x1c: "5-1 Dragonfly",
    0x1d: "5-2 Sway",
    0x1e: "5-3 Jumpplex",
    0x1f: "5-4 Drop of Doom",
    0x20: "5-5 Perimeter",
    0x21: "5-6 Rotary",
    0x22: "5-7 Snakeskin",
    0x23: "5-8 Range",
    0x24: "5-9 Departure",
    0x25: "5-10 Warp Dreams",
    0x26: "6-1 Tripwire",
    0x27: "6-2 Equilibrium",
    0x28: "6-3 Rook",
    0x29: "6-4 Rigidify",
    0x2a: "6-5 Binary Launchers",
    0x2b: "6-6 Pyramid Run",
    0x2c: "6-7 Assembly",
    0x2d: "6-8 Circus",
    0x2e: "6-9 Seismic",
    0x2f: "6-10 Slot Machine",
    0x119: "7-1 Ikaruga",
    0x11a: "7-2 Focus Breaker",
    0x11b: "7-3 Polarity",
    0x11c: "7-4 Carpets",
    0x11d: "7-5 Phantasm",
    0x11e: "7-6 Upstream",
    0x11f: "7-7 Rebuild",
    0x120: "7-8 Seige",
    0x121: "7-9 Albatross",
    0x30: "7-10 Gaokao",
    0x31: "8-1 Lock On",
    0x32: "8-2 Recoil",
    0x33: "8-3 Derelict",
    0x34: "8-4 Gradient Descent",
    0x35: "8-5 Raze",
    0x36: "8-6 Gyroscope",
    0x37: "8-7 Revision",
    0x38: "8-8 Painted Pipe",
    0x39: "8-9 Visionary",
    0x3a: "8-10 Factory",
    0x3b: "9-1 Demolition",
    0x3c: "9-2 Twisty Triad",
    0x3d: "9-3 Spinways",
    0x3e: "9-4 Strum",
    0x3f: "9-5 Antagonizer",
    0x40: "9-6 Axle",
    0x41: "9-7 Colossus",
    0x42: "9-8 Fallout Zone",
    0x43: "9-9 Lightspeed",
    0x44: "9-10 Apparatus",
    0x155: "10-1 Exodus",
    0x156: "10-2 Pandora's Box",
    0x157: "10-3 Genesis",
    0x158: "10-4 Ausdauer",
    0x159: "10-5 Intermezzo",
    0x15a: "10-6 Trick Room",
    0x15b: "10-7 Ouroboros",
    0x15c: "10-8 Red Sea",
    0x15d: "10-9 Shadow Tag",
    0x15e: "10-10 Curtain Call",
    0x141: "M-1 Enigma",
    0xD3: "MX-1 Master of All",
    0xD4: "MX-2 Maelstrom",
    0xD5: "MX-3 Tartarus",
    0xD6: "MX-4 Sisyphus",
    0xD7: "MX-5 Acheron",
    0xD8: "MX-6 Styx",
    0xD9: "MX-7 Pride",
    0xDA: "MX-8 Babel",
    0xDB: "MX-9 Gauntlet",
    0xDC: "MX-10 The Grand Finale",
    0xc9: "Staff Roll"
})

rp.add_lookup("Mode", {
    0x00: "Story Mode",
    0x01: "Challenge Mode",
    0x02: "Practice Mode",
})

rp.add_format("Value", "VALUE")

rp.add_display(
    [in_game == 0x00],
    "Pondering ones ball on what to do..."
)

rp.add_display(
    [level_id == 0xDC],
    f"Finalizing their final finale in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(
    [level_id == 0xD6],
    f"Pushing a ball up hill in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(
    [level_id == 0x39],
    f"Envisioning levels like a visionary would in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(
    [level_id == 0x141],
    f"Trying to crack the code in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(
    [level_id == 0xc9, world_id == 0x09],
    f"Celebrating the staff in the {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(
    [level_id != 0xffffffff, level_id != 0xc9],
    f"Rolling around in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)}"
)

rp.add_display(None,
    "Monkeying around ..."
)
mySet.add_rich_presence(rp)

dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")
    
match platform:
    case "Wii" | "GameCube":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case default:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()
 