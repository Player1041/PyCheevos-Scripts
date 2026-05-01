import pycheevos.core.helpers as helpers
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=19693, title="NHL Rock the Rink")

gameState = byte(0x090c20)

coreLogic = [
    prior(gameState) == 0x0b,
    gameState == 0x0c
]
# Elite
unlockElites = Achievement("Can't Stop Scoring", "Score 500 goals and unlock the NHL Elite Team", 1)
unlockElites.add_core(coreLogic)
eliteUnlocks = [byte(0x091638), byte(0x091958), byte(0x091c78), byte(0x091f98), byte(0x0922b8), byte(0x0925d8), byte(0x0928f8), byte(0x092c18), byte(0x092f38), byte(0x093258)]
for x in eliteUnlocks:
    altLogic = [
    delta(x) == 0x00,
    x == 0x01
    ]
    unlockElites.add_alt(altLogic)

mySet.add_achievement(unlockElites)

unlockNA = Achievement("No Such Thing as Skill Disparity", "Win a match on every difficulty and unlock the NHL All Star - North America team", 1)
unlockNA.add_core(coreLogic)

naUnlocks = [byte(0x091618), byte(0x091938), byte(0x091c58), byte(0x091f78), byte(0x092298), byte(0x0925b8), byte(0x0928d8), byte(0x092bf8), byte(0x092f18), byte(0x093238)]
for x in naUnlocks:
    altLogic = [
    delta(x) == 0x00,
    x == 0x01
    ]
    unlockNA.add_alt(altLogic)

mySet.add_achievement(unlockNA)

unlockWorld= Achievement("We're Not Larping This Time", "Win a match with every fantasy team, including Reapers, and unlock the NHL All-Star - World team", 1)
unlockWorld.add_core(coreLogic)

worldUnlocks = [byte(0x091628), byte(0x091948), byte(0x091c68), byte(0x091f88), byte(0x0922a8), byte(0x0925c8), byte(0x0928f8), byte(0x092c08), byte(0x092f28), byte(0x093248)]
for x in worldUnlocks:
    altLogic = [
    delta(x) == 0x00,
    x == 0x01
    ]
    unlockWorld.add_alt(altLogic)

mySet.add_achievement(unlockWorld)
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

if laptopPath.exists():
    mySet.save(laptopPath)
elif pcPath.exists():
    mySet.save(pcPath)
else:
    mySet.save()