import pycheevos.core.helpers as helpers
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=20965, title="Frogger: The Great Quest")

main_pointer = dword(0x00218148)

def titles_complete(name):
    return {
    "Rolling River Creek": "Journey Has Started",
    "Bog Town": f"Complete {name}",
    "Slick Willy's River Boat": f"Complete {name}",
    "River Town": f"Complete {name}",
    "Mushroom Valley": f"Complete {name}",
    "Fairy Town in Spring": f"Complete {name}",
    "The Tree of Knowledge": f"Complete {name}",
    "Fairy Town in Summer": f"Complete {name}",
    "The Cat Dragon's Lair": f"Complete {name}",
    "Fairy Town in Autumn": f"Complete {name}",
    "The Dark Trail Ruins": f"Complete {name}",
    "Dr. Starkenstein's Castle": f"Complete {name}",
    "The Catacombs": f"Complete {name}",
    "Goblin Trail": f"Complete {name}",
    "The Goblin Fort": f"Complete {name}",
    "Joy Castle": f"Complete {name}",
    "The Towers of Joy Castle": "Journey Has Finished"
    }.get(name)

def titles_shop(name):
    return {
    "Rolling River Creek": f"Shop {name}",
    "Bog Town": f"Shop {name}",
    "Slick Willy's River Boat": f"Shop {name}",
    "River Town": f"Shop {name}",
    "Mushroom Valley": f"Shop {name}",
    "Fairy Town in Spring": f"Shop {name}",
    "The Tree of Knowledge": f"Shop {name}",
    "Fairy Town in Summer": f"Shop {name}",
    "The Cat Dragon's Lair": f"Shop {name}",
    "Fairy Town in Autumn": f"Shop {name}",
    "The Dark Trail Ruins": f"Shop {name}",
    "Dr. Starkenstein's Castle": f"Shop {name}",
    "The Catacombs": f"Shop {name}",
    "Goblin Trail": f"Shop {name}",
    "The Goblin Fort": f"Shop {name}",
    "Joy Castle": f"Shop {name}",
    "The Towers of Joy Castle": f"Shop {name}",
    "Everything": f"Shop {name}"
    }.get(name)

def titles_speedrun(name):
    return {
    "Rolling River Creek": f"Placeholder {name}",
    "Bog Town": f"Placeholder {name}",
    "Slick Willy's River Boat": f"Placeholder {name}",
    "River Town": f"Placeholder {name}",
    "Mushroom Valley": f"Placeholder {name}",
    "Fairy Town in Spring": f"Placeholder {name}",
    "The Tree of Knowledge": f"Placeholder {name}",
    "Fairy Town in Summer": f"Placeholder {name}",
    "The Cat Dragon's Lair": f"Placeholder {name}",
    "Fairy Town in Autumn": f"Placeholder {name}",
    "The Dark Trail Ruins": f"Placeholder {name}",
    "Dr. Starkenstein's Castle": f"Placeholder {name}",
    "The Catacombs": f"Placeholder {name}",
    "Goblin Trail": f"Placeholder {name}",
    "The Goblin Fort": f"Placeholder {name}",
    "Joy Castle": f"Placeholder {name}",
    "The Towers of Joy Castle": f"Placeholder {name}",
    }.get(name)

def desc_complete(name):
    return f"Complete \"{name}\""

def desc_shop(name):
    return f"Purchase every item at the end of \"{name}\". If you have leaderboard indicators enabled in your emulator settings, press R2 and L3 to check how much is left to collect to purchase everything in the level."

def desc_speedrun(name):
    return {
    "Rolling River Creek": "",
    "Bog Town": "",
    "Slick Willy's River Boat": "",
    "River Town": "",
    "Mushroom Valley": "",
    "Fairy Town in Spring": "",
    "The Tree of Knowledge": "",
    "Fairy Town in Summer": "",
    "The Cat Dragon's Lair": "",
    "Fairy Town in Autumn": "",
    "The Dark Trail Ruins": "",
    "Dr. Starkenstein's Castle": "",
    "The Catacombs": "",
    "Goblin Trail": "",
    "The Goblin Fort": "",
    "Joy Castle": "",
    "The Towers of Joy Castle": ""
    }.get(name)



