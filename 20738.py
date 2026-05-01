import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=20738, title="Scaler")
platform = "PS2"

levels = [
"Chimerum",
"Bakuldo",
"Klonium",
"Altus",
"Desollem",
"Koradus",
"Medoozum",
"Iridium",
"Voidrem",
"Komoldo"
]

current_level = dword(0x0045b79c)
ending_check = dword_be(0x004276ef)
class SaveData:

    def __init__(self):
        pass

    def crystal_gem(self, level: str):
 
        gem_addresses = ["0x0045ba4f", # Chimerum 1-8  (bit0 - bit7)
                        "0x0045ba50",  # Chimerum 9-10 (bit0 - bit1) | Bakuldo 1-6  (bit2 - bit7)
                        "0x0045ba51",  # Bakuldo  7-10 (bit0 - bit3) | Klonium 1-4  (bit4 - bit7)
                        "0x0045ba52",  # Klonium  5-10 (bit0 - bit5) | Altus   1-2  (bit6 - bit7)
                        "0x0045ba53",  # Altus    3-10 (bit0 - bit7)
                        "0x0045ba54",  # Desollem 1-8  (bit0 - bit7)
                        "0x0045ba55",  # Desollem 9-10 (bit0 - bit1) | Koradus 1-6  (bit2 - bit7)
                        "0x0045ba56",  # Koradus  7-10 (bit0 - bit3) | Medoozum 1-4 (bit4 - bit7)
                        "0x0045ba57",  # Medoozum 5-10 (bit0 - bit5) | Iridium 1-2  (bit6 - bit7)
                        "0x0045ba58",  # Iridium  3-10 (bit0 - bit7)
                        "0x0045ba59",  # Voidrem  1-8  (bit0 - bit7)
                        "0x0045ba5a",  # Voidrem  9-10 (bit0 - bit1) | Komoldo 1-6  (bit2 - bit7)
                        "0x0045ba5b"]  # Komoldo  7-10 (bit0 - bit3)
        
        area_bits = {
            "Chimerum": {}, "Bakuldo":  {}, "Klonium":  {}, "Altus":    {},
            "Desollem": {}, "Koradus":  {}, "Medoozum": {}, "Iridium":  {},
            "Voidrem":  {}, "Komoldo":  {},
        }
    
        for x in gem_addresses:
            addr = int(x, 16)
            match addr:

                # 0x0045ba4f : Chimerum 1-8 (bit0-bit7)
                case 0x0045ba4f:
                    area_bits["Chimerum"][1]  = (lambda _x=addr: bit0(_x))
                    area_bits["Chimerum"][2]  = (lambda _x=addr: bit1(_x))
                    area_bits["Chimerum"][3]  = (lambda _x=addr: bit2(_x))
                    area_bits["Chimerum"][4]  = (lambda _x=addr: bit3(_x))
                    area_bits["Chimerum"][5]  = (lambda _x=addr: bit4(_x))
                    area_bits["Chimerum"][6]  = (lambda _x=addr: bit5(_x))
                    area_bits["Chimerum"][7]  = (lambda _x=addr: bit6(_x))
                    area_bits["Chimerum"][8]  = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba50 : Chimerum 9-10 (bit0-bit1) | Bakuldo 1-6 (bit2-bit7)
                case 0x0045ba50:
                    area_bits["Chimerum"][9]  = (lambda _x=addr: bit0(_x))
                    area_bits["Chimerum"][10] = (lambda _x=addr: bit1(_x))
                    area_bits["Bakuldo"][1]   = (lambda _x=addr: bit2(_x))
                    area_bits["Bakuldo"][2]   = (lambda _x=addr: bit3(_x))
                    area_bits["Bakuldo"][3]   = (lambda _x=addr: bit4(_x))
                    area_bits["Bakuldo"][4]   = (lambda _x=addr: bit5(_x))
                    area_bits["Bakuldo"][5]   = (lambda _x=addr: bit6(_x))
                    area_bits["Bakuldo"][6]   = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba51 : Bakuldo 7-10 (bit0-bit3) | Klonium 1-4 (bit4-bit7)
                case 0x0045ba51:
                    area_bits["Bakuldo"][7]   = (lambda _x=addr: bit0(_x))
                    area_bits["Bakuldo"][8]   = (lambda _x=addr: bit1(_x))
                    area_bits["Bakuldo"][9]   = (lambda _x=addr: bit2(_x))
                    area_bits["Bakuldo"][10]  = (lambda _x=addr: bit3(_x))
                    area_bits["Klonium"][1]   = (lambda _x=addr: bit4(_x))
                    area_bits["Klonium"][2]   = (lambda _x=addr: bit5(_x))
                    area_bits["Klonium"][3]   = (lambda _x=addr: bit6(_x))
                    area_bits["Klonium"][4]   = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba52 : Klonium 5-10 (bit0-bit5) | Altus 1-2 (bit6-bit7)
                case 0x0045ba52:
                    area_bits["Klonium"][5]   = (lambda _x=addr: bit0(_x))
                    area_bits["Klonium"][6]   = (lambda _x=addr: bit1(_x))
                    area_bits["Klonium"][7]   = (lambda _x=addr: bit2(_x))
                    area_bits["Klonium"][8]   = (lambda _x=addr: bit3(_x))
                    area_bits["Klonium"][9]   = (lambda _x=addr: bit4(_x))
                    area_bits["Klonium"][10]  = (lambda _x=addr: bit5(_x))
                    area_bits["Altus"][1]     = (lambda _x=addr: bit6(_x))
                    area_bits["Altus"][2]     = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba53 : Altus 3-10 (bit0-bit7)
                case 0x0045ba53:
                    area_bits["Altus"][3]     = (lambda _x=addr: bit0(_x))
                    area_bits["Altus"][4]     = (lambda _x=addr: bit1(_x))
                    area_bits["Altus"][5]     = (lambda _x=addr: bit2(_x))
                    area_bits["Altus"][6]     = (lambda _x=addr: bit3(_x))
                    area_bits["Altus"][7]     = (lambda _x=addr: bit4(_x))
                    area_bits["Altus"][8]     = (lambda _x=addr: bit5(_x))
                    area_bits["Altus"][9]     = (lambda _x=addr: bit6(_x))
                    area_bits["Altus"][10]    = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba54 : Desollem 1-8 (bit0-bit7)
                case 0x0045ba54:
                    area_bits["Desollem"][1]  = (lambda _x=addr: bit0(_x))
                    area_bits["Desollem"][2]  = (lambda _x=addr: bit1(_x))
                    area_bits["Desollem"][3]  = (lambda _x=addr: bit2(_x))
                    area_bits["Desollem"][4]  = (lambda _x=addr: bit3(_x))
                    area_bits["Desollem"][5]  = (lambda _x=addr: bit4(_x))
                    area_bits["Desollem"][6]  = (lambda _x=addr: bit5(_x))
                    area_bits["Desollem"][7]  = (lambda _x=addr: bit6(_x))
                    area_bits["Desollem"][8]  = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba55 : Desollem 9-10 (bit0-bit1) | Koradus 1-6 (bit2-bit7)
                case 0x0045ba55:
                    area_bits["Desollem"][9]  = (lambda _x=addr: bit0(_x))
                    area_bits["Desollem"][10] = (lambda _x=addr: bit1(_x))
                    area_bits["Koradus"][1]   = (lambda _x=addr: bit2(_x))
                    area_bits["Koradus"][2]   = (lambda _x=addr: bit3(_x))
                    area_bits["Koradus"][3]   = (lambda _x=addr: bit4(_x))
                    area_bits["Koradus"][4]   = (lambda _x=addr: bit5(_x))
                    area_bits["Koradus"][5]   = (lambda _x=addr: bit6(_x))
                    area_bits["Koradus"][6]   = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba56 : Koradus 7-10 (bit0-bit3) | Medoozum 1-4 (bit4-bit7)
                case 0x0045ba56:
                    area_bits["Koradus"][7]   = (lambda _x=addr: bit0(_x))
                    area_bits["Koradus"][8]   = (lambda _x=addr: bit1(_x))
                    area_bits["Koradus"][9]   = (lambda _x=addr: bit2(_x))
                    area_bits["Koradus"][10]  = (lambda _x=addr: bit3(_x))
                    area_bits["Medoozum"][1]  = (lambda _x=addr: bit4(_x))
                    area_bits["Medoozum"][2]  = (lambda _x=addr: bit5(_x))
                    area_bits["Medoozum"][3]  = (lambda _x=addr: bit6(_x))
                    area_bits["Medoozum"][4]  = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba57 : Medoozum 5-10 (bit0-bit5) | Iridium 1-2 (bit6-bit7)
                case 0x0045ba57:
                    area_bits["Medoozum"][5]  = (lambda _x=addr: bit0(_x))
                    area_bits["Medoozum"][6]  = (lambda _x=addr: bit1(_x))
                    area_bits["Medoozum"][7]  = (lambda _x=addr: bit2(_x))
                    area_bits["Medoozum"][8]  = (lambda _x=addr: bit3(_x))
                    area_bits["Medoozum"][9]  = (lambda _x=addr: bit4(_x))
                    area_bits["Medoozum"][10] = (lambda _x=addr: bit5(_x))
                    area_bits["Iridium"][1]   = (lambda _x=addr: bit6(_x))
                    area_bits["Iridium"][2]   = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba58 : Iridium 3-10 (bit0-bit7)
                case 0x0045ba58:
                    area_bits["Iridium"][3]   = (lambda _x=addr: bit0(_x))
                    area_bits["Iridium"][4]   = (lambda _x=addr: bit1(_x))
                    area_bits["Iridium"][5]   = (lambda _x=addr: bit2(_x))
                    area_bits["Iridium"][6]   = (lambda _x=addr: bit3(_x))
                    area_bits["Iridium"][7]   = (lambda _x=addr: bit4(_x))
                    area_bits["Iridium"][8]   = (lambda _x=addr: bit5(_x))
                    area_bits["Iridium"][9]   = (lambda _x=addr: bit6(_x))
                    area_bits["Iridium"][10]  = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba59 : Voidrem 1-8 (bit0-bit7)
                case 0x0045ba59:
                    area_bits["Voidrem"][1]   = (lambda _x=addr: bit0(_x))
                    area_bits["Voidrem"][2]   = (lambda _x=addr: bit1(_x))
                    area_bits["Voidrem"][3]   = (lambda _x=addr: bit2(_x))
                    area_bits["Voidrem"][4]   = (lambda _x=addr: bit3(_x))
                    area_bits["Voidrem"][5]   = (lambda _x=addr: bit4(_x))
                    area_bits["Voidrem"][6]   = (lambda _x=addr: bit5(_x))
                    area_bits["Voidrem"][7]   = (lambda _x=addr: bit6(_x))
                    area_bits["Voidrem"][8]   = (lambda _x=addr: bit7(_x))
                
                # 0x0045ba5a : Voidrem 9-10 (bit0-bit1) | Komoldo 1-6 (bit2-bit7)
                case 0x0045ba5a:
                    area_bits["Voidrem"][9]   = (lambda _x=addr: bit0(_x))
                    area_bits["Voidrem"][10]  = (lambda _x=addr: bit1(_x))
                    area_bits["Komoldo"][1]   = (lambda _x=addr: bit2(_x))
                    area_bits["Komoldo"][2]   = (lambda _x=addr: bit3(_x))
                    area_bits["Komoldo"][3]   = (lambda _x=addr: bit4(_x))
                    area_bits["Komoldo"][4]   = (lambda _x=addr: bit5(_x))
                    area_bits["Komoldo"][5]   = (lambda _x=addr: bit6(_x))
                    area_bits["Komoldo"][6]   = (lambda _x=addr: bit7(_x))
    
                
                # 0x0045ba5b : Komoldo 7-10 (bit0-bit3)
                case 0x0045ba5b:
                    area_bits["Komoldo"][7]   = (lambda _x=addr: bit0(_x))
                    area_bits["Komoldo"][8]   = (lambda _x=addr: bit1(_x))
                    area_bits["Komoldo"][9]   = (lambda _x=addr: bit2(_x))
                    area_bits["Komoldo"][10]  = (lambda _x=addr: bit3(_x))
    
        key = level.strip().title()
        return area_bits.get(key)
    
    def shop_purchases(self, level: str):
 
        shop_addresses = ["0x0045ba90",
                        "0x0045ba91", 
                        "0x0045ba92", 
                        "0x0045ba93", 
        ]
        
        shop_bits = {
            "Health": {}, "Bombs":  {}, "Claws":  {}, "EBombs": {},
            "Freeze": {}, "Camouflage":  {}
        }
    
        for x in shop_addresses:
            addr = int(x, 16)
            match addr:

                # 0x0045ba4f : Chimerum 1-8 (bit0-bit7)
                case 0x0045ba90:
                    shop_bits["Camouflage"][1]  = (lambda _x=addr: bit1(_x))
                    shop_bits["Camouflage"][2]  = (lambda _x=addr: bit2(_x))
                    shop_bits["Camouflage"][3]  = (lambda _x=addr: bit3(_x))
                    shop_bits["Claws"][1]  = (lambda _x=addr: bit4(_x))
                    shop_bits["Claws"][2]  = (lambda _x=addr: bit5(_x))
                    shop_bits["Freeze"][1]  = (lambda _x=addr: bit6(_x))
                    shop_bits["EBombs"][1]  = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba50 : Chimerum 9-10 (bit0-bit1) | Bakuldo 1-6 (bit2-bit7)
                case 0x0045ba91:
                    shop_bits["EBombs"][2]  = (lambda _x=addr: bit0(_x))
    
                # 0x0045ba51 : Bakuldo 7-10 (bit0-bit3) | Klonium 1-4 (bit4-bit7)
                case 0x0045ba92:
                    shop_bits["Health"][1]   = (lambda _x=addr: bit6(_x))
                    shop_bits["Health"][2]   = (lambda _x=addr: bit7(_x))
    
                # 0x0045ba52 : Klonium 5-10 (bit0-bit5) | Altus 1-2 (bit6-bit7)
                case 0x0045ba93:
                    shop_bits["Health"][3]   = (lambda _x=addr: bit0(_x))
                    shop_bits["Bombs"][1]   = (lambda _x=addr: bit1(_x))
                    shop_bits["Bombs"][2]   = (lambda _x=addr: bit2(_x))
                    shop_bits["Bombs"][3]   = (lambda _x=addr: bit3(_x))
                    shop_bits["Bombs"][4]   = (lambda _x=addr: bit4(_x))
    

        return shop_bits.get(level.strip())


