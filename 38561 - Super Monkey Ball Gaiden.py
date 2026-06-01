import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

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
    4: ("Enigma IV",     "Find a strange number in \"10-6 Trick Room\". Be sure to write it down for later!", 5),
    5: ("No Turning Back Now!",       "Decipher the secret code and clear the Master level \"Enigma\"", 5),
}

extras = {
    "bananas":   ("Can Never Have Enough",              "Collect 999 bananas in Story Mode", 10),
    "mx":        ("Through the Fire and the Flames",    "Clear Master Extra", 100),
    "colourful": ("Colorful Collection",                "Enter every green and red goal in one session", 25)
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
    "4-8": ("Button Bouncer",                 "On \"4-8 Turbine\", hit all 3 switches within 5 seconds of each other", 5),
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
goal_state = byte(0x00553973)
stage_complete_delta = (bit5(0x00553973).delta() == 0x00)
stage_complete = (bit5(0x00553973) == 0x01)
stage_failed = (bit4(0x00553973) == 0x01)

switch_speed = (dword_be(0x005bd97c) & mask) >> byte(0xa3)
#0x00 - Normal
#0x01 - Paused
#0x02 - Reverse
#0x03 - 2x Faster
#0x04 - 2x Reverse

# Modes
main_mode = (byte(0x0054df20) == 0x00)
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



LEVEL_TABLE = {
    (1,  1): (0xc9,  "1-1 Ease"),
    (1,  2): (0xca,  "1-2 Interceptor"),
    (1,  3): (0xcb,  "1-3 Cornercraft"),
    (1,  4): (0xcc,  "1-4 Expedition"),
    (1,  5): (0x01,  "1-5 Flippers"),
    (1,  6): (0x02,  "1-6 Pulse"),
    (1,  7): (0x03,  "1-7 Slopeshift"),
    (1,  8): (0x04,  "1-8 Safety Pipe"),
    (1,  9): (0x05,  "1-9 Stair Valley"),
    (1, 10): (0x06,  "1-10 Margin"),
    (2,  1): (0x07,  "2-1 Hidden Hills"),
    (2,  2): (0x08,  "2-2 Emergency Brake"),
    (2,  3): (0x09,  "2-3 Landing Gear"),
    (2,  4): (0x0a,  "2-4 Parkour"),
    (2,  5): (0x0b,  "2-5 Whisk"),
    (2,  6): (0x0c,  "2-6 Kickflip"),
    (2,  7): (0x0d,  "2-7 Multi Spring"),
    (2,  8): (0x0e,  "2-8 Cubbyholes"),
    (2,  9): (0x67,  "2-9 Unwind"),
    (2, 10): (0x10,  "2-10 Shrink Ray"),
    (3,  1): (0xe7,  "3-1 Cycle Hit"),
    (3,  2): (0xe8,  "3-2 Boost Bridges"),
    (3,  3): (0xe9,  "3-3 Suspension"),
    (3,  4): (0xea,  "3-4 Quaketray"),
    (3,  5): (0xeb,  "3-5 Aligner"),
    (3,  6): (0xec,  "3-6 Master of None"),
    (3,  7): (0xed,  "3-7 Ringfield"),
    (3,  8): (0xee,  "3-8 Trinity"),
    (3,  9): (0xef,  "3-9 Battle Royale"),
    (3, 10): (0x11,  "3-10 Actual Guillotine"),
    (4,  1): (0x12,  "4-1 Mandoline"),
    (4,  2): (0x13,  "4-2 Tug"),
    (4,  3): (0x14,  "4-3 Whirlers"),
    (4,  4): (0x15,  "4-4 Diaphragm"),
    (4,  5): (0x16,  "4-5 Roundabout"),
    (4,  6): (0x17,  "4-6 Catenary"),
    (4,  7): (0x18,  "4-7 Pattern Prism"),
    (4,  8): (0x19,  "4-8 Turbine"),
    (4,  9): (0x1a,  "4-9 Piercers"),
    (4, 10): (0x1b,  "4-10 Emitter"),
    (5,  1): (0x1c,  "5-1 Dragonfly"),
    (5,  2): (0x1d,  "5-2 Sway"),
    (5,  3): (0x1e,  "5-3 Jumpplex"),
    (5,  4): (0x1f,  "5-4 Drop of Doom"),
    (5,  5): (0x20,  "5-5 Perimeter"),
    (5,  6): (0x21,  "5-6 Rotary"),
    (5,  7): (0x22,  "5-7 Snakeskin"),
    (5,  8): (0x23,  "5-8 Range"),
    (5,  9): (0x24,  "5-9 Departure"),
    (5, 10): (0x25,  "5-10 Warp Dreams"),
    (6,  1): (0x26,  "6-1 Tripwire"),
    (6,  2): (0x27,  "6-2 Equilibrium"),
    (6,  3): (0x28,  "6-3 Rook"),
    (6,  4): (0x29,  "6-4 Rigidify"),
    (6,  5): (0x2a,  "6-5 Binary Launchers"),
    (6,  6): (0x2b,  "6-6 Pyramid Run"),
    (6,  7): (0x2c,  "6-7 Assembly"),
    (6,  8): (0x2d,  "6-8 Circus"),
    (6,  9): (0x2e,  "6-9 Seismic"),
    (6, 10): (0x2f,  "6-10 Slot Machine"),
    (7,  1): (0x119, "7-1 Ikaruga"),
    (7,  2): (0x11a, "7-2 Focus Breaker"),
    (7,  3): (0x11b, "7-3 Polarity"),
    (7,  4): (0x11c, "7-4 Carpets"),
    (7,  5): (0x11d, "7-5 Phantasm"),
    (7,  6): (0x11e, "7-6 Upstream"),
    (7,  7): (0x11f, "7-7 Rebuild"),
    (7,  8): (0x120, "7-8 Seige"),
    (7,  9): (0x121, "7-9 Albatross"),
    (7, 10): (0x30,  "7-10 Gaokao"),
    (8,  1): (0x31,  "8-1 Lock On"),
    (8,  2): (0x32,  "8-2 Recoil"),
    (8,  3): (0x33,  "8-3 Derelict"),
    (8,  4): (0x34,  "8-4 Gradient Descent"),
    (8,  5): (0x35,  "8-5 Raze"),
    (8,  6): (0x36,  "8-6 Gyroscope"),
    (8,  7): (0x37,  "8-7 Revision"),
    (8,  8): (0x38,  "8-8 Painted Pipe"),
    (8,  9): (0x39,  "8-9 Visionary"),
    (8, 10): (0x3a,  "8-10 Factory"),
    (9,  1): (0x3b,  "9-1 Demolition"),
    (9,  2): (0x3c,  "9-2 Twisty Triad"),
    (9,  3): (0x3d,  "9-3 Spinways"),
    (9,  4): (0x3e,  "9-4 Strum"),
    (9,  5): (0x3f,  "9-5 Antagonizer"),
    (9,  6): (0x40,  "9-6 Axle"),
    (9,  7): (0x41,  "9-7 Colossus"),
    (9,  8): (0x42,  "9-8 Fallout Zone"),
    (9,  9): (0x43,  "9-9 Lightspeed"),
    (9, 10): (0x44,  "9-10 Apparatus"),
    (10,  1): (0x155, "10-1 Exodus"),
    (10,  2): (0x156, "10-2 Pandora's Box"),
    (10,  3): (0x157, "10-3 Genesis"),
    (10,  4): (0x158, "10-4 Ausdauer"),
    (10,  5): (0x159, "10-5 Intermezzo"),
    (10,  6): (0x15a, "10-6 Trick Room"),
    (10,  7): (0x15b, "10-7 Ouroboros"),
    (10,  8): (0x15c, "10-8 Red Sea"),
    (10,  9): (0x15d, "10-9 Shadow Tag"),
    (10, 10): (0x15e, "10-10 Curtain Call"),
}
 
def story_level(world: int, level: int) -> tuple[int, str]:
    """Return (hex_code, label) for the given world-level combo."""
    if (world, level) not in LEVEL_TABLE:
        raise ValueError(f"No entry for World {world}-{level}")
    return LEVEL_TABLE[(world, level)]  
# level, bounding

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
    return logic


def level_check(world: int, level: int):
    hex_code, _ = story_level(world, level)
    return level_id == hex_code

def reset_level_check(world: int, level: int):
    hex_code, _ = story_level(world, level)
    return reset_if(level_id != hex_code)


#fix
def over_speed(mode: str, level, required_speed):
    speed_logic = [
        add_source(speed_pointer >> (low4(0x720) * 100)), # hundreds
        add_source(speed_pointer >> (low4(0x721) * 10)),  # tens
        speed_pointer >> low4(0x721) >= value(required_speed) # ones = goal
    ]
    logic = []
    logic.extend(mode_check(mode))

#todo: replace
def under_speed(mode, level, required_speed):
    return [
        add_source(speed_pointer >> (low4(0x720) * 100)), # hundreds
        add_source(speed_pointer >> (low4(0x721) * 10)),  # tens
        speed_pointer >> low4(0x721) <= value(required_speed) # ones = goal
    ]

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
def score_clear(mode, world, level, score_required):
    logic = [
        *mode_check(mode),
        level_check(world, level),
        and_next(level_score != 0xffffffff),
        trigger(level_score >= score_required),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        time != 0x00
    ]
    return logic

def switchless(mode, world, level, boxes, max_level_time):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (time == max_level_time * 60).with_hits(1)
    ]
    for box in boxes:
        logic.extend(box)
        logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
        logic.append(reset_if(bit2(0x0056e36a) == 0x01))


    logic.append(trigger(stage_complete_delta))
    logic.append(trigger(stage_complete))
    logic.append(reset_if(time == 0x00))

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
        (time == starting_time * 60).with_hits(1),
        reset_if(time == ((starting_time - within_time) * 60)),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(time == 0)
    ]

    return logic