shopUnlockFlagsMem = {
    "Rolling River Creek": [main_pointer >> bit1(0x3EC), main_pointer >> bit2(0x3EC), main_pointer >> bit3(0x3EC)],
    "Bog Town": [main_pointer >> bit4(0x3EC), main_pointer >> bit5(0x3EC), main_pointer >> bit6(0x3EC)],
    "Slick Willy's River Boat": [main_pointer >> bit7(0x3EC), main_pointer >> bit0(0x3ED), main_pointer >> bit1(0x3ED)],
    "River Town": [main_pointer >> bit2(0x3ED), main_pointer >> bit3(0x3ED), main_pointer >> bit4(0x3ED)],
    "Mushroom Valley": [main_pointer >> bit5(0x3ED), main_pointer >> bit6(0x3ED), main_pointer >> bit7(0x3ED)],
    "Fairy Town in Spring": [main_pointer >> bit0(0x3EE), main_pointer >> bit1(0x3EE), main_pointer >> bit2(0x3EE)],
    "The Tree of Knowledge": [main_pointer >> bit3(0x3EE), main_pointer >> bit4(0x3EE), main_pointer >> bit5(0x3EE)],
    "Fairy Town in Summer": [main_pointer >> bit6(0x3EE), main_pointer >> bit7(0x3EE), main_pointer >> bit0(0x3EF)],
    "The Cat Dragon's Lair": [main_pointer >> bit1(0x3EF), main_pointer >> bit2(0x3EF), main_pointer >> bit3(0x3EF)],
    "Fairy Town in Autumn": [main_pointer >> bit4(0x3EF), main_pointer >> bit5(0x3EF), main_pointer >> bit6(0x3EF)],
    "The Dark Trail Ruins": [main_pointer >> bit7(0x3EF), main_pointer >> bit0(0x3F0), main_pointer >> bit1(0x3F0)],
    "Dr. Starkenstein's Castle": [main_pointer >> bit2(0x3F0), main_pointer >> bit3(0x3F0), main_pointer >> bit4(0x3F0)],
    "The Catacombs": [main_pointer >> bit5(0x3F0), main_pointer >> bit6(0x3F0), main_pointer >> bit7(0x3F0)],
    "Goblin Trail": [main_pointer >> bit0(0x3F1), main_pointer >> bit1(0x3F1), main_pointer >> bit2(0x3F1)],
    "The Goblin Fort": [main_pointer >> bit3(0x3F1), main_pointer >> bit4(0x3F1), main_pointer >> bit5(0x3F1)],
    "Joy Castle": [main_pointer >> bit6(0x3F1), main_pointer >> bit7(0x3F1), main_pointer >> bit0(0x3F2)],
    "The Towers of Joy Castle": [main_pointer >> bit1(0x3F2), main_pointer >> bit2(0x3F2), main_pointer >> bit3(0x3F2)],
}

shopUnlockFlagsDelta = {
    "Rolling River Creek": [main_pointer >> bit1(0x3EC).delta(), main_pointer >> bit2(0x3EC).delta(), main_pointer >> bit3(0x3EC).delta()],
    "Bog Town": [main_pointer >> bit4(0x3EC).delta(), main_pointer >> bit5(0x3EC).delta(), main_pointer >> bit6(0x3EC).delta()],
    "Slick Willy's River Boat": [main_pointer >> bit7(0x3EC).delta(), main_pointer >> bit0(0x3ED).delta(), main_pointer >> bit1(0x3ED).delta()],
    "River Town": [main_pointer >> bit2(0x3ED).delta(), main_pointer >> bit3(0x3ED).delta(), main_pointer >> bit4(0x3ED).delta()],
    "Mushroom Valley": [main_pointer >> bit5(0x3ED).delta(), main_pointer >> bit6(0x3ED).delta(), main_pointer >> bit7(0x3ED).delta()],
    "Fairy Town in Spring": [main_pointer >> bit0(0x3EE).delta(), main_pointer >> bit1(0x3EE).delta(), main_pointer >> bit2(0x3EE).delta()],
    "The Tree of Knowledge": [main_pointer >> bit3(0x3EE).delta(), main_pointer >> bit4(0x3EE).delta(), main_pointer >> bit5(0x3EE).delta()],
    "Fairy Town in Summer": [main_pointer >> bit6(0x3EE).delta(), main_pointer >> bit7(0x3EE).delta(), main_pointer >> bit0(0x3EF).delta()],
    "The Cat Dragon's Lair": [main_pointer >> bit1(0x3EF).delta(), main_pointer >> bit2(0x3EF).delta(), main_pointer >> bit3(0x3EF).delta()],
    "Fairy Town in Autumn": [main_pointer >> bit4(0x3EF).delta(), main_pointer >> bit5(0x3EF).delta(), main_pointer >> bit6(0x3EF).delta()],
    "The Dark Trail Ruins": [main_pointer >> bit7(0x3EF).delta(), main_pointer >> bit0(0x3F0).delta(), main_pointer >> bit1(0x3F0).delta()],
    "Dr. Starkenstein's Castle": [main_pointer >> bit2(0x3F0).delta(), main_pointer >> bit3(0x3F0).delta(), main_pointer >> bit4(0x3F0).delta()],
    "The Catacombs": [main_pointer >> bit5(0x3F0).delta(), main_pointer >> bit6(0x3F0).delta(), main_pointer >> bit7(0x3F0).delta()],
    "Goblin Trail": [main_pointer >> bit0(0x3F1).delta(), main_pointer >> bit1(0x3F1).delta(), main_pointer >> bit2(0x3F1).delta()],
    "The Goblin Fort": [main_pointer >> bit3(0x3F1).delta(), main_pointer >> bit4(0x3F1).delta(), main_pointer >> bit5(0x3F1).delta()],
    "Joy Castle": [main_pointer >> bit6(0x3F1).delta(), main_pointer >> bit7(0x3F1).delta(), main_pointer >> bit0(0x3F2).delta()],
    "The Towers of Joy Castle": [main_pointer >> bit1(0x3F2).delta(), main_pointer >> bit2(0x3F2).delta(), main_pointer >> bit3(0x3F2).delta()],
}
gold_collected = main_pointer >> byte(0x402)
silver_collected = main_pointer >> byte(0x403)
copper_collected = main_pointer >> byte(0x404)