crystal_gems = {
    "Chimerum": ("Chimerum", "Collect all 10 Crystal Gems in Chimerum"),
    "Bakuldo":  ("Bakuldo", "Collect all 10 Crystal Gems in Bakuldo"),
    "Klonium":  ("Klonium", "Collect all 10 Crystal Gems in Klonium"),
    "Altus":    ("Altus", "Collect all 10 Crystal Gems in Altus"),
    "Desollem": ("Desollem", "Collect all 10 Crystal Gems in Desollem"),
    "Koradus":  ("Koradus", "Collect all 10 Crystal Gems in Koradus"),
    "Medoozum": ("Medoozum", "Collect all 10 Crystal Gems in Medoozum"),
    "Iridium":  ("Iridium", "Collect all 10 Crystal Gems in Iridium"),
    "Voidrem":  ("Voidrem", "Collect all 10 Crystal Gems in Voidrem"),
    "Komoldo":  ("Komoldo", "Collect all 10 Crystal Gems in Komoldo")
}

shop_items = {
    "Health":         ("Extra Heart Points", "Purchase every Extra Heart Point", 3),
    "Bombs":          ("Bomb Containers", "Purchase every Bomb Container", 4),
    "Claws":          ("Claws", "Purchase the Iron Claws and the Steel Claws", 2),
    "EBombs":         ("Bombs", "Purchase the Electric Bomb Blast and the Electric Bomb Mega-Blast", 2),
    "Freeze":         ("Freeze", "Purchase Freeze Mode", 1),
    "Camouflage":     ("Camouflages", "Purchase the both of the Extra Camouflages", 3),
}


