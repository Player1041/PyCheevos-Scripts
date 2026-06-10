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

mySet = AchievementSet(game_id=38660, title="Super Monkey Ball 349")
platform = "GameCube"

# Titles/Descs
world_prog = {
    0: ("Eternal Sunset",                   "Clear Beginner", 5),
    1: ("Branching Paths",                   "Clear Beginner Extra playing the even-numbered stages", 5),
    2: ("Back Route",                   "Clear Beginner Extra playing the odd-numbered stages", 25),
}

extras = {
    "deathless":   ("349 Problems But A Life Ain't One",              "Clear SMB 349 without losing a life or using an optional warp goal", 10),
}

special_clears = {
    "B1-1":   ("Prismatic Warper",                                     "Enter both warp goals in \"B1 Refraction\" in a single session", 25),
    "B1-2":   ("Advanced Potassium Avoidance",              "Enter the blue goal in \"B1 Refraction\" without collecting any bananas", 5),
    "B3":     ("Wormin' It",                                "Clear \"B3 Worm\" in 14 seconds or less", 4),
    "B5":     ("Hey Stinky!",                               "Collect all bananas in \"B5 Shower\"", 3),
    "B7-1":   ("Powers of Pausing",                         "Enter both warp goals in \"B7 Powers of 10\" in a single session", 10),
    "B7-2":   ("Take the Bait",                                     "Clear \"B7 Powers of 10\" with all bananas collected", 4),
    "B8":     ("Finders Keepers",                           "Clear \"B8 Hide & Seek\" with the banana bunch collected", 5),
    "B9-1":   ("Emergency Operation",                                     "Clear \"B9 X-Ray\" without activating the pause switch"    , 3),
    "B9-2":   ("On Edge",                                   "Clear \"B9 X-Ray\" with all bananas collected", 10),
    "B10":    ("Base 10",                                   "Enter both goals in \"B10 Base\" in 5 seconds or less in one session", 5),
    "BX1":    ("Future Sight",                              "Clear \"BX1 Mirage\" in 5 seconds or less", 5),
    "BX4":    ("When Push Comes to Shove",                  "Clear \"BX4 Fake Out\" with all bananas collected", 3),
    "BX6":    ("Poisonous Speedrun",                        "Clear \"BX6 Poison\" without pressing the reverse switch", 5),
    "BX8":    ("You Make It Then If You're So Smart",                                     "Clear \"BX8 Horrible Stage Maker\" with exclusively Platform 2 paused", 4),
    "BX9":    ("Around the Rim",                            "Clear \"BX9 Sensitive Seesaw\" with all bananas collected", 5),
    "BX10":   ("Makin' Waves",                              "Clear \"BX10 Surfin' the Waves\" in 15 seconds or less", 5)
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
stage_over = (bit4(0x00553973) == 0x01)
death_counter = dword_be(0x00969c80)
switch_state = bit2(0x0056e36a)
in_game = dword_be(0x5bc484)
paused = bit3(0x005bc477)
lives = byte(0x005bc9a2)

# Modes
main_mode = (byte(0x0054df20) == 0x00)
sub_mode = byte(0x0054df27)
story_mode = (byte(0x0054df27) == 0x00)
challenge_mode = (byte(0x0054df27) == 0x01)
practice_mode = (byte(0x0054df27) == 0x02)

x_coord = float32_be(0x005bc9a4)
y_coord = float32_be(0x005bc9a8)
z_coord = float32_be(0x005bc9ac)

def bounding(x1, x2, y1, y2, z1, z2, include_y: bool = True):
    if x1 == int:
        float(x1)
    if x2 == int:
        float(x2)
    if y1 == int:
        float(y1)
    if y2 == int:
        float(y2)
    if z1 == int:
        float(z1)
    if z2 == int:
        float(z2)
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

def inverted_bounding(x1, x2, y1, y2, z1, z2, include_y: bool = True):
    if x1 == int:
        float(x1)
    if x2 == int:
        float(x2)
    if y1 == int:
        float(y1)
    if y2 == int:
        float(y2)
    if z1 == int:
        float(z1)
    if z2 == int:
        float(z2)
    match include_y:
        case True:
            return [
                or_next(x_coord >= x1),
                and_next(x_coord <= x2),
                or_next(y_coord >= y1),
                and_next(y_coord <= y2),
                or_next(z_coord >= z1),
                and_next(z_coord <= z2)
            ]
        case False:
            return [
                or_next(x_coord >= x1),
                and_next(x_coord <= x2),
                or_next(z_coord >= z1),
                and_next(z_coord <= z2)
            ]
        
def inverted_bounding_no_z(x1, x2, y1, y2, z1, z2, include_y: bool = True):
    if x1 == int:
        float(x1)
    if x2 == int:
        float(x2)
    if y1 == int:
        float(y1)
    if y2 == int:
        float(y2)
    if z1 == int:
        float(z1)
    if z2 == int:
        float(z2)
    match include_y:
        case True:
            return [
                or_next(x_coord >= x1),
                and_next(x_coord <= x2),
                or_next(y_coord >= y1),
                and_next(y_coord <= y2),
                or_next(z_coord >= z1),
                and_next(z_coord <= z2)
            ]
        case False:
            return [
                or_next(x_coord >= x1),
                and_next(x_coord <= x2),
            ]

# world, level, hex, name, starting time
LEVEL_TABLE: dict[tuple[Union[int, str], int], tuple[int, str, int]] = {
    ("B",  1):  (0x0C9,  "B1 Refraction", 60),
    ("B",  2):  (0x0CA,  "B2 Cloth", 60),
    ("B",  3):  (0x0CB,  "B3 Worm", 60),
    ("B",  4):  (0x0CC,  "B4 Mirrors", 60),
    ("B",  5):  (0x0CD,  "B5 Shower", 60),
    ("B",  6):  (0x0CE,  "B6 Acoustic Insulation", 60),
    ("B",  7):  (0x0CF,  "B7 Powers of 10", 60),
    ("B",  8):  (0x0D0,  "B8 Hide & Seek", 60),
    ("B",  9):  (0x0D1,  "B9 X-Ray", 60),
    ("B", 10):  (0x0D2,  "B10 Base", 60),
    ("BX",  1): (0x0D3,  "BX1 Mirage", 60),
    ("BX",  2): (0x0D4,  "BX2 Break In", 60),
    ("BX",  3): (0x0D5,  "BX3 Downward Trend", 200),
    ("BX",  4): (0x0D6,  "BX4 Fake Out", 60),
    ("BX",  5): (0x0D7,  "BX5 Shadow", 60),
    ("BX",  6): (0x0D8,  "BX6 Poison", 60),
    ("BX",  7): (0x0D9,  "BX7 Fourth Wall Seesaw", 60),
    ("BX",  8): (0x0DA,  "BX8 Horrible Stage Maker", 90),
    ("BX",  9): (0x0DB,  "BX9 Sensitive Seesaw", 60),
    ("BX", 10): (0x0DC,  "BX10 Surfin' the Waves", 60),
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

def all_bananas_collected_old(mode, world, level):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (bananas_remaining != 0).with_hits(1),
        trigger(bananas_remaining == 0),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_over),
        reset_if(time == 0x00)
    ]
    return logic

