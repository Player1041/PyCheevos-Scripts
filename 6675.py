### Imports ###
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import delta, prior, bcd
import pycheevos.core.constants as const
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement

### Define Addresses ###

gameState = helpers.byte(0x0d4110)
#0x02 - Logos
#0x03 - Logos but rolled over from the main menu
#0x04 - Intro Cutscene
#0x05 - Win
#0x06 - Menus
#0x07 - In Game

hz = helpers.byte(0x0e1412)
#0x05 - 50hz
#0x06 - 60hz

loadingScreen = helpers.byte(0x0d4420)
#0x00 - No
#0x01 - Yes

raceOutcome = helpers.dword(0x03e378) # Pointer

raceData = (helpers.tbyte(0x1181a8) >> (helpers.tbyte(0x02A0)))

modeAddress = helpers.byte(0x0e3746)
demoAddress = helpers.byte(0x0e407c)

### Functions ###

demoCheck = (demoAddress == 0x00)
championship = (modeAddress == 0x00)
miniChampionship = (modeAddress == 0x01)
arcadeRace = (modeAddress == 0x02)

raceState = (raceData >> helpers.byte(0x38))
#0x00 - Loading
#0x01 - When set, resets race 
#0x02 - Flyover
#0x03 - Countdown
#0x04 - Racing
#0x05 - Win/Lose
#0x06 - Race result

credits = helpers.byte(0x0e3251)
creditIncrease = [
    Condition(credits.delta()).with_flag(add_source),
    Condition(value(0x01)).with_flag(add_source),
    Condition(value(0x00) == credits).with_flag(trigger) 
]

### Initialize Set ###

mySet = AchievementSet(game_id=6675, title="South Park Rally")

### Achievements ###

intro = Achievement("Come on Up to South Park!", "Watch the whole South Park intro", 5)
introCore = [
    (gameState.delta() == 0x02).with_flag(const.Flag.OR_NEXT),
    (gameState.delta() == 0x03).with_flag(const.Flag.RESET_IF),
    (gameState == 0x06)
]

introAlt1 = [
    (hz == 0x05).with_flag(const.Flag.AND_NEXT),
    (loadingScreen == 0x00).with_flag(const.Flag.AND_NEXT),
    (gameState.delta() == 0x04).with_hits(1420)
]

introAlt2 = [
    (hz == 0x06).with_flag(const.Flag.AND_NEXT),
    (loadingScreen == 0x00).with_flag(const.Flag.AND_NEXT),
    (gameState.delta() == 0x04).with_hits(1700),
]


intro.add_core(introCore)
intro.add_alt(introAlt1)
intro.add_alt(introAlt2)

intro.add_alt(creditIncrease)

mySet.add_achievement(intro)

mySet.save()