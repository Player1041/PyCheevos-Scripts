import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path

mySet = AchievementSet(game_id=35163, title="Grey's Anatomy")
platform = "Wii"

ep2_prog = {
    1: ("ep2 | act 1 complete", "Complete Ep2 - Act 1", 3),
    2: ("ep2 | act 2 complete", "Complete Ep2 - Act 2", 3),
    3: ("ep2 | act 3 complete", "Complete Ep2 - Act 3", 3),
    4: ("ep2 | act 4 complete", "Complete Ep2 - Act 4", 3),
    5: ("ep2 | act 5 complete", "Complete Ep2 - Act 5", 3),
    6: ("ep2 | act 6 complete", "Complete Ep2 - Act 6", 3),
}

ep2_cos = {
    1: ("ep2 | act 1 complete - chief", "Complete Ep2 - Act 1 with a chief of surgery rank", 3),
    2: ("ep2 | act 2 complete - chief", "Complete Ep2 - Act 2 with a chief of surgery rank", 3),
    3: ("ep2 | act 3 complete - chief", "Complete Ep2 - Act 3 with a chief of surgery rank", 3),
    4: ("ep2 | act 4 complete - chief", "Complete Ep2 - Act 4 with a chief of surgery rank", 3),
    5: ("ep2 | act 5 complete - chief", "Complete Ep2 - Act 5 with a chief of surgery rank", 3),
    6: ("ep2 | act 6 complete - chief", "Complete Ep2 - Act 6 with a chief of surgery rank", 3),
}

game_pointer = dword_be(0x00556128)
loaded_save = game_pointer >> byte(0x60)

