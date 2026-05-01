import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=0, title="Template")
platform = "Wii"

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