import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=34836, title="New Play Control! Mario Power Tennis")
platform = "Wii"

# Exhibition

exAch = Achievement("Exhibition", "Do something idfk", 100)
exAch.add_core(value(0x00) == value(0x00))
for x in range(0x311354, 0x311498):
    logic = []
    logic.append(byte(x).delta() < 0x14)
    logic.append(byte(x) >= 0x14)
    exAch.add_alt(logic)

mySet.add_achievement(exAch)

#Gimmick
exAch = Achievement("Gimmick Exhibition", "Do something idfk", 100)
exAch.add_core(value(0x00) == value(0x00))
for x in range(0x311498, 0x3115dc):
    logic = []
    logic.append(byte(x).delta() < 0x14)
    logic.append(byte(x) >= 0x14)
    exAch.add_alt(logic)

mySet.add_achievement(exAch)

# Item Battle
exAch = Achievement("Item Battle Exhibition", "Do something idfk", 100)
exAch.add_core(value(0x00) == value(0x00))
for x in range(0x3115dc, 0x311720):
    logic = []
    logic.append(byte(x).delta() < 0x14)
    logic.append(byte(x) >= 0x14)
    exAch.add_alt(logic)

mySet.add_achievement(exAch)

# Ring Shot
exAch = Achievement("Ring Shot Exhibition", "Do something idfk", 100)
exAch.add_core(value(0x00) == value(0x00))
for x in range(0x311720, 0x311864):
    logic = []
    logic.append(byte(x).delta() < 0x14)
    logic.append(byte(x) >= 0x14)
    exAch.add_alt(logic)

mySet.add_achievement(exAch)

dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

match platform:
    case "Wii":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case default:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()