diamonds_collected = main_pointer >> byte(0x405)
sapphires_collected = main_pointer >> byte(0x406)
rubies_collected = main_pointer >> byte(0x407)
amethysts_collected = main_pointer >> byte(0x408)

level_id = main_pointer >> byte(0x448)
game_state = main_pointer >> dword(0x3cc)

def map_pull(name=None, id=None):
    maps = {
        "Rolling River Creek": 0x01,
        "Bog Town": 0x02,
        "Slick Willy's River Boat": 0x03, #
        "River Town": 0x04,
        "Mushroom Valley": 0x05,
        "Fairy Town in Spring": 0x06,
        "The Tree of Knowledge": 0x07, # 
        "Fairy Town in Summer": 0x08,
        "The Cat Dragon's Lair": 0x09,
        "Fairy Town in Autumn": 0x0a,
        "The Dark Trail Ruins": 0x0b,
        "Dr. Starkenstein's Castle": 0x0c, #
        "The Catacombs": 0x0d,
        "Goblin Trail": 0x0e, # 
        "The Goblin Fort": 0x0f,
        "Joy Castle": 0x10, #
        "The Towers of Joy Castle": 0x11
    }



    if name is not None:
        return maps.get(name)
    if id is not None:
        reversed_maps = {val: name for name, val in maps.items()}
        return reversed_maps.get(id)

def coin_collection_logic():
    logic = []

    possible_multipliers = [24,16,8,80,60,40,32]
    coin_multipliers = [30,20,10,100,75,50,40]

    logic.append(main_pointer >> byte(0x494) != 0x00)

    for i, x in enumerate(range(0x492, 0x499)):
        if possible_multipliers[i] == 32:
            logic.append(remember(main_pointer >> byte(x) * possible_multipliers[i]))
        else:
            logic.append(add_source(main_pointer >> byte(x) * possible_multipliers[i]))

    for i, x in enumerate(range(0x402, 0x409)):
        logic.append(add_source(main_pointer >> byte(x) * coin_multipliers[i]))
    logic.append(value(0) >= recall())

    return logic

def purchase_logic(level):
    logic = []
    flags = shopUnlockFlagsMem.get(level)
    flagsDelta = shopUnlockFlagsDelta.get(level)
    for i, x in enumerate(flagsDelta):
        if i == 2:
            logic.append(trigger(x == 0x02))
        else:
            logic.append(add_source(x == 0x00))
    for i, x in enumerate(flags):
        if i == 2:
            logic.append(trigger(x == 0x03))
        else:
            logic.append(add_source(x == 0x01))

    return logic

def purchase_logic_all():
    logic = []
    new_index = 0
    for i, x in enumerate(range(0x01, 0x12)):
        print(new_index)
        map = map_pull(id = x)
        flagsDelta = shopUnlockFlagsDelta.get(map)
        for i, x in enumerate(flagsDelta):
            new_index += 1
            if new_index == 51:
                logic.append(x == 0x32)
            else:
                logic.append(add_source(x == 0x00))
    new_index = 0       
    for i, x in enumerate(range(0x01, 0x12)):
        map = map_pull(id = x)
        flags = shopUnlockFlagsMem.get(map)
        for i, x in enumerate(flags):
            new_index += 1
            if new_index == 51:
                logic.append(measured(x == 0x33))
            else:
                logic.append(add_source(x == 0x01))

    return logic

for i, x in enumerate(range(0x01, 0x12)):
    ach = Achievement(titles_shop(map_pull(id=x)), desc_shop(map_pull(id=x)), 10)
    logic = []
    logic.append(level_id == x)
    logic.append(purchase_logic(map_pull(id=x)))
    logic.append(coin_collection_logic())

    ach.add_core(logic)
    mySet.add_achievement(ach)

def allShop():
    allShopAch = Achievement(titles_shop("Everything"), "Purchase every item in the game", 5)
    logic = []
    logic.append(level_id > 0x00)
    logic.append(level_id < 0x12)
    logic.append(purchase_logic_all())

    allShopAch.add_core(logic)
    mySet.add_achievement(allShopAch)

allShop()

for i, x in enumerate(range(0x01, 0x12)):
    map = map_pull(id = x)
    ach = Achievement(titles_complete(map), desc_complete(map), 5)
    logic = []
    logic.append(level_id == x)
    logic.append((game_state.delta() == 0x001f97b0))
    logic.append(game_state == 0x001fc4d0)

    ach.add_core(logic)

    mySet.add_achievement(ach)

laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")
ps2Path = Path("D:\\Games\\Emulation\\Emulators\\PCSX2\\RACache\\Data")

if laptopPath.exists():
    mySet.save(laptopPath)
elif ps2Path.exists():
    mySet.save(ps2Path)
elif pcPath.exists():
    mySet.save(pcPath)
else:
    mySet.save()