def hearts(episode, act, scene, delta=False, heart_count=0, cmp="=="):
    def b(n, addr):
        v = bit0(addr) if n == 0 else bit1(addr) if n == 1 else bit2(addr) if n == 2 else bit3(addr) if n == 3 else bit4(addr) if n == 4 else bit5(addr) if n == 5 else bit6(addr) if n == 6 else bit7(addr)
        return v.delta() if delta else v
    episodes = {
        1: {
            '1': {
                1: [game_pointer >> add_source(b(7, 0x18)), game_pointer >> add_source(b(6, 0x18)), game_pointer >> b(5, 0x18) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x18)), game_pointer >> add_source(b(3, 0x18)), game_pointer >> b(2, 0x18) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x18)), game_pointer >> add_source(b(0, 0x18)), game_pointer >> b(7, 0x19) == heart_count],
                4: [game_pointer >> add_source(b(6, 0x19)), game_pointer >> add_source(b(5, 0x19)), game_pointer >> b(4, 0x19) == heart_count],
                5: [game_pointer >> add_source(b(3, 0x19)), game_pointer >> add_source(b(2, 0x19)), game_pointer >> b(1, 0x19) == heart_count],
            },
            '2': {
                1: [game_pointer >> add_source(b(0, 0x19)), game_pointer >> add_source(b(7, 0x1A)), game_pointer >> b(6, 0x1A) == heart_count],
                2: [game_pointer >> add_source(b(5, 0x1A)), game_pointer >> add_source(b(4, 0x1A)), game_pointer >> b(3, 0x1A) == heart_count],
                3: [game_pointer >> add_source(b(2, 0x1A)), game_pointer >> add_source(b(1, 0x1A)), game_pointer >> b(0, 0x1A) == heart_count],
                4: [game_pointer >> add_source(b(7, 0x1B)), game_pointer >> add_source(b(6, 0x1B)), game_pointer >> b(5, 0x1B) == heart_count],
                5: [game_pointer >> add_source(b(4, 0x1B)), game_pointer >> add_source(b(3, 0x1B)), game_pointer >> b(2, 0x1B) == heart_count],
                6: [game_pointer >> add_source(b(1, 0x1B)), game_pointer >> add_source(b(0, 0x1B)), game_pointer >> b(7, 0x1C) == heart_count],
            },
            '3': {
                1: [game_pointer >> add_source(b(6, 0x1C)), game_pointer >> add_source(b(5, 0x1C)), game_pointer >> b(4, 0x1C) == heart_count],
                2: [game_pointer >> add_source(b(3, 0x1C)), game_pointer >> add_source(b(2, 0x1C)), game_pointer >> b(1, 0x1C) == heart_count],
                3: [game_pointer >> add_source(b(0, 0x1C)), game_pointer >> add_source(b(7, 0x1D)), game_pointer >> b(6, 0x1D) == heart_count],
                4: [game_pointer >> add_source(b(5, 0x1D)), game_pointer >> add_source(b(4, 0x1D)), game_pointer >> b(3, 0x1D) == heart_count],
                5: [game_pointer >> add_source(b(2, 0x1D)), game_pointer >> add_source(b(1, 0x1D)), game_pointer >> b(0, 0x1D) == heart_count],
            }, 
            '4': {
                1: [game_pointer >> add_source(b(7, 0x1E)), game_pointer >> add_source(b(6, 0x1E)), game_pointer >> b(5, 0x1E) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x1E)), game_pointer >> add_source(b(3, 0x1E)), game_pointer >> b(2, 0x1E) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x1E)), game_pointer >> add_source(b(0, 0x1E)), game_pointer >> b(7, 0x1F) == heart_count],
                4: [game_pointer >> add_source(b(6, 0x1F)), game_pointer >> add_source(b(5, 0x1F)), game_pointer >> b(4, 0x1F) == heart_count],
                5: [game_pointer >> add_source(b(3, 0x1F)), game_pointer >> add_source(b(2, 0x1F)), game_pointer >> b(1, 0x1F) == heart_count],
                6: [game_pointer >> add_source(b(0, 0x1F)), game_pointer >> add_source(b(7, 0x20)), game_pointer >> b(6, 0x20) == heart_count],
            },
            '5': {
                1: [game_pointer >> add_source(b(5, 0x20)), game_pointer >> add_source(b(4, 0x20)), game_pointer >> b(3, 0x20) == heart_count],
                2: [game_pointer >> add_source(b(2, 0x20)), game_pointer >> add_source(b(1, 0x20)), game_pointer >> b(0, 0x20) == heart_count],
                3: [game_pointer >> add_source(b(7, 0x21)), game_pointer >> add_source(b(6, 0x21)), game_pointer >> b(5, 0x21) == heart_count],
                4: [game_pointer >> add_source(b(4, 0x21)), game_pointer >> add_source(b(3, 0x21)), game_pointer >> b(2, 0x21) == heart_count],
                5: [game_pointer >> add_source(b(1, 0x21)), game_pointer >> add_source(b(0, 0x21)), game_pointer >> b(7, 0x22) == heart_count],
                6: [game_pointer >> add_source(b(6, 0x22)), game_pointer >> add_source(b(5, 0x22)), game_pointer >> b(4, 0x22) == heart_count],
            },
            '6': {
                1: [game_pointer >> add_source(b(3, 0x22)), game_pointer >> add_source(b(2, 0x22)), game_pointer >> b(1, 0x22) == heart_count],
                2: [game_pointer >> add_source(b(0, 0x22)), game_pointer >> add_source(b(7, 0x23)), game_pointer >> b(6, 0x23) == heart_count],
                3: [game_pointer >> add_source(b(5, 0x23)), game_pointer >> add_source(b(4, 0x23)), game_pointer >> b(3, 0x23) == heart_count],
                4: [game_pointer >> add_source(b(2, 0x23)), game_pointer >> add_source(b(1, 0x23)), game_pointer >> b(0, 0x23) == heart_count],
                5: [game_pointer >> add_source(b(7, 0x24)), game_pointer >> add_source(b(6, 0x24)), game_pointer >> b(5, 0x24) == heart_count],
                6: [game_pointer >> add_source(b(4, 0x24)), game_pointer >> add_source(b(3, 0x24)), game_pointer >> b(2, 0x24) == heart_count],
            },
        },
        2: {
            '1': {
                1: [game_pointer >> add_source(b(1, 0x24)), game_pointer >> add_source(b(0, 0x24)), game_pointer >> b(7, 0x25) == heart_count],
                2: [game_pointer >> add_source(b(6, 0x25)), game_pointer >> add_source(b(5, 0x25)), game_pointer >> b(4, 0x25) == heart_count],
                3: [game_pointer >> add_source(b(3, 0x25)), game_pointer >> add_source(b(2, 0x25)), game_pointer >> b(1, 0x25) == heart_count],
                4: [game_pointer >> add_source(b(0, 0x25)), game_pointer >> add_source(b(7, 0x26)), game_pointer >> b(6, 0x26) == heart_count],
                5: [game_pointer >> add_source(b(5, 0x26)), game_pointer >> add_source(b(4, 0x26)), game_pointer >> b(3, 0x26) == heart_count],
            },
            '2': {
                1: [game_pointer >> add_source(b(2, 0x26)), game_pointer >> add_source(b(1, 0x26)), game_pointer >> b(0, 0x26) == heart_count],
                2: [game_pointer >> add_source(b(7, 0x27)), game_pointer >> add_source(b(6, 0x27)), game_pointer >> b(5, 0x27) == heart_count],
                3: [game_pointer >> add_source(b(4, 0x27)), game_pointer >> add_source(b(3, 0x27)), game_pointer >> b(2, 0x27) == heart_count],
            },
            '3': {
                1: [game_pointer >> add_source(b(1, 0x27)), game_pointer >> add_source(b(0, 0x27)), game_pointer >> b(7, 0x28) == heart_count],
                2: [game_pointer >> add_source(b(6, 0x28)), game_pointer >> add_source(b(5, 0x28)), game_pointer >> b(4, 0x28) == heart_count],
                3: [game_pointer >> add_source(b(3, 0x28)), game_pointer >> add_source(b(2, 0x28)), game_pointer >> b(1, 0x28) == heart_count],
            },
            '4': {
                1: [game_pointer >> add_source(b(0, 0x28)), game_pointer >> add_source(b(7, 0x29)), game_pointer >> b(6, 0x29) == heart_count],
                2: [game_pointer >> add_source(b(5, 0x29)), game_pointer >> add_source(b(4, 0x29)), game_pointer >> b(3, 0x29) == heart_count],
                3: [game_pointer >> add_source(b(2, 0x29)), game_pointer >> add_source(b(1, 0x29)), game_pointer >> b(0, 0x29) == heart_count],
            },
            '5': {
                1: [game_pointer >> add_source(b(7, 0x2A)), game_pointer >> add_source(b(6, 0x2A)), game_pointer >> b(5, 0x2A) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x2A)), game_pointer >> add_source(b(3, 0x2A)), game_pointer >> b(2, 0x2A) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x2A)), game_pointer >> add_source(b(0, 0x2A)), game_pointer >> b(7, 0x2B) == heart_count],
                4: [game_pointer >> add_source(b(6, 0x2B)), game_pointer >> add_source(b(5, 0x2B)), game_pointer >> b(4, 0x2B) == heart_count],
            },
            '6': {
                1: [game_pointer >> add_source(b(3, 0x2B)), game_pointer >> add_source(b(2, 0x2B)), game_pointer >> b(1, 0x2B) == heart_count],
                2: [game_pointer >> add_source(b(0, 0x2B)), game_pointer >> add_source(b(7, 0x2C)), game_pointer >> b(6, 0x2C) == heart_count],
                3: [game_pointer >> add_source(b(5, 0x2C)), game_pointer >> add_source(b(4, 0x2C)), game_pointer >> b(3, 0x2C) == heart_count],
                4: [game_pointer >> add_source(b(2, 0x2C)), game_pointer >> add_source(b(1, 0x2C)), game_pointer >> b(0, 0x2C) == heart_count],
                5: [game_pointer >> add_source(b(7, 0x2D)), game_pointer >> add_source(b(6, 0x2D)), game_pointer >> b(5, 0x2D) == heart_count],
            },
        },
        3: {
            '1': {
                1: [game_pointer >> add_source(b(4, 0x2D)), game_pointer >> add_source(b(3, 0x2D)), game_pointer >> b(2, 0x2D) == heart_count],
                2: [game_pointer >> add_source(b(1, 0x2D)), game_pointer >> add_source(b(0, 0x2D)), game_pointer >> b(7, 0x2E) == heart_count],
                3: [game_pointer >> add_source(b(6, 0x2E)), game_pointer >> add_source(b(5, 0x2E)), game_pointer >> b(4, 0x2E) == heart_count],
                4: [game_pointer >> add_source(b(3, 0x2E)), game_pointer >> add_source(b(2, 0x2E)), game_pointer >> b(1, 0x2E) == heart_count],
                5: [game_pointer >> add_source(b(0, 0x2E)), game_pointer >> add_source(b(7, 0x2F)), game_pointer >> b(6, 0x2F) == heart_count],
                6: [game_pointer >> add_source(b(5, 0x2F)), game_pointer >> add_source(b(4, 0x2F)), game_pointer >> b(3, 0x2F) == heart_count],
            },
            '2': {
                1: [game_pointer >> add_source(b(2, 0x2F)), game_pointer >> add_source(b(1, 0x2F)), game_pointer >> b(0, 0x2F) == heart_count],
                2: [game_pointer >> add_source(b(7, 0x30)), game_pointer >> add_source(b(6, 0x30)), game_pointer >> b(5, 0x30) == heart_count],
                3: [game_pointer >> add_source(b(4, 0x30)), game_pointer >> add_source(b(3, 0x30)), game_pointer >> b(2, 0x30) == heart_count],
                4: [game_pointer >> add_source(b(1, 0x30)), game_pointer >> add_source(b(0, 0x30)), game_pointer >> b(7, 0x31) == heart_count],
                5: [game_pointer >> add_source(b(6, 0x31)), game_pointer >> add_source(b(5, 0x31)), game_pointer >> b(4, 0x31) == heart_count],
            },
            '3': {
                1: [game_pointer >> add_source(b(3, 0x31)), game_pointer >> add_source(b(2, 0x31)), game_pointer >> b(1, 0x31) == heart_count],
                2: [game_pointer >> add_source(b(0, 0x31)), game_pointer >> add_source(b(7, 0x32)), game_pointer >> b(6, 0x32) == heart_count],
                3: [game_pointer >> add_source(b(5, 0x32)), game_pointer >> add_source(b(4, 0x32)), game_pointer >> b(3, 0x32) == heart_count],
                4: [game_pointer >> add_source(b(2, 0x32)), game_pointer >> add_source(b(1, 0x32)), game_pointer >> b(0, 0x32) == heart_count],
            },
            '4': {
                1: [game_pointer >> add_source(b(7, 0x33)), game_pointer >> add_source(b(6, 0x33)), game_pointer >> b(5, 0x33) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x33)), game_pointer >> add_source(b(3, 0x33)), game_pointer >> b(2, 0x33) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x33)), game_pointer >> add_source(b(0, 0x33)), game_pointer >> b(7, 0x34) == heart_count],
                4: [game_pointer >> add_source(b(6, 0x34)), game_pointer >> add_source(b(5, 0x34)), game_pointer >> b(4, 0x34) == heart_count],
                5: [game_pointer >> add_source(b(3, 0x34)), game_pointer >> add_source(b(2, 0x34)), game_pointer >> b(1, 0x34) == heart_count],
            },
            '5': {
                1: [game_pointer >> add_source(b(0, 0x34)), game_pointer >> add_source(b(7, 0x35)), game_pointer >> b(6, 0x35) == heart_count],
                2: [game_pointer >> add_source(b(5, 0x35)), game_pointer >> add_source(b(4, 0x35)), game_pointer >> b(3, 0x35) == heart_count],
                3: [game_pointer >> add_source(b(2, 0x35)), game_pointer >> add_source(b(1, 0x35)), game_pointer >> b(0, 0x35) == heart_count],
                4: [game_pointer >> add_source(b(7, 0x36)), game_pointer >> add_source(b(6, 0x36)), game_pointer >> b(5, 0x36) == heart_count],
            },
            '6': {
                1: [game_pointer >> add_source(b(4, 0x36)), game_pointer >> add_source(b(3, 0x36)), game_pointer >> b(2, 0x36) == heart_count],
                2: [game_pointer >> add_source(b(1, 0x36)), game_pointer >> add_source(b(0, 0x36)), game_pointer >> b(7, 0x37) == heart_count],
                3: [game_pointer >> add_source(b(6, 0x37)), game_pointer >> add_source(b(5, 0x37)), game_pointer >> b(4, 0x37) == heart_count],
                4: [game_pointer >> add_source(b(3, 0x37)), game_pointer >> add_source(b(2, 0x37)), game_pointer >> b(1, 0x37) == heart_count],
                5: [game_pointer >> add_source(b(0, 0x37)), game_pointer >> add_source(b(7, 0x38)), game_pointer >> b(6, 0x38) == heart_count],
            },
        },
        4: {
            '1': {
                1: [game_pointer >> add_source(b(5, 0x38)), game_pointer >> add_source(b(4, 0x38)), game_pointer >> b(3, 0x38) == heart_count],
                2: [game_pointer >> add_source(b(2, 0x38)), game_pointer >> add_source(b(1, 0x38)), game_pointer >> b(0, 0x38) == heart_count],
                3: [game_pointer >> add_source(b(7, 0x39)), game_pointer >> add_source(b(6, 0x39)), game_pointer >> b(5, 0x39) == heart_count],
                4: [game_pointer >> add_source(b(4, 0x39)), game_pointer >> add_source(b(3, 0x39)), game_pointer >> b(2, 0x39) == heart_count],
                5: [game_pointer >> add_source(b(1, 0x39)), game_pointer >> add_source(b(0, 0x39)), game_pointer >> b(7, 0x3A) == heart_count],
            },
            '2': {
                1: [game_pointer >> add_source(b(6, 0x3A)), game_pointer >> add_source(b(5, 0x3A)), game_pointer >> b(4, 0x3A) == heart_count],
                2: [game_pointer >> add_source(b(3, 0x3A)), game_pointer >> add_source(b(2, 0x3A)), game_pointer >> b(1, 0x3A) == heart_count],
            },
            '3': {
                1: [game_pointer >> add_source(b(0, 0x3A)), game_pointer >> add_source(b(7, 0x3B)), game_pointer >> b(6, 0x3B) == heart_count],
                2: [game_pointer >> add_source(b(5, 0x3B)), game_pointer >> add_source(b(4, 0x3B)), game_pointer >> b(3, 0x3B) == heart_count],
                3: [game_pointer >> add_source(b(2, 0x3B)), game_pointer >> add_source(b(1, 0x3B)), game_pointer >> b(0, 0x3B) == heart_count],
            },
            '4': {
                1: [game_pointer >> add_source(b(7, 0x3C)), game_pointer >> add_source(b(6, 0x3C)), game_pointer >> b(5, 0x3C) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x3C)), game_pointer >> add_source(b(3, 0x3C)), game_pointer >> b(2, 0x3C) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x3C)), game_pointer >> add_source(b(0, 0x3C)), game_pointer >> b(7, 0x3D) == heart_count],
            },
            '5': {
                1: [game_pointer >> add_source(b(6, 0x3D)), game_pointer >> add_source(b(5, 0x3D)), game_pointer >> b(4, 0x3D) == heart_count],
                2: [game_pointer >> add_source(b(3, 0x3D)), game_pointer >> add_source(b(2, 0x3D)), game_pointer >> b(1, 0x3D) == heart_count],
                3: [game_pointer >> add_source(b(0, 0x3D)), game_pointer >> add_source(b(7, 0x3E)), game_pointer >> b(6, 0x3E) == heart_count],
            },
            '6': {
                1: [game_pointer >> add_source(b(5, 0x3E)), game_pointer >> add_source(b(4, 0x3E)), game_pointer >> b(3, 0x3E) == heart_count],
                2: [game_pointer >> add_source(b(2, 0x3E)), game_pointer >> add_source(b(1, 0x3E)), game_pointer >> b(0, 0x3E) == heart_count],
                3: [game_pointer >> add_source(b(7, 0x3F)), game_pointer >> add_source(b(6, 0x3F)), game_pointer >> b(5, 0x3F) == heart_count],
                4: [game_pointer >> add_source(b(4, 0x3F)), game_pointer >> add_source(b(3, 0x3F)), game_pointer >> b(2, 0x3F) == heart_count],
                5: [game_pointer >> add_source(b(1, 0x3F)), game_pointer >> add_source(b(0, 0x3F)), game_pointer >> b(7, 0x40) == heart_count],
                6: [game_pointer >> add_source(b(6, 0x40)), game_pointer >> add_source(b(5, 0x40)), game_pointer >> b(4, 0x40) == heart_count],
            },
        },
        5: {
            '1': {
                1: [game_pointer >> add_source(b(3, 0x40)), game_pointer >> add_source(b(2, 0x40)), game_pointer >> b(1, 0x40) == heart_count],
                2: [game_pointer >> add_source(b(0, 0x40)), game_pointer >> add_source(b(7, 0x41)), game_pointer >> b(6, 0x41) == heart_count],
                3: [game_pointer >> add_source(b(5, 0x41)), game_pointer >> add_source(b(4, 0x41)), game_pointer >> b(3, 0x41) == heart_count],
                4: [game_pointer >> add_source(b(2, 0x41)), game_pointer >> add_source(b(1, 0x41)), game_pointer >> b(0, 0x41) == heart_count],
                5: [game_pointer >> add_source(b(7, 0x42)), game_pointer >> add_source(b(6, 0x42)), game_pointer >> b(5, 0x42) == heart_count],
            },
            '2': {
                1: [game_pointer >> add_source(b(4, 0x42)), game_pointer >> add_source(b(3, 0x42)), game_pointer >> b(2, 0x42) == heart_count],
                2: [game_pointer >> add_source(b(1, 0x42)), game_pointer >> add_source(b(0, 0x42)), game_pointer >> b(7, 0x43) == heart_count],
                3: [game_pointer >> add_source(b(6, 0x43)), game_pointer >> add_source(b(5, 0x43)), game_pointer >> b(4, 0x43) == heart_count],
                4: [game_pointer >> add_source(b(3, 0x43)), game_pointer >> add_source(b(2, 0x43)), game_pointer >> b(1, 0x43) == heart_count],
                5: [game_pointer >> add_source(b(0, 0x43)), game_pointer >> add_source(b(7, 0x44)), game_pointer >> b(6, 0x44) == heart_count],
                6: [game_pointer >> add_source(b(5, 0x44)), game_pointer >> add_source(b(4, 0x44)), game_pointer >> b(3, 0x44) == heart_count],
            },
            '3': {
                1: [game_pointer >> add_source(b(2, 0x44)), game_pointer >> add_source(b(1, 0x44)), game_pointer >> b(0, 0x44) == heart_count],
                2: [game_pointer >> add_source(b(7, 0x45)), game_pointer >> add_source(b(6, 0x45)), game_pointer >> b(5, 0x45) == heart_count],
                3: [game_pointer >> add_source(b(4, 0x45)), game_pointer >> add_source(b(3, 0x45)), game_pointer >> b(2, 0x45) == heart_count],
                4: [game_pointer >> add_source(b(1, 0x45)), game_pointer >> add_source(b(0, 0x45)), game_pointer >> b(7, 0x46) == heart_count],
            },
            '4': {
                1: [game_pointer >> add_source(b(6, 0x46)), game_pointer >> add_source(b(5, 0x46)), game_pointer >> b(4, 0x46) == heart_count],
                2: [game_pointer >> add_source(b(3, 0x46)), game_pointer >> add_source(b(2, 0x46)), game_pointer >> b(1, 0x46) == heart_count],
                3: [game_pointer >> add_source(b(0, 0x46)), game_pointer >> add_source(b(7, 0x47)), game_pointer >> b(6, 0x47) == heart_count],
            },
            '5': {
                1: [game_pointer >> add_source(b(5, 0x47)), game_pointer >> add_source(b(4, 0x47)), game_pointer >> b(3, 0x47) == heart_count],
                2: [game_pointer >> add_source(b(2, 0x47)), game_pointer >> add_source(b(1, 0x47)), game_pointer >> b(0, 0x47) == heart_count],
            },
            '6a': {
                1: [game_pointer >> add_source(b(7, 0x48)), game_pointer >> add_source(b(6, 0x48)), game_pointer >> b(5, 0x48) == heart_count],
                2: [game_pointer >> add_source(b(4, 0x48)), game_pointer >> add_source(b(3, 0x48)), game_pointer >> b(2, 0x48) == heart_count],
                3: [game_pointer >> add_source(b(1, 0x48)), game_pointer >> add_source(b(0, 0x48)), game_pointer >> b(7, 0x49) == heart_count],
                4: [game_pointer >> add_source(b(6, 0x49)), game_pointer >> add_source(b(5, 0x49)), game_pointer >> b(4, 0x49) == heart_count],
                5: [game_pointer >> add_source(b(3, 0x49)), game_pointer >> add_source(b(2, 0x49)), game_pointer >> b(1, 0x49) == heart_count],
            },
            '6b': {
                1: [game_pointer >> add_source(b(0, 0x49)), game_pointer >> add_source(b(7, 0x4A)), game_pointer >> b(6, 0x4A) == heart_count],
                2: [game_pointer >> add_source(b(5, 0x4A)), game_pointer >> add_source(b(4, 0x4A)), game_pointer >> b(3, 0x4A) == heart_count],
                3: [game_pointer >> add_source(b(2, 0x4A)), game_pointer >> add_source(b(1, 0x4A)), game_pointer >> b(0, 0x4A) == heart_count],
                4: [game_pointer >> add_source(b(7, 0x4B)), game_pointer >> add_source(b(6, 0x4B)), game_pointer >> b(5, 0x4B) == heart_count],
                5: [game_pointer >> add_source(b(4, 0x4B)), game_pointer >> add_source(b(3, 0x4B)), game_pointer >> b(2, 0x4B) == heart_count],
            },
        },
    }
    ops = {"==": lambda a, b: a == b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}
    b0, b1, b2 = bits
    return [game_pointer >> add_source(b0), game_pointer >> add_source(b1), ops[cmp](game_pointer >> b2, heart_count)]

for act_id, (title, desc, points) in ep2_prog.items():
    ach = Achievement(title, desc, points)
    logic = [
        loaded_save == loaded_save,
        hearts(2, act_id, 5, True, 0)
        hearts(2, act_id, 5,)
    ]



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
 