def all_bananas_collected(mode, world, level):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (bananas_remaining != 0).with_hits(1),
        trigger(bananas_remaining == 0),
        trigger(bit5(0x00553973).prior() == 0x00),
        trigger(stage_complete),
        reset_if(stage_over),
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
        reset_if(stage_over),
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
        reset_if(stage_over),
        reset_if(time == 0x00)
    ])

    return logic

def maximum_bananas_collected(mode, world, level, starting_time, max_bananas):
    if max_bananas != 0:
        max_bananas += 1
    logic = [
        *mode_check("non-challenge"),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
        reset_if(bananas_remaining < bananas_remaining.delta()).with_hits(max_bananas),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(stage_over),
        reset_if(time == 0x00)
    ]

    return logic

def score_clear(mode, world, level, score_required):
    logic = [
        *mode_check(mode),
        level_check(world, level),
        and_next(level_score != 0xffffffff),
        trigger(level_score >= score_required),
        trigger(bit4(goal_state).delta() == 0x00),
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
    logic.append(reset_if(stage_over))
    logic.append(reset_if(time == 0x00))

    return logic

def miss_specific_switch(mode, world, level, boxes, starting_time):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1)
    ]

    for box in boxes:
        logic.extend(box)
        logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
        logic.append(reset_if(bit2(0x0056e36a) == 0x01))

    logic.append(trigger(stage_complete_delta))
    logic.append(trigger(stage_complete))
    logic.append(reset_if(stage_over))
    logic.append(reset_if(time == 0x00))

    return logic

