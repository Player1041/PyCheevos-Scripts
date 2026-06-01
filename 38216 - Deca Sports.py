import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=38216, title="Deca Sports")
platform = "Wii"


deca_challenge = {
    "badminton":                    ("gBad", "deca_challenge | badminton",                                                                   "Earn the Deca Challenge medal in Badminton", 5),
    "kart_racing_beginner":         ("gkar", "deca_challenge | kart_racing_beginner",                                                                       "Earn the Deca Challenge medal in Kart Racing - Beginner", 5),
    "kart_racing_intermediate":     ("gkar", "deca_challenge | kart_racing_intermediate",                                                           "Earn the Deca Challenge medal in Kart Racing - Intermediate", 5),
    "kart_racing_advanced":         ("gkar", "deca_challenge | kart_racing_advanced",                                                                "Earn the Deca Challenge medal in Kart Racing - Advanced", 5),
    "curling":                      ("gCur", "deca_challenge | curling",                                                                   "Earn the Deca Challenge medal in Curling", 5),
    "snowboard_cross_beginner":     ("gSno", "deca_challenge | snowboard_cross_beginner",                                                                   "Earn the Deca Challenge medal in Snowboard Cross - Beginner", 5),
    "snowboard_cross_intermediate": ("gSno", "deca_challenge | snowboard_cross_intermediate",                                                                   "Earn the Deca Challenge medal in Snowboard Cross - Intermediate", 5),
    "snowboard_cross_advanced":     ("gSno", "deca_challenge | snowboard_cross_advanced",                                                              "Earn the Deca Challenge medal in Snowboard Cross - Advanced", 10),
    "archery":                      ("gArc", "deca_challenge | archery",                                                                        "Earn the Deca Challenge medal in Archery", 5),
    "supercross_beginner":          ("gsup", "deca_challenge | supercross_beginner",                                                                   "Earn the Deca Challenge medal in Supercross - Beginner", 5),
    "supercross_intermediate":      ("gsup", "deca_challenge | supercross_intermediate",                                                                   "Earn the Deca Challenge medal in Supercross - Intermediate", 5),
    "supercross_advanced":          ("gsup", "deca_challenge | supercross_advanced",                                                                   "Earn the Deca Challenge medal in Supercross - Advanced", 10),
    "beach_volleyball":             ("gVol", "deca_challenge | beach_volleyball",                                                                     "Earn the Deca Challenge medal in Beach Volleyball", 5),
    "figure_skating":               ("gfig", "deca_challenge | figure_skating",                                                                   "Earn the Deca Challenge medal in Figure Skating", 5),
    "basketball":                   ("gBas", "deca_challenge | basketball",                                                                   "Earn the Deca Challenge medal in Basketball", 5),
    "soccer":                       ("gsoc", "deca_challenge | soccer",                                                                   "Earn the Deca Challenge medal in Soccer", 5),
}  

challenges = {

}

sport = byte(0x001bc92b)
tournament_game = byte(0x001bca8a) # this and sport use the same values
tournament_round = byte(0x001bca8b)
game_mode = byte(0x001bc92a)

character_chosen = byte(0x001bc851)
team_chosen = byte(0x001bc84f)