data = SaveData()

def gemCheevos():
    for level_idx, level in enumerate(levels):
        logic = []
        logic.append(measured_if(current_level == level_idx))

        gem_entries = list(data.crystal_gem(level).items())
        last_idx = len(gem_entries) - 1

        for i, (idx, fn) in enumerate(gem_entries):
            bit = fn()
            if i == last_idx:
                logic.append(bit.delta() == 0x09)          # last: no flag
            else:
                logic.append(add_source(bit.delta()))

        for i, (idx, fn) in enumerate(gem_entries):
            bit = fn()
            if i == last_idx:
                logic.append(measured(bit == 0x0a))        # last: measured
            else:
                logic.append(add_source(bit))

        title, description = crystal_gems[level]
        ach = Achievement(title, description, points=5)
        print(logic)
        print("\n")
        ach.add_core(logic)
        mySet.add_achievement(ach)

def shopCheevos():
    for key, (title, description, count) in shop_items.items():
        logic = []

        shop_entries = list(data.shop_purchases(key).items())
        last_idx = len(shop_entries) - 1

        logic.append(current_level < 0x10)
        for i, (idx, fn) in enumerate(shop_entries):
            bit = fn()
            if i == last_idx:
                logic.append(bit.delta() == (count - 1))
            else:
                logic.append(add_source(bit.delta()))

        for i, (idx, fn) in enumerate(shop_entries):
            bit = fn()
            if i == last_idx:
                logic.append(bit == count)       # count from shop_items tuple
            else:
                logic.append(add_source(bit))

        ach = Achievement(title, description, points=5)
        print(logic)
        print("\n")
        ach.add_core(logic)
        mySet.add_achievement(ach)

def hiddenEnding():
        logic = []

        logic.append(ending_check.delta() == 0x454e4447)
        logic.append(ending_check == 0x414c4c47)

        ach = Achievement("Cheesy Ending", "View the alternate ending by collecting all 100 Crystal Gems", points=5)
        print(logic)
        print("\n")
        ach.add_core(logic)
        mySet.add_achievement(ach)
    
gemCheevos()
shopCheevos()
hiddenEnding()

dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
pcsx2Path = Path("D:\\Games\\Emulation\\Emulators\\PCSX2\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

match platform:
    case "Wii":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case "PS2":
        if pcsx2Path.exists():
            mySet.save(pcsx2Path)
    case default:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()