def all_but_one_switch_off(mode, world, level, boxes, starting_time, extra = None):
    # requires an inverted bounding box
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1)
    ]

    match extra:
        case "two_box":
            for box in boxes:
                logic.extend(box)
            logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
            logic.append(reset_if(bit2(0x0056e36a) == 0x01))
            logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
            logic.append(trigger(bit2(0x0056e36a) == 0x01).with_hits(2))
        case _:
            for box in boxes:
                logic.extend(box)
                logic.append(and_next(bit2(0x0056e36a).delta() == 0x00))
                logic.append(reset_if(bit2(0x0056e36a) == 0x01))

    logic.append(trigger(stage_complete_delta))
    logic.append(trigger(stage_complete))
    logic.append(reset_if(stage_over))
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
        reset_if(stage_over),
        reset_if(time == 0x00)
    ]

    return logic

def bananaless(mode, world, level, starting_time):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        (time == starting_time * 60).with_hits(1),
        reset_if(bananas_remaining < bananas_remaining.delta()),
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
        reset_if(stage_over),
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
        reset_if(stage_over),
        reset_if(time == 0x00)
    ])

    return logic

def multiple_goals_within_time(mode, world, level, starting_time, within_time, boxes):
    if starting_time == int:
        float(starting_time)
    if within_time == int:
        float(within_time)

    logic = [
        *mode_check(mode),
        level_check(world, level),
        reset_next_if(time == starting_time * 60),
        pause_if(time <= (starting_time - within_time) * 60),
        (time.prior() == starting_time * 60).with_hits(1),
    ]

    for box in boxes:
        logic.extend(box)
        logic.append(and_next(stage_complete_delta))
        logic.append(add_hits(stage_complete).with_hits(1))

    logic.append(measured(value(0x00) == value(0x01)).with_hits(len(boxes)))
    return logic

def level_maker_total_switches_active(mode, world, level, starting_time, total_switches_active, on_switches, off_switches):
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        reset_if(time == starting_time * 60),
        (time.prior() == starting_time * 60).with_hits(1),
    ]

    for box in on_switches:
        logic.extend(box)
        logic.append(and_next(switch_state.delta() == 0x00))
        logic.append(add_hits(switch_state == 0x01).with_hits(1))

    for box in off_switches:
        logic.extend(box)
        logic.append(and_next(switch_state.delta() == 0x00))
        logic.append(sub_hits(switch_state == 0x01).with_hits(1))

    logic.append(reset_next_if(value(0x00) == value(0x01)).with_hits(total_switches_active + 1))
    logic.append(trigger(value(0x00) == value(0x00)))
    logic.append(trigger(stage_complete_delta))
    logic.append(trigger(stage_complete))
    logic.append(reset_if(time == 0x00))

    return logic

def challenge_and_extra(mode, world, starting_time):
    logic = [
        *mode_check("challenge")
    ]

    match world:
        case "B":
            logic.extend([
                and_next(level_check("B", 1)),
                (time == starting_time * 60).with_hits(1),
                and_next(level_check("BX", 10)),
                and_next(stage_complete_delta),
                trigger(stage_complete),   
                pause_if(lives.delta() > lives).with_hits(1),
                and_next(level_check("B", 1)),
                and_next(stage_complete_delta),
                and_next(stage_complete),
                reset_if(goal_type_entered != 0x00),
                and_next(level_check("B", 7)),
                and_next(stage_complete_delta),
                and_next(stage_complete),
                reset_if(goal_type_entered != 0x00),
            ])

    return logic

