import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=35609, title="Gummy Bears Minigolf")
platform = "Wii"

mask = value(0x1fffffff)
game_pointer = (dword_be(0x001992e0) & mask)
save_pointer = game_pointer >> (dword_be(0x16CC) & mask)

course = game_pointer >> dword_be(0x8A0)
world = game_pointer >> dword_be(0x8A4)
custom_hole_count = game_pointer >> dword_be(0x8EC)

coins = game_pointer >> dword_be(0xB0)

ascii_mode = (dword_be(0x0019ef58) & mask) >> (dword_be(0x00) & mask) >> (dword_be(0x00) & mask) >> (dword_be(0x00) & mask) >> dword_be(0x05)
results = ascii_mode == value(0x52455355)
in_game = ascii_mode == value(0x504c4159)
theme = ascii_mode == value(0x5049434b)
game_state = (dword_be(0x001a9690) & mask) >> dword_be(0x53c)

award_grass = save_pointer >> bit0(0xb5) #Stay on the grass!
award_swim = save_pointer >> bit1(0xb5) #Swimming Badge
award_top = save_pointer >> bit2(0xb5) #Top of the Class
award_max = save_pointer >> bit3(0xb5) #To the Max
award_ace = save_pointer >> bit0(0xb6) #Ace Shooter

award_bogey = save_pointer >> bit1(0xb6) #B for Bogey
award_designer = save_pointer >> bit2(0xb6) #Minigolf Designer
award_king = save_pointer >> bit3(0xb6) #Gummy Bear King
award_hio = save_pointer >> bit4(0xb6) #Hole in One!
award_hotshot = save_pointer >> bit5(0xb6) #Hotshot
award_on_par = save_pointer >> bit6(0xb6) #On Par!
award_par_for_course = save_pointer >> bit7(0xb6) #Par for the course!

award_fairytale_badge = save_pointer >> bit0(0xb7) #Fairytale Kingdom Badge
award_fairytale_star = save_pointer >> bit1(0xb7) #Fairytale Kingdom Star
award_adventure_badge = save_pointer >> bit2(0xb7) #Adventure Park Badge
award_adventure_star = save_pointer >> bit3(0xb7) #Adventure Park Star
award_rainbow_badge = save_pointer >> bit4(0xb7) #Rainbow City Badge
award_rainbow_star = save_pointer >> bit5(0xb7) #Rainbow City Star
award_candyland_badge = save_pointer >> bit6(0xb7) #Candy Land Badge
award_candyland_star = save_pointer >> bit7(0xb7) #Candy Land Star

prog = {
    "fairytale": (award_fairytale_star, "In Love With a Fairytale", "Earn the \"Fairytale Kingdom Star\" award by finishing the \"Fairytale\" course within par", 2),
    "adventure": (award_adventure_star, "Adventure Is Out There!", "Earn the \"Adventure Park Star\" award by finishing the \"Adventure Park\" course within par", 2),
    "rainbow": (award_rainbow_star,     "Rainbow Road", "Earn the \"Rainbow City Star\" award by finishing the \"Rainbow City\" course within par", 3),
    "candyland": (award_candyland_star, "Take You to the Candy Shop", "Earn the \"Candy Land Star\" award by finishing the \"Candyland\" course within par", 5)
}

awards = {
    "fairytale": (award_fairytale_badge, "Happily Gummy After", "Earn the \"Fairytale Kingdom Badge\" award by completing the \"Fairytale\" course", 1),
    "adventure": (award_adventure_badge, "Adventuring Through the Park", "Earn the \"Adventure Park Badge\" award by finishing the \"Adventure Park\" course", 1),
    "rainbow": (award_rainbow_badge, "Sunshine and Rainbows", "Earn the \"Rainbow City Badge\" badge by finishing the \"Rainbow City\" course", 2),
    "candyland": (award_candyland_badge, "The Candy Man Can", "Earn the \"Candy Land Badge\" award by completing the \"Candyland\" course", 3),
    "ace": (award_ace, "All Aces", "Earn the \"Ace Shooter\" award by scoring 20 hole in ones", 3),
    "bogey": (award_bogey, "Bogey Wonderland", "Earn the \"B for Bogey\" award by finishing a hole with a bogey", 1),
    "designer":    (award_designer, "Designer Fashion", "Earn the \"Minigolf Designer\" award by designing a Custom Course", 1),
    "hio":    (award_hio, "Score!", "Earn the \"Hole in One!\" award by scoring a hole in one", 1),
    "hotshot":    (award_hotshot, "Hot Shots... Golf?", "Earn the \"Hotshot\" award by scoring 5 hole in ones", 3),
    "on_par":    (award_on_par, "Not Bad", "Earn the \"On Par!\" award by completing any area on par in the Courses mode", 1),
    "par_for_course":    (award_par_for_course, "Average Joe", "Earn the \"Par for the course!\" award by scoring par on any Quick Game hole", 1),
    "grass":    (award_grass, "Fore!", "Earn the \"Stay on the grass!\" award by hitting 5 shots out of bounds in a single hole", 1),
    "swim":    (award_swim, "I Can't Swim!", "Earn the \"Swimming Badge\" award by hitting the ball into a water hazard 5 times", 1),
    "top":    (award_top, "Class Pet", "Earn the \"Top of the Class\" award by scoring 10 hole in ones", 5),


}

custom_holes = {
    0: ("The Hole-y Trinity", "Complete any custom 3 hole course", 2),
    1: ("Six Shooter", "Complete any custom 6 hole course", 3),
    2: ("Nine, Nine, Nine!", "Complete any custom 9 hole course", 5),
}



for area, (award, title, desc, points) in prog.items():
    ach = Achievement(title, desc, points)
    logic = [
        game_pointer >> dword_be(0x16cc) == delta(dword_be(0x16cc)),
        in_game,
        delta(award) == 0,
        award == 1
    ]

    ach.add_core(logic)
    mySet.add_achievement(ach)


for area, (award, title, desc, points) in awards.items():
    ach = Achievement(title, desc, points)
    logic = [
        game_pointer >> dword_be(0x16cc) == delta(dword_be(0x16cc)),
        in_game,
        delta(award) == 0,
        award == 1
    ]

    ach.add_core(logic)
    mySet.add_achievement(ach)

for x, (title, desc, points) in enumerate(custom_holes.values()):
    ach = Achievement(title, desc, points)
    logic = [
        and_next(world >= 0x04),
        custom_hole_count == x,
    ]
    for y in range((x + 1) * 3):
        logic.append(and_next(results))
        logic.append((course == y).with_hits(1))
    logic.append(reset_if(theme))

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
 