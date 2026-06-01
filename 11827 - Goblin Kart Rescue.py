import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pycheevos.models.leaderboard import Leaderboard
from pathlib import Path

mySet = AchievementSet(game_id=11827, title="Goblin Kart Rescue")
platform = "SMS"


main_prog = {
    "af":  ("Save the Goblins", "Rescue the princesses in every Ancient Forest track in Story Mode"),
    "dc":  ("Raised New Flags", "Rescue the princesses in every Dark Castle track in Story Mode"),
    "idp": ("It's So Peak...", "Rescue the princesses in every Ice Dragon Peak track in Story Mode"),
    "gh":  ("Goblin Savior", "Rescue the princesses in every Giant House track in Story Mode")
}

time_trials = {
    "ancient_forest": {
        "Ancient Forest 1": ("A Quick Jaunt", "Complete Ancient Forest 1 in Time Attack with every coin collected and within 0'10\"00", 1000),
        "Ancient Forest 2": ("A Gentle Stroll", "Complete Ancient Forest 2 in Time Attack with every coin collected and within 0'10\"00", 1000),
        "Ancient Forest 3": ("Rainy Day Fund", "Complete Ancient Forest 3 in Time Attack with every coin collected and within 0'12\"00", 1200),
        "Ancient Forest 4": ("Need for Greed", "Complete Ancient Forest 4 in Time Attack with every coin collected and within 0'10\"00", 1000),
        "Ancient Forest 5": ("Mud Running", "Complete Ancient Forest 5 in Time Attack with every coin collected and within 0'10\"00", 1000),
        "Ancient Forest 6": ("Grab the Shinies", "Complete Ancient Forest 6 in Time Attack with every coin collected and within 0'33\"00", 3300),
    },
    "dark_castle": {
        "Dark Castle 1": ("Mob on Mob Violence", "Complete Dark Castle 1 in Time Attack with every coin collected and within 0'14\"00", 1400),
        "Dark Castle 2": ("Castle Plunderin'", "Complete Dark Castle 2 in Time Attack with every coin collected and within 0'13\"00", 1300),
        "Dark Castle 3": ("Emptying the Coffers", "Complete Dark Castle 3 in Time Attack with every coin collected and within 0'12\"00", 1200),
        "Dark Castle 4": ("Taking the Scenic Route", "Complete Dark Castle 4 in Time Attack with every coin collected and within 0'15\"00", 1500),
        "Dark Castle 5": ("Burning Rubber", "Complete Dark Castle 5 in Time Attack with every coin collected and within 0'12\"00", 1200),
        "Dark Castle 6": ("A New Monarchy", "Complete Dark Castle 6 in Time Attack with every coin collected and within 0'54\"00", 5400),
    },
    "ice_dragon_peak": {
        "Ice Dragon Peak 1": ("Peak Cinema", "Complete Ice Dragon Peak 1 in Time Attack with every coin collected and within 0'16\"00", 1600),
        "Ice Dragon Peak 2": ("Cold Snap", "Complete Ice Dragon Peak 2 in Time Attack with every coin collected and within 0'11\"00", 1100),
        "Ice Dragon Peak 3": ("Ice to Meet You", "Complete Ice Dragon Peak 3 in Time Attack with every coin collected and within 0'12\"00", 1200),
        "Ice Dragon Peak 4": ("Frostbitten", "Complete Ice Dragon Peak 4 in Time Attack with every coin collected and within 0'14\"00", 1400),
        "Ice Dragon Peak 5": ("Chillin'", "Complete Ice Dragon Peak 5 in Time Attack with every coin collected and within 0'15\"00", 1500),
        "Ice Dragon Peak 6": ("The Long Freeze", "Complete Ice Dragon Peak 6 in Time Attack with every coin collected and within 0'42\"00", 4200),
    },
    "giant_house": {
        "Giant House 1": ("Watch Your Step", "Complete Giant House 1 in Time Attack with every coin collected and within 0'23\"00", 2300),
        "Giant House 2": ("Making Myself at Home", "Complete Giant House 2 in Time Attack with every coin collected and within 0'28\"00", 2800),
        "Giant House 3": ("Borrowed Without Asking", "Complete Giant House 3 in Time Attack with every coin collected and within 0'33\"00", 3300),
        "Giant House 4": ("Mind the Gap", "Complete Giant House 4 in Time Attack with every coin collected and within 0'36\"00", 3600),
        "Giant House 5": ("The Big House", "Complete Giant House 5 in Time Attack with every coin collected and within 0'35\"00", 3500),
        "Giant House 6": ("The Grand Tour", "Complete Giant House 6 in Time Attack with every coin collected and within 0'56\"00", 5600),
    }
}

endless = {
    "af":  ("Endless Appetite", "Complete every Ancient Forest track in Endless Mode"),
    "dc":  ("Perpetual Plunder", "Complete every Dark Castle track in Endless Mode"),
    "idp": ("Infinite Chill", "Complete every Ice Dragon Peak track in Endless Mode"),
    "gh":  ("There's No Place Like Home", "Complete every Giant House track in Endless Mode")
}