def character_type(type):
    characters = {
        "Team Thunder": {
            "Casey": "Speed",
            "Charlie": "Balance",
            "Brandon": "Power",
            "Flores": "Power",
            "Jarod": "Power"
        },
        "Mad Maidens": {
            "Meredith": "Speed",
            "Ash": "Speed",
            "Sarah": "Speed",
            "Chilla": "Balance",
            "Amy": "Power",
        },
        "Speed Strikers": {
            "Pete": "Speed",
            "Samuel": "Speed",
            "Devi": "Speed",
            "Shelly": "Speed",
            "Caroljean": "Speed",
        },
        "Hard Hitters": {
            "Lebron": "Power",
            "Urbando": "Power",
            "Kevin": "Power",
            "Kate": "Power",
            "Calyx": "Power"
        },
        "Average Joes": {
            "Brian": "Balance",
            "Pepe": "Balance",
            "Riley": "Balance",
            "Camegie": "Balance",
            "Jackie": "Balance",
        },
        "Crusaders": {
            "Ted": "Speed",
            "Adrian": "Balance",
            "Rufus": "Balance",
            "Stephanie": "Balance",
            "Ali": "Power",
        },
        "Boost Force": {
            "Billy": "Speed",
            "Jay": "Speed",
            "Laura": "Speed",
            "Sadie": "Power",
            "Olivia": "Power",
        },
        "Disco Knights": {
            "Stephan": "Speed",
            "Cliff": "Balance",
            "Tony": "Power",
            "Lucy": "Balance",
            "Sabine": "Power"
        }
    }

    speed_characters_logic = []
    balance_characters_logic = []
    power_characters_logic = []
    for tidx, (team, members) in enumerate(characters.items()):
        for cidx, (character, char_type) in enumerate(members.items()):
            match char_type:  # also fixed: was matching `character` (the name) instead of the type
                case "Speed":
                    speed_characters_logic.append(and_next(team_chosen == tidx))
                    speed_characters_logic.append(or_next(character_chosen == cidx))
                case "Balance":
                    balance_characters_logic.append(and_next(team_chosen == tidx))
                    balance_characters_logic.append(or_next(character_chosen == cidx))
                case "Power":
                    power_characters_logic.append(and_next(team_chosen == tidx))
                    power_characters_logic.append(or_next(character_chosen == cidx))
                case _:
                    print(f"ERROR: Bad type - {type}")
    print(speed_characters_logic)

ascii_mode = dword_be(0x001b4e90)
def mode_check(mode: str):
    modes = {
        "boot": 0x626F6F74, # Booting up
        "gArc": 0x67417263, # Archery
        "gBad": 0x67426164, # Badminton
        "gBas": 0x67426173, # Basketball
        "gCur": 0x67437572, # Curling
        "gfig": 0x67666967, # Figure Skating
        "gkar": 0x676B6172, # Kart Racing
        "gSno": 0x67536E6F, # Snowboard Cross
        "gsoc": 0x67736F63, # Soccer
        "gsup": 0x67737570, # Supercross
        "gVol": 0x67566F6C, # Beach Volleyball  
        "lock": 0x6C6F636B, # Locker Room
        "menu": 0x6D656E75, # Menu
        "selm": 0x73656C6D, # Select Menu
        "staf": 0x73746166, # Staff Roll
    }
    return value(modes.get(mode))

def get_trophy(mode: str):
    modes = {
        "beach_volleyball":             byte(0x1bcaec),
        "figure_skating":               byte(0x1bcaed),
        "soccer":                       byte(0x1bcaee),
        "archery":                      byte(0x1bcaef),
        "basketball":                   byte(0x1bcaf0),
        "snowboard_cross_beginner":     byte(0x1bcaf1),
        "snowboard_cross_intermediate": byte(0x1bcaf2),
        "snowboard_cross_advanced":     byte(0x1bcaf3),
        "badminton":                    byte(0x1bcaf4),
        "supercross_beginner":          byte(0x1bcaf5),
        "supercross_intermediate":      byte(0x1bcaf6),
        "supercross_advanced":          byte(0x1bcaf7),
        "curling":                      byte(0x1bcaf8),
        "kart_racing_beginner":         byte(0x1bcaf9),
        "kart_racing_intermediate":     byte(0x1bcafa),
        "kart_racing_advanced":         byte(0x1bcafb),
    }
    return modes.get(mode)


for sport, (mode, title, desc, points) in deca_challenge.items():
    ach = Achievement(title, desc, points)
    logic = [
        game_mode == 0x03,
        ascii_mode == mode_check(mode),
        get_trophy(sport).delta() == 0x00,
        get_trophy(sport) == 0x01
    ]

    ach.add_core(logic)
    mySet.add_achievement(ach)



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
 