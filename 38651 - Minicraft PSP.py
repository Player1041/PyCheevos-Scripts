import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=38651, title="Minicraft PSP")
platform = "PSP"

BASE_ADDR = 0x009b3264
MENU_ID = dword(0x00e072c4)

# 0x00 - No Menu
# 0x01 - TitleMenu
# 0x02 - InventoryMenu
# 0x03 - CraftingMenu
# 0x04 - AboutMenu
# 0x05 - ContainerMenu
# 0x06 - DeadMenu
# 0x07 - ExitConfirmationMenu
# 0x08 - InstructionsMenu
# 0x09 - LevelTransitionMenu
# 0x0A - PauseMenu
# 0x0B - WhatsNewMenu
# 0x0C - WonMenu

achievements = {
    "Wood!":                   ("Earn the \"Wood!\" achievement by punching a tree and picking up your first wood.", 1),
    "Rockin' It":              ("Earn the \"Rockin' It\" achievement by mining some stone.", 1),
    "Smudged":                 ("Earn the \"Smudged\" achievement by mining some coal.", 1),
    "Going Deeper":            ("Earn the \"Going Deeper\" achievement by mining some iron ore.", 2),
    "Shiny!":                  ("Earn the \"Shiny!\" achievement by unearthing some gold ore.", 2),
    "Deep Find":               ("Earn the \"Deep Find\" achievement by discovering a gem far underground.", 3),
    "Ew Gross":                ("Earn the \"Ew Gross\" achievement by collecting some slime.", 2),
    "Soft":                    ("Earn the \"Soft\" achievement by collecting cloth from a Zombie.", 2),
    "Getting Started":         ("Earn the \"Getting Started\" achievement by crafting a wooden pickaxe.", 1),
    "Stone Age":               ("Earn the \"Stone Age\" achievement by crafting a stone pickaxe.", 2),
    "Iron Will":               ("Earn the \"Iron Will\" achievement by forging an iron pickaxe.", 2),
    "Golden Touch":            ("Earn the \"Golden Touch\" achievement by forging a gold pickaxe.", 3),
    "Best Pick":               ("Earn the \"Best Pick\" achievement by forging a gem pickaxe.", 5),
    "Lumberjack":              ("Earn the \"Lumberjack\" achievement by crafting a wooden axe.", 1),
    "Stone Chopper":           ("Earn the \"Stone Chopper\" achievement by crafting a stone axe.", 2),
    "Iron Woodsman":           ("Earn the \"Iron Woodsman\" achievement by forging an iron axe.", 2),
    "Gold Logger":             ("Earn the \"Gold Logger\" achievement by forging a gold axe.", 3),
    "Final Cut":               ("Earn the \"Final Cut\" achievement by forging a gem axe.", 5),
    "En Garde!":               ("Earn the \"En Garde!\" achievement by crafting a wooden sword.", 1),
    "Stone Warrior":           ("Earn the \"Stone Warrior\" achievement by crafting a stone sword.", 2),
    "Knight's Blade":          ("Earn the \"Knight's Blade\" achievement by forging an iron sword.", 2),
    "All That Glitters":       ("Earn the \"All That Glitters\" achievement by forging a gold sword.", 3),
    "Excalibur":               ("Earn the \"Excalibur\" achievement by forging a gem sword.", 5),
    "Digging Dirt":            ("Earn the \"Digging Dirt\" achievement by crafting a wooden shovel.", 1),
    "Stone Digger":            ("Earn the \"Stone Digger\" achievement by crafting a stone shovel.", 2),
    "Hard Labor":              ("Earn the \"Hard Labor\" achievement by forging an iron shovel.", 2),
    "Gilded Spade":            ("Earn the \"Gilded Spade\" achievement by forging a gold shovel.", 3),
    "Six Feet Deep":           ("Earn the \"Six Feet Deep\" achievement by forging a gem shovel.", 5),
    "Getting Crafty":          ("Earn the \"Getting Crafty\" achievement by placing your first workbench.", 1),
    "Smelting":                ("Earn the \"Smelting\" achievement by crafting and placing a furnace.", 1),
    "Heating Up":              ("Earn the \"Heating Up\" achievement by building and placing an oven.", 1),
    "On the Anvil":            ("Earn the \"On the Anvil\" achievement by building and placing an anvil.", 2),
    "An Apple a Day":          ("Earn the \"An Apple a Day\" achievement by eating your first apple.", 1),
    "Baker":                   ("Earn the \"Baker\" achievement by baking your first loaf of bread.", 1),
    "Let There Be Light":      ("Earn the \"Let There Be Light\" achievement by placing a torch or lantern.", 1),
    "Ahh My Eyes":             ("Earn the \"Ahh, My Eyes\" achievement by crafting a lantern.", 1),
    "Pack Rat":                ("Earn the \"Treasure Chest\" achievement by placing a chest.", 1),
    "Going Under":             ("Earn the \"Going Under\" achievement by descending into the caves.", 1),
    "Deeper Darkness":         ("Earn the \"Deeper Darkness\" achievement by reaching the lower cave level.", 2),
    "Into the Deep":           ("Earn the \"Into the Deep\" achievement by finding your way into the dungeon.", 2),
    "Sky High":                ("Earn the \"Sky High\" achievement by climbing up to the sky.", 3),
    "Air Apparent":            ("Earn the \"Air Apparent\" achievement by saving the world from the Air Wizard.", 5),
    "[VOID] One More Turn...":        ("Earn the \"One More Turn...\" achievement by continuing to play after the credits.", 0),
    "[VOID] Back for More":           ("Earn the \"Back for More\" achievement by starting a new game after winning.", 0),
    "Respawned":               ("Earn the \"Respawned\" achievement by dying for the first time. It happens.", 1),
    "Hungry?":                 ("Earn the \"Hungry?\" achievement by eating food for the first time.", 1),
    "Under the Water":         ("Earn the \"Under the Water\" achievement by inhaling a bit too much water", 1),
    "Slime Slayer":            ("Earn the \"Slime Slayer\" achievement by defeating your first slime.", 1),
    "Frostbite":               ("Earn the \"Frostbite\" achievement by defeating a cold slime.", 2),
    "Zombie Killer":           ("Earn the \"Zombie Killer\" achievement by defeating a zombie.", 1),
    "Frozen Dead":             ("Earn the \"Frozen Dead\" achievement by defeating a cold zombie.", 2),
    "Monster Hunter":          ("Earn the \"Monster Hunter\" achievement by defeating every regular mob type and variant.", 10),
    "Green Thumb":             ("Earn the \"Green Thumb\" achievement by planting a tree from an acorn.", 1),
    "Botanist":                ("Earn the \"Botanist\" achievement by planting a flower.", 1),
    "Shh...":                  ("Earn the \"Hidden Achievement 1\" and \"Hidden Achievement 2\" achievements by viewing the hidden QR codes on the main menu.", 1),
    "[VOID] Hidden Achievement 2":    ("Earn the \"Hidden Achievement 2\" achievement by viewing the QR code for: the-sauna.icu", 0),
    "Power Within":            ("Earn the \"Power Within\" achievement by using the Power Glove to lift something heavy.", 2),
    "[VOID] And That's a Wrap!":      ("Earn the \"And That's a Wrap!\" achievement by unlocking every non-hidden achievement.", 0),
    "Nice Try":                ("Earn the \"Nice Try\" achievement by inputting a code for... 30 lives? There isn't any lives in this game...", 1),
    "Prickly Up Here":         ("Earn the \"Prickly Up Here\" achievement by placing and harvesting a cactus really high up.", 2),
    "Snowball Fight!":         ("Earn the \"Snowball Fight!\" achievement by throwing a snowball.", 1),
    "Well That Was Quick!?":   ("Earn the \"Well That Was Quick!?\" by defeating the Air Wizard within an hour", 10),
}
id = 614782
for i, (title, (description, points)) in enumerate(achievements.items()):
    unlock_addr = BASE_ADDR + (i * 0x0C)
    unlock_flag = byte(unlock_addr)

    ach = Achievement(
        title=title,
        description=description,
        points=points,
        id=id
    )

    logic = [
        unlock_flag.delta() == 0x00,
        unlock_flag == 0x01
    ]
    match title:
        case "[VOID] One More Turn..." | "[VOID] Back for More" | "[VOID] Hidden Achievement 2" | "[VOID] And That's a Wrap!": 
            continue
        case "Shh...":
            logic = [
                add_source(unlock_flag.delta()),
                byte(unlock_addr + 0x0c).delta() == 0x01,
                add_source(unlock_flag),
                byte(unlock_addr + 0x0c) == 0x02,
            ]
            logic.append(MENU_ID == 0x01)
        case "Nice Try":
            logic.append(MENU_ID == 0x04)
        case _:
            logic.append(MENU_ID != 0x01)
            logic.append(MENU_ID != 0x0B)

    ach.add_core(logic)
    mySet.add_achievement(ach)
    id += 1



dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")
ppssppPath = Path("D:\\Games\\Emulation\\Emulators\\PPSSPP\\RACache\\Data")

match platform:
    case "Wii":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case "PSP":
        if ppssppPath.exists():
            mySet.save(ppssppPath)
    case default:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()
 