for world, (title, description, points) in world_prog.items():
    ach = Achievement(title, description, points)
    logic = [
        *mode_check("challenge")
    ]
    match world:
        case 0:
            logic.append(level_check("B", 10))
        case 1:
            logic.append(level_id.prior() == 0xda)
            logic.append(level_check("BX", 10))
        case 2:
            logic.append(level_id.prior() == 0xdb)
            logic.append(level_check("BX", 10))
    logic.extend([
        reset_if(time == 60 * 60),
        (time.prior() == 60 * 60).with_hits(1),
        trigger(stage_complete_delta),
        trigger(stage_complete),
        reset_if(time == 0)
    ])
    ach.add_core(logic)
    mySet.add_achievement(ach)

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
        case "deathless":
            logic = challenge_and_extra("challenge", "B", 60)
            altLogic = [reset_if(in_game == 0x00)]
    ach.add_core(logic)
    ach.add_alt(altLogic)
    mySet.add_achievement(ach)

for x in special_clears:
    ach = Achievement(special_clears[x][0], special_clears[x][1], special_clears[x][2])
    match x:
        case "B1-1": # Enter both warp goals in \"B1 Refraction\" in a single session
            logic = [
                *mode_check("non-story"),
                clear_level_type("B", 1, "green"),
                clear_level_type("B", 1, "red"),
                measured(value(0x00) == value(0x01)).with_hits(2)
            ]
        case "B1-2": # Enter the blue goal in \"B1 Refraction\" without collecting any bananas
            logic = bananaless("non-story", "B", 1, 60)
            logic.append(trigger(goal_type_entered == 0x00)) # blue goal
        case "B3":   # Clear \"B3 Worm\" in 14 seconds or less
            logic = timed("non-story", "B", 3, 60, 14)
        case "B5":   # Collect all bananas in \"B5 Shower\"
            logic = all_bananas_collected("non-story", "B", 5)
        case "B7-1": # Enter both warp goals in \"B7 Powers of 10\" in a single session
            logic = [
                *mode_check("non-story"),
                clear_level_type("B", 7, "green"),
                clear_level_type("B", 7, "red"),
                measured(value(0x00) == value(0x01)).with_hits(2)
            ]
        case "B7-2": # Clear \"B7 Powers of 10\" with all bananas collected
            logic = all_bananas_collected("non-story", "B", 7)
        case "B8":   # Clear \"B8 Hide & Seek\" with the banana bunch collected
            logic = banana_bunches_collected("non-story", "B", 8, 1)
        case "B9-1": # Clear \"B9 X-Ray\" without activating the pause switch
            logic = switchless("non-story", "B", 9, 60)
        case "B9-2": # Clear \"B9 X-Ray\" with all bananas collected
            logic = all_bananas_collected("non-story", "B", 9)
        case "B10":  # Enter both goals in \"B10 Base\" in 5 seconds or less in one session
            logic = multiple_goals_within_time("non-story", "B", 10, 60, 5, [bounding(
                -3.0, 2.0,
                -0.5, 0.5,
                47.0, 53.0
            ),
            bounding(
                -3.0, 2.0,
                -7.0, -6.0,
                47.0, 53.0
            )])
        case "BX1":  # Clear \"BX1 Mirage\" in 5 seconds or less
            logic = timed("non-story", "BX", 1, 60, 5)
        case "BX4":  # Clear \"BX4 Fake Out\" with all bananas collected
            logic = all_bananas_collected("non-story", "BX", 4)
        case "BX6":  # Clear \"BX6 Poison\" without pressing the reverse switch
            logic = all_but_one_switch_off("non-story", "BX", 6, [inverted_bounding(
                12.0, 8.0,
                3.0, 2.0,
                21.0, 17.0,
                False)], 60, )
        case "BX8":  # Clear \"BX8 Horrible Stage Maker\" activating only one pause switch
            logic = all_but_one_switch_off("non-story", "BX", 8, [
            inverted_bounding_no_z(
                9.5, 6.5,
                0.0, 0.0,
                38.0, 34.0,
            False),
            inverted_bounding_no_z(
                -16.5, -20.0,
                0.0, 0.0,
                38.0, 34.5,
            False)], 90, "two_box")
        case "BX9":  # Clear \"BX9 Sensitive Seesaw\" with all bananas collected
            logic = all_bananas_collected("non-story", "BX", 9)
        case "BX10": # Clear \"BX10 Surfin' the Waves\" in 15 seconds or less
            logic = timed("non-story", "BX", 10, 60, 15)
        case _:
            continue
    ach.add_core(logic)
    mySet.add_achievement(ach)