def wormhole_limit_clear(mode, world, level, starting_time, max_wormhole_entries):
    max_wormhole_entries += 1
    print(wormhole_entered)
    print(wormhole_entered >> dword_be(0xd8).delta())
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (time == starting_time * 60).with_hits(1),
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


def clear_level_type(world: int, level: int, goal_type: int):
    """Return a condition list for clearing a level with a specific goal type."""
    hex_code, _ = story_level(world, level)
    return [
        and_next(level_id == hex_code),
        (bit2(0x0056e36a) == goal_type).with_hits(1)
    ]

colour_clears = {
    "": (1, 1, 0x01, "green"),
}

for x in extras:
    ach = Achievement(extras[x][0], extras[x][1], extras[x][2])
    match x:
        case "bananas":
            logic = [
                main_mode,
                story_mode,
                bananas_collected.delta() < 999,
                bananas_collected >= 999
            ]
        case "mx":
            logic = [
                main_mode,
                challenge_mode,
                level_id == 0x15b,
                bananas_remaining == 0
            ]
        case "colourful":
            logic = [
                main_mode,
                story_mode,
            ]
    ach.add_core(logic)
    mySet.add_achievement(ach)

for x in special_clears:
    ach = Achievement(special_clears[x][0], special_clears[x][1], special_clears[x][2])
    match x:
        case "1-1": # "Clear "1-1 Ease" with a stage score of 13,000 points or more
            logic = score_clear("non-challenge", 1, 1, 13000)
        case "1-5": # "Clear "1-5 Flippers" without pressing the switch
            boxes = [bounding(
                -62.0, -59.0,
                2.0, 3.0,
                -1.5, 1.5
            )] 
            logic = switchless("non-challenge", 1, 5, boxes, 60)
            print(logic)
        case "1-6": # "Clear "1-6 Pulse" without pressing any switches
            boxes = [bounding( ## middle
                -2.0, 2.0,
                0.0, 0.0,
                -2.0, 2.0,
            False), 
            bounding( ## top
                -24.0, -20.0,
                0.0, 0.0,
                -2.0, 2.0,
            False),
            bounding( ## right
                -2.0, 2.0,
                0.0, 0.0,
                -20.0, -16.0,
            False),
            bounding( ## left
                -2.0, 2.0,
                0.0, 0.0,
                16.0, 20.0,
            False)]
            logic = switchless("non-challenge", 1, 6, boxes, 60)
        case "1-7": # "Clear "1-7 Slopeshift" after collecting every banana
            logic = all_bananas_collected("non-challenge", 1, 7)
        case "1-10": # "Clear "1-10 Margin" in 5.5 seconds or less
            logic = timed("non-challenge", 1, 10, 60.0, 5.5)
        case "2-3": # "Clear "2-3 Landing Gear" without entering more than 1 wormhole
            logic = wormhole_limit_clear("non-challenge", 2, 3, 60, 1)
        case "2-4": # "Clear "2-4 Parkour" without pressing the switch
            boxes = [bounding(
                -0.5, 3,
                14.0, 15.0,
                2.5, 6
            )]
            logic = switchless("non-challenge", 2, 4, boxes, 60)
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
            boxes = [bounding( # bottom left
                62.0, 66.0,
                1.0, 2.0,
                -66.0, -62.0
            ),
            bounding( # top left
                62.0, 66.0,
                1.0, 2.0,
                30.0, 34.0
            ),
            bounding( # top right
               -66.0, -62.0,
                1.0, 2.0,
                62.0, 66.0
            ),
            bounding( # bottom right
                -66.0, -62.0,
                1.0, 2.0,
                -34.0, -30.0
            ),
            ]
            all_switches("non-challenge", 3, 9, boxes, 180)
        case "4-1": # "Clear "4-1 Mandoline" with a stage score of 11,000 points or more
            logic = score_clear("non-challenge", 4, 1, 11000)
        case "4-2": # "Clear "4-2 Tug" after taking the thin path
            continue
        case "4-6": # "Clear "4-6 Catenary" after collecting all bananas
            logic = all_bananas_collected("non-challenge", 4, 6)
        case "4-8": # "On "4-8 Turbine", hit all 3 switches within 5 seconds of each other
            continue
        case "5-3": # "Clear "5-3 Jumpplex" in 15 seconds or less
            logic = timed("non-challenge", 5, 3, 60, 15)
        case "5-6": # "Clear "5-6 Rotary" with all 5 banana bunches collected
            logic = banana_bunches_collected("non-challenge", 5, 6, 5)
        case "5-8": # "Clear "5-8 Range" going over 400mph
            continue
        case "5-9": # "Clear "5-9 Departure" in 30 seconds or less
            continue
        case "6-3": # "Clear "6-3 Rook" without collecting any bananas
            continue
        case "6-4": # "Clear "6-4 Rigidify" with both banana bunches collected
            continue
        case "6-6": # "Clear "6-6 Pyramid Run" in 7 seconds or less
            continue
        case "6-7": # "Clear "6-7 Assembly" without pressing any switches
            continue
        case "7-1": # "Clear "7-1 Ikaruga" collecting 1 banana at most
            continue
        case "7-3": # "Clear "7-3 Polarity" before the stage flips over for a 4th time
            continue
        case "7-5": # "Clear "7-5 Phantasm" with all bananas collected
            continue
        case "7-8": # "Clear "7-8 Siege" going over 150mph
            continue
        case "8-2": # "Clear "8-2 Recoil" with all 3 banana bunches collected
            continue
        case "8-4": # "Clear "8-4 Gradient Descent" without entering a wormhole
            continue
        case "8-8": # "Clear "8-8 Painted Pipe" with a stage score of 6,500 points or more
            continue
        case "8-9": # "Clear all 8 different layouts of "8-9 Visionary" in one session
            continue
        case "8-10": # "Clear "8-10 Factory" in 7 seconds or less
            continue
        case "9-2": # "Clear "9-2 Twisty Triad" with both banana bunches collected
            continue
        case "9-6": # "Clear "9-6 Axle" with the fast forward switch active
            continue
        case "9-7": # "Clear "9-7 Colossus" with all bananas collected
            continue
        case "10-7": # "Clear "10-7 Ouroboros" with the fast forward switch active
            continue
        case "MX-7": # "Clear "MX-7 Pride" by taking the thinner path after the switch
            continue
        case _:
            continue
    ach.add_core(logic)
    mySet.add_achievement(ach)


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
 