forest_prog = [bit1(0x2004), bit1(0x2005), bit1(0x2006), bit1(0x2007), bit1(0x2008), bit1(0x2009)]
castle_prog = [bit1(0x200A), bit1(0x200B), bit1(0x200C), bit1(0x200D), bit1(0x200E), bit1(0x200F)]
peak_prog   = [bit1(0x2010), bit1(0x2011), bit1(0x2012), bit1(0x2013), bit1(0x2014), bit1(0x2015)]
house_prog  = [bit1(0x2016), bit1(0x2017), bit1(0x2018), bit1(0x2019), bit1(0x201A), bit1(0x201B)]

coin_array = [bit1(0x0030).invert(), bit1(0x0031).invert(), bit1(0x0032).invert(), bit1(0x0033).invert(), bit1(0x0034).invert(), bit1(0x0035).invert(), bit1(0x0036).invert(), bit1(0x0037).invert()]

game_state = byte(0x001c92)
#0x00 - Main Menu
#0x30 - Transition
#0x38 - Racing

mode = byte(0x1a6d)
#0x00 - Endless
#0x01 - Story
#0x02 - Time Attack

world = byte(0x1a6b)
level = byte(0x1a6a)

dance = byte(0x1a5d)

time_logic = [
        add_source(byte(0x1938).bcd() * 10000),
        add_source(byte(0x1937).bcd() * 1000),
        add_source(byte(0x1936).bcd() * 100),
        add_source(byte(0x1935).bcd() * 10),
        remember(byte(0x1934).bcd())
]

def time_goal(goal: int):
    logic = []
    logic.append(reset_if(recall() >= goal))
    return logic

# Progression
for key, (title, desc) in main_prog.items():
    ach = Achievement(title, desc, 5)
    logic = []
    match key:
        case "af":
            enumOver = forest_prog
        case "dc":
            enumOver = castle_prog
        case "idp":
            enumOver = peak_prog
        case "gh":
            enumOver = house_prog

    for i, game in enumerate(enumOver):
        if i == len(enumOver) - 1:
            logic.append(game.delta() == (len(enumOver) - 1))
        else:
            logic.append(add_source(game.delta()))
    for i, game in enumerate(enumOver): 
        if i == len(enumOver) - 1:
            logic.append(measured(game == len(enumOver)))
        else:
            logic.append(add_source(game))

    ach.add_core(logic)
    mySet.add_achievement(ach)

# Time Trials

coin_logic = []
for i, coin in enumerate(coin_array):
    if i == len(coin_array) - 1:
        coin_logic.append(trigger(coin == (len(coin_array))))
    else:
        coin_logic.append(add_source(coin))


for aindex, area in enumerate(time_trials.items()):
    for index, (key, (title, desc, goal)) in enumerate(area[1].items()):
        ach = Achievement(title, desc, 5)
        logic = []
        logic.append(mode == 2)  # time attack
        logic.append(and_next(world == aindex))
        logic.append(level == index)  # index is 0-5 within the area
        logic.extend(coin_logic)
        logic.extend(time_logic)
        logic.append((recall() == 0).with_hits(1))
        logic.append(and_next(recall() != 0))
        logic.extend(time_goal(goal))
        logic.append(trigger(dance.delta() < dance))

        ach.add_core(logic)
        mySet.add_achievement(ach)

# Endless

endless_progress = byte(0x1fe3)

for index, (key, (title, desc)) in enumerate(endless.items()):
    ach = Achievement(title, desc, 5)
    logic = []
    
    logic.append(mode == 0)  # endless
    logic.append(endless_progress.delta() == (index + 1) * 6 - 1)
    logic.append(endless_progress == (index + 1)* 6)

    ach.add_core(logic)
    mySet.add_achievement(ach)

# Leaderboards

coin_logic_lb = []
for i, coin in enumerate(coin_array):
    if i == len(coin_array) - 1:
        coin_logic_lb.append(coin == (len(coin_array)))
    else:
        coin_logic_lb.append(add_source(coin))


count = 162850
for aindex, area in enumerate(time_trials.items()):
    for index, (key, (title, desc, goal)) in enumerate(area[1].items()):
        count = count + 1
        lb = Leaderboard(f"Time Attack - {key}", f"How fast can you complete {key} with every coin collected?", id=count, format=LeaderboardFormat.MILLISECS, lower_is_better=True)
        logic = []
        logic.append(mode == 2)  # time attack
        logic.append(and_next(world == aindex))
        logic.append(level == index)  # index is 0-5 within the area
        logic.extend(coin_logic_lb)
        logic.append(dance == 0x01)

        lb.set_start(logic)
        lb.set_cancel(value(0x00) == value(0x01))
        lb.set_submit(value(0x00) == value(0x00))
        
        lb.set_value([
        add_source(byte(0x1938).bcd() * 10000),
        add_source(byte(0x1937).bcd() * 1000),
        add_source(byte(0x1936).bcd() * 100),
        add_source(byte(0x1935).bcd() * 10),
        measured(byte(0x1934).bcd())
        ])

        mySet.add_leaderboard(lb)
        #mySet.add_achievement(ach)



dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

match platform:
    case "Wii":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case _:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()