#
# Leaderboards


# Times
for (world, level), (hex_code, title, starting_time) in LEVEL_TABLE.items():
    
    match (world, level):
        case ("BX", 7):
            lb = Leaderboard(f"{title} - Fastest Time", "Clear this as fast as possible!")
            lb.format = LeaderboardFormat.FRAMES
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-story"),
                level_check(world, level),
                time != 0x00,
                time == starting_time * 60,
            ])
            lb.set_cancel([
                in_game == 0x00
            ])
            lb.set_submit([
                (time != starting_time * 60),
                stage_complete_delta,
                stage_complete,
            ])
            lb.set_value([
                measured(time)
            ])
            mySet.add_leaderboard(lb)

        case ("B", 1) | ("B", 5) | ("B", 7) | ("B", 8) | ("B", 10) | ("BX", 1) | ("BX", 2) | ("BX", 4) | ("BX", 6) | ("BX", 8) | ("BX", 9) | ("BX", 10):
            lb = Leaderboard(f"{title} - Fastest Time", "Clear this as fast as possible!")
            lb.format = LeaderboardFormat.FRAMES
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-story"),
                level_check(world, level),
                time != 0x00,
                time == starting_time * 60,
            ])
            lb.set_cancel([
                paused == 0x01
            ])
            lb.set_submit([
                (time != starting_time * 60),
                stage_complete_delta,
                stage_complete,
            ])
            lb.set_value([
                measured(time)
            ])
            mySet.add_leaderboard(lb)

            lb = Leaderboard(f"{title} - Highest Score", "Set the highest score!")
            lb.format = LeaderboardFormat.SCORE
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-story"),
                level_check(world, level),
                time != 0x00,
                time == starting_time * 60,
            ])

            lb.set_cancel([
                paused == 0x01
            ])

            lb.set_submit([
                (time != starting_time * 60),
                stage_complete,
                bit4(goal_state).delta() == 0x00,
                bit4(goal_state) == 0x01,
            ])

            lb.set_value([
                measured(level_score)
            ])

            mySet.add_leaderboard(lb)

        case _:
            lb = Leaderboard(f"{title} - Fastest Time", "Clear this as fast as possible!")
            lb.format = LeaderboardFormat.FRAMES
            lb.lower_is_better = False
            lb.set_start([
                *mode_check("non-story"),
                level_check(world, level),
                time != 0x00,
                time == starting_time * 60,
            ])
            lb.set_cancel([
                paused == 0x01
            ])
            lb.set_submit([
                (time != starting_time * 60),
                stage_complete_delta,
                stage_complete,
            ])
            lb.set_value([
                measured(time)
            ])
            mySet.add_leaderboard(lb)

        


rp = RichPresence()
rp.add_lookup("Level", {
0x0C9: "B1 Refraction",
0x0CA: "B2 Cloth",
0x0CB: "B3 Worm",
0x0CC: "B4 Mirrors",
0x0CD: "B5 Shower",
0x0CE: "B6 Acoustic Insulation",
0x0CF: "B7 Powers of 10",
0x0D0: "B8 Hide & Seek",
0x0D1: "B9 X-Ray",
0x0D2: "B10 Base",
0x0D3: "BX1 Mirage",
0x0D4: "BX2 Break In",
0x0D5: "BX3 Downward Trend",
0x0D6: "BX4 Fake Out",
0x0D7: "BX5 Shadow",
0x0D8: "BX6 Poison",
0x0D9: "BX7 Fourth Wall Seesaw",
0x0DA: "BX8 Horrible Stage Maker",
0x0DB: "BX9 Sensitive Seesaw",
0x0DC: "BX10 Surfin' the Waves",
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
    [level_id != 0xffffffff],
    f"Rolling around in {rp.lookup("Level", level_id)} | {rp.lookup('Mode', sub_mode)} | Bananas: {rp.value(bananas_collected)} | Score: {rp.value(score)} | Lives: {rp.value(lives)}"
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
 