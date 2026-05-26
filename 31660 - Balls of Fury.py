import pycheevos.core.helpers as helpers
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pathlib import Path


mySet = AchievementSet(game_id=31660, title="Balls of Fury")

# [8-bit] [Save 1] Trophies unlocked
# bit0 - Marathon - Win 10 Exhibition games in a row [Normal or Hard]
# bit1 - The Best Around - Beat Arcade Mode
# bit2 - Happy Ending - Beat Story Mode
# bit3 - Two is Better than One - Play a Multiplayer Game
# bit4 - Multiplayer Marathon - Win 10 Multiplayer games in a row
# bit5 - Arcade Perfection - Beat Arcade Mode without losing a point [Normal or Hard]
# bit6 - Story Perfection - Beat Story Mode without losing a point [Normal or Hard]
# bit7 - Playing with a Full Deck - Unlock all characters
#
# [8-bit] [Save 1] Trophies/Characters unlocked
# bit0 - Not Playing With Power - Beat Arcade Mode without using a Power Move [Normal or Hard]
# bit1 - Everyone's a Winner - Beat Arcade Mode with all characters
# bit2 - Ping Pong Addict - Play for 10 hours
# bit3 - Got Game - Win 10 matches
# bit4 - Karl Wolfschtagg unlocked
# bit5 - Master Wong unlocked - Beat arcade mode
# bit6 - Young Randy unlocked - Beat story mode
# bit7 - The Hammer unlocked 

trophy_addresses = [0x000c3ae4, 0x000c3b5c, 0x000c3bd4, 0x000c3c4c]
arcade_addresses = [0x000c3b48, 0x000c3bc0, 0x000c3c38, 0x000c3cb0]
points_addresses = [0x000c3b30, 0x000c3ba8, 0x000c3c20, 0x000c3c98]
aces_addresses = [0x000c3b34, 0x000c3bac, 0x000c3c24, 0x000c3c9c]
taunt_addresses = [0x000c3b38, 0x000c3bb0, 0x000c3c28, 0x000c3ca0]
power_move_addresses = [0x000c3b36, 0x000c3bae, 0x000c3c26, 0x000c3c9e]



# [24-bit pointer] Points to game data
# +0x28: [32-bit] Player score
# +0x2C: [32-bit] Opponent score
# +0x84: [8-bit] Changes to 0x01 on game over, check player score > opponent score
game_pointer = tbyte(0x000c03c4)
game_over = game_pointer >> byte(0x84)
player_score = remember(game_pointer >> byte(0x28))
opponent_score = game_pointer >> byte(0x2c)

save_index = byte(0x000c3cd1)

mode = dword(0x000c3db4)
opponent = dword(0x000c3da4)
difficulty = dword(0x000c3dac)

game_over_logic = [
    game_over.prior() == value(0x00),
    game_over == value(0x01),
]

core_logic = [
    game_over_logic,
    player_score,
    (opponent_score < recall())
]

def trophy_logic(address, bit_func, offset=0, index=0):
    trophy = bit_func(address + offset)
    return [
        save_index == value(index),
        trophy.delta() == value(0x00),
        trophy == value(0x01),
    ]

def everyones_a_winner_logic(address, bit_func, offset=0, index=0):
    addlist = []
    for y in range(0,10):
        addlist.append(add_source(byte(trophy_addresses[index] + 0x2c + y)))
    print(addlist)
    return [
        *trophy_logic(address, bit1, index=trophy_addresses.index(x)),
        *addlist,
        measured(value(0x00) == value(0x0a))
    ]

def stat_logic(address, bit_func, target, index=0):
    stat = bit_func(address)
    return [
        save_index == value(index),
        stat.delta() < value(target),
        measured(stat == value(target))
    ]

def story_logic(opponent_selected):
    return [
        mode == value(0x01),
        opponent == opponent_selected,
        difficulty >= value(0x01),
        core_logic
    ]

def arcade_logic(arcade_progress, index=0):
    return [
        save_index == value(index),
        byte(arcade_progress) == value(0x09),
    ]
the_hammer = Achievement("The Hammer", "Defeat The Hammer in Story Mode on Normal or Hard difficulty", 1)
the_hammer.add_core(story_logic(value(0x08)))
mySet.add_achievement(the_hammer)

master_wong = Achievement("Master Wong", "Defeat Master Wong in Story Mode on Normal or Hard difficulty", 1)
master_wong.add_core(story_logic(value(0x06)))
mySet.add_achievement(master_wong)

maggie_wong = Achievement("Maggie Wong", "Defeat Maggie Wong in Story Mode on Normal or Hard difficulty", 2)
maggie_wong.add_core(story_logic(value(0x01)))
mySet.add_achievement(maggie_wong)

the_dragon = Achievement("The Dragon", "Defeat The Dragon in Story Mode on Normal or Hard difficulty", 2)
the_dragon.add_core(story_logic(value(0x02)))
mySet.add_achievement(the_dragon)

freddie_fingers = Achievement("Freddie Fingers", "Defeat Freddie Fingers in Story Mode on Normal or Hard difficulty", 3)
freddie_fingers.add_core(story_logic(value(0x03)))
mySet.add_achievement(freddie_fingers)

yukito_nagasaki = Achievement("Yukito Nagasaki", "Defeat Yukito Nagasaki in Story Mode on Normal or Hard difficulty", 3)
yukito_nagasaki.add_core(story_logic(value(0x07)))
mySet.add_achievement(yukito_nagasaki)

feng = Achievement("Feng", "Defeat Feng in Story Mode on Normal or Hard difficulty", 5)
feng.add_core(story_logic(value(0x04)))
mySet.add_achievement(feng)

story_perf = Achievement("Story Perfection", "Unlock the \"Story Perfection\" trophy by beating Story Mode without losing a point on Normal or Hard difficulty", 10)
story_perf.add_core(game_over_logic)
for x in trophy_addresses:
    story_perf.add_alt(trophy_logic(x, bit6, index=trophy_addresses.index(x)))
mySet.add_achievement(story_perf)

arcade_beat = Achievement("Arcade Beat", "Beat Arcade Mode as any character on Normal or Hard difficulty", 5)
arcade_beat.add_core(mode == value(0x02))
arcade_beat.add_core(difficulty >= value(0x01))
arcade_beat.add_core(core_logic)

for x in arcade_addresses:
    arcade_beat.add_alt(arcade_logic(x, index=arcade_addresses.index(x)))
mySet.add_achievement(arcade_beat)

everyones_a_winner = Achievement("Everyone's a Winner", "Unlock the \"Everyone\'s a Winner\" trophy by beating Arcade Mode with every character", 25)
everyones_a_winner.add_core(game_over_logic)

for x in trophy_addresses:
    everyones_a_winner.add_alt(everyones_a_winner_logic(x, bit1, index=trophy_addresses.index(x)))
mySet.add_achievement(everyones_a_winner)

arcade_perfection = Achievement("Arcade Perfection", "Unlock the \"Arcade Perfection\" trophy by beating Arcade Mode without losing a point on Normal or Hard difficulty", 50)
arcade_perfection.add_core(game_over_logic)

for x in trophy_addresses:
    arcade_perfection.add_alt(trophy_logic(x, bit5, index=trophy_addresses.index(x)))
mySet.add_achievement(arcade_perfection)

not_playing_with_power = Achievement("Not Playing With Power", "Unlock the \"Not Playing With Power\" trophy by beating Arcade Mode without using a Power Move on Normal or Hard difficulty", 25)
not_playing_with_power.add_core(game_over_logic)

for x in trophy_addresses:
    not_playing_with_power.add_alt(trophy_logic(x, bit0, offset=0x01, index=trophy_addresses.index(x)))
mySet.add_achievement(not_playing_with_power)

# insert the extra ones for getting stat padding

points_1000 = Achievement("Points Machine", "Win 1000 points", 10, 592358)
points_1000.add_core(value(0x00) == value(0x00))

for x in points_addresses:
    points_1000.add_alt(stat_logic(x, dword, target=0x3e8,index=points_addresses.index(x)))
mySet.add_achievement(points_1000)

aces_50 = Achievement("Aces High", "Ace 50 Serves", 10)
aces_50.add_core(game_over_logic)
for x in aces_addresses:
    aces_50.add_alt(stat_logic(x, word, target=0x32,index=aces_addresses.index(x)))
mySet.add_achievement(aces_50)

power_moves_150 = Achievement("Power Player", "Perform 150 Power Moves", 10)
power_moves_150.add_core(game_over_logic)
for x in power_move_addresses:
    power_moves_150.add_alt(stat_logic(x, word, target=0x96,index=power_move_addresses.index(x)))
mySet.add_achievement(power_moves_150)




got_game = Achievement("Got Game", "Unlock the \"Got Game\" trophy by winning 10 matches", 5)
got_game.add_core(game_over_logic)
for x in trophy_addresses:
    got_game.add_alt(trophy_logic(x, bit3, offset=0x01, index=trophy_addresses.index(x)))
mySet.add_achievement(got_game)



marathon_achievement = Achievement("Marathon", "Unlock the \"Marathon\" trophy by winning 10 Exhibition games in a row on Normal or Hard difficulty", 10)
marathon_achievement.add_core(game_over_logic)

for x in trophy_addresses:
    marathon_achievement.add_alt(trophy_logic(x, bit0, index=trophy_addresses.index(x)))

mySet.add_achievement(marathon_achievement)

ping_pong_addict = Achievement("Ping Pong Addict", "Unlock the \"Ping Pong Addict\" trophy by playing the greatest table tennis movie tie-in game ever released for 10 hours", 5)
ping_pong_addict.add_core(game_over_logic)

for x in trophy_addresses:
    ping_pong_addict.add_alt(trophy_logic(x, bit2, offset=0x01, index=trophy_addresses.index(x)))
mySet.add_achievement(ping_pong_addict)

playing_with_a_full_deck = Achievement("Playing With a Full Deck", "Unlock the \"Playing with a Full Deck\" trophy by unlocking every character", 5)
playing_with_a_full_deck.add_core(game_over_logic)

for x in trophy_addresses:
    playing_with_a_full_deck.add_alt(trophy_logic(x, bit3, index=trophy_addresses.index(x)))

mySet.add_achievement(playing_with_a_full_deck)

karl_wolfschtagg_unlock = Achievement("Karl Wolfschtagg", "Unlock Karl Wolfschtagg by winning 20 matches against the AI", 2)
karl_wolfschtagg_unlock.add_core(game_over_logic)

for x in trophy_addresses:
    karl_wolfschtagg_unlock.add_alt(trophy_logic(x, bit4, offset=0x01, index=trophy_addresses.index(x)))
mySet.add_achievement(karl_wolfschtagg_unlock)

the_hammer_unlock = Achievement("The Hammer", "Unlock The Hammer by playing for 5 hours", 2)
the_hammer_unlock.add_core(game_over_logic)
for x in trophy_addresses:
    the_hammer_unlock.add_alt(trophy_logic(x, bit7, offset=0x01, index=trophy_addresses.index(x)))
mySet.add_achievement(the_hammer_unlock)



laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

if laptopPath.exists():
    mySet.save(laptopPath)
elif pcPath.exists():
    mySet.save(pcPath)
else:
    mySet.save()