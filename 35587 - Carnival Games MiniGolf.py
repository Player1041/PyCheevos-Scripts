import pycheevos.core.helpers as helpers
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pycheevos.models.leaderboard import Leaderboard
from pathlib import Path
import csv

mySet = AchievementSet(game_id=35587, title="Carnival Games: Minigolf")
mask = 0x1fffffff

player2_not_barker   = (dword_be(0x005f5594) != 0x00) & (pause_if((dword_be(0x005f5594) & mask) >> byte(0xba) != 0x38))
special_player2_not_barker = (dword_be(0x005f5594) == 0x00) | ((dword_be(0x005f5594) & mask) >> byte(0xba) == 0x38)

# Base pointers — masked at root
main_pointer     = dword_be(0x005f5590) & mask
egg_pointer      = dword_be(0x005eb58c) & mask
minigame_pointer = dword_be(0x005f54b8) & mask
timer_pointer    = dword_be(0x005ddc48) & mask

print(main_pointer)

# Map pointer — every intermediate pointer masked, final offset is leaf
map_ptr = (dword_be(0x005f550c) & mask) >> (dword_be(0x00) & mask)
map     = map_ptr >> dword_be(0x04)

area_id          = dword_be(0x005ddb98)
unlocking_hidden = dword_be(0x005f5504)

# Character game data — every intermediate pointer masked, final offset is leaf
game_data_ptr   = main_pointer >> (dword_be(0x19c) & mask)
hole_complete   = game_data_ptr >> byte(0x127)
shot            = game_data_ptr >> dword_be(0x84)
coins_collected = game_data_ptr >> dword_be(0xb0)
flipper_coins   = game_data_ptr >> dword_be(0xb4)

# Minigame data — intermediate 0x08 pointer masked, final offsets are leaves
mg_data_ptr     = minigame_pointer >> (dword_be(0x08) & mask)
mg_state        = mg_data_ptr >> dword_be(0x110)
mg_secondary    = mg_data_ptr >> dword_be(0x114)  # eggs/gnomes/ghouls/notes
mg_coins        = mg_data_ptr >> dword_be(0x11c)
mg_total_coins  = mg_data_ptr >> dword_be(0x120)
mg_failed       = mg_data_ptr >> byte(0x130)
mg_ghosts       = mg_data_ptr >> dword_be(0x148)
mg_shots_remain = mg_data_ptr >> dword_be(0x160)
mg_items_missed = mg_data_ptr >> dword_be(0x178)

# Timer — one level of indirection, final offset is leaf
mg_timer        = timer_pointer >> float32_be(0x80)

# Egg — one level of indirection, final offsets are leaves
egg_damaged     = egg_pointer >> word_be(0xde4)
egg_state       = egg_pointer >> word_be(0xde6)

# ---------------------------------------------------------------------------
# Per-map minigame state overrides
# start      : state value when minigame is starting — accumulates 1 hit
# in_game    : state value when minigame is being played
# trigger_on : state value when minigame completed successfully
# ---------------------------------------------------------------------------
MINIGAME_STATES = {
    # map_name:              (start, in_game, trigger_on)
    "Sky City":              (0x04,  0x05,    0x07),   # Maze-o-Rama (optional)
    "Old Toothy":            (0x03,  0x04,    0x06),   # Ghoul Hunter
    "Going Tribal":          (0x03,  0x04,    0x06),   # Jungle Bogey
    "Crooked Walk":          (0x03,  0x04,    0x07),   # Juggles
    "Old #7":                (0x03,  0x04,    0x06),   # Mine Shaft Madness
    "Hog Heaven":            (0x04,  0x05,    0x08),   # The Scrambler
    "Skull Isle":            (0x03,  0x04,    0x06),   # Cannon Fodder (mandatory)
    "Pterodactyl's Roost":   (0x03,  0x04,    0x06),   # Pterodactyl's Run
    "Downhill Slide":        (0x03,  0x09,    0x0f),   # G-Nome Project (results=0x10)
}


def get_coin_pointers(area_name):
    area_coin_offsets = {
        "Rah's Revenge":    [0x246, 0x247, 0x248],
        "Spook-o-Rama":     [0x249, 0x24a, 0x24b],
        "Amazeon":          [0x24c, 0x24d, 0x24e],
        "King's Court":     [0x24f, 0x250, 0x251],
        "Wild West":        [0x252, 0x253, 0x254],
        "Prehistoria":      [0x255, 0x256, 0x257],
        "Barn Yard":        [0x258, 0x259, 0x25a],
        "Pirate's Delight": [0x25b, 0x25c, 0x25d],
        "Fairytella":       [0x25e, 0x25f, 0x260],
    }
    offsets = area_coin_offsets.get(area_name)
    if offsets is None:
        return None
    return offsets


def get_puzzle_pointers(area_name):
    area_puzzle_offsets = {
        "Rah's Revenge":    [0x262, 0x263, 0x264],
        "Spook-o-Rama":     [0x265, 0x266, 0x267],
        "Amazeon":          [0x268, 0x269, 0x26a],
        "King's Court":     [0x26b, 0x26c, 0x26d],
        "Wild West":        [0x26e, 0x26f, 0x270],
        "Prehistoria":      [0x271, 0x272, 0x273],
        "Barn Yard":        [0x274, 0x275, 0x276],
        "Pirate's Delight": [0x277, 0x278, 0x279],
        "Fairytella":       [0x27a, 0x27b, 0x27c],
    }
    offsets = area_puzzle_offsets.get(area_name)
    if offsets is None:
        return None
    return offsets


def get_hidden_unlock_pointers(area_name):
    area_hidden_offsets = {
        "Wild West":        [0x22b],  # Samurai Face
        "Rah's Revenge":    [0x22c],  # Florence Mask
        "Barn Yard":        [0x22d],  # Cupid Wings
        "Spook-o-Rama":     [0x22e],  # Dragon Wings
        "Amazeon":          [0x22f],  # Monkey-on-my-Back
        "Prehistoria":      [0x230],  # Lion Paws
        "King's Court":     [0x231],  # Rainbow Shoes
        "Fairytella":       [0x232],  # Sunday Shoes
        "Pirate's Delight": [0x233],  # Sharkster Shoes
    }
    offsets = area_hidden_offsets.get(area_name)
    if offsets is None:
        return None
    return offsets


def get_area_maps(area_name):
    area_maps = {
        "Rah's Revenge":    ["Sky City", "Egyptian Way", "That Sphinx"],
        "Spook-o-Rama":     ["Old Toothy", "Devil's Brew", "Windy Lane"],
        "Amazeon":          ["Going Tribal", "Big Mouth Juju", "Rickety Ride"],
        "King's Court":     ["Crooked Walk", "Knight's Gauntlet", "Castle Siege"],
        "Wild West":        ["Old #7", "Dynamite", "Gunslinger"],
        "Prehistoria":      ["Pterodactyl's Roost", "Dino-Mite", "Magma Madness"],
        "Barn Yard":        ["Hog Heaven", "Egghead", "Old Mcdoogle"],
        "Pirate's Delight": ["Skull Isle", "Pirate's Crossing", "Deck Hand"],
        "Fairytella":       ["Downhill Slide", "Troll Bridge", "Flower Power"],
    }
    maps = area_maps.get(area_name)
    if maps is None:
        return None
    return maps


def map_pull(name):
    maps = {
        "Sky City": 0x5f305f4e,
        "Egyptian Way": 0x5f315f4e,
        "That Sphinx": 0x5f325f4e,
        "Old Toothy": 0x5f335f4e,
        "Devil's Brew": 0x5f345f4e,
        "Windy Lane": 0x5f355f4e,
        "Going Tribal": 0x5f365f4e,
        "Big Mouth Juju": 0x5f375f4e,
        "Rickety Ride": 0x5f385f4e,
        "Crooked Walk": 0x5f395f4e,
        "Knight's Gauntlet": 0x5f31305f,
        "Castle Siege": 0x5f31315f,
        "Old #7": 0x5f31325f,
        "Dynamite": 0x5f31335f,
        "Gunslinger": 0x5f31345f,
        "Pterodactyl's Roost": 0x5f31355f,
        "Dino-Mite": 0x5f31365f,
        "Magma Madness": 0x5f31375f,
        "Hog Heaven": 0x5f31385f,
        "Egghead": 0x5f31395f,
        "Old Mcdoogle": 0x5f32305f,
        "Skull Isle": 0x5f32315f,
        "Pirate's Crossing": 0x5f32325f,
        "Deck Hand": 0x5f32335f,
        "Downhill Slide": 0x5f32345f,
        "Troll Bridge": 0x5f32355f,
        "Flower Power": 0x5f32365f,
    }
    return maps.get(name)


def get_shop_pointers(area_name):
    area_shop_offsets = {
        "Fairytella":       [0x1dc, 0x1dd, 0x1de, 0x1df, 0x1e0, 0x1e1, 0x1e2, 0x1e3],
        "Prehistoria":      [0x1e4, 0x1e5, 0x1e6, 0x1e7, 0x1e8, 0x1e9, 0x1ea, 0x1eb],
        "Barn Yard":        [0x1ec, 0x1ed, 0x1ee, 0x1ef, 0x1f0, 0x1f1, 0x1f2, 0x1f3],
        "Pirate's Delight": [0x1f4, 0x1f5, 0x1f6, 0x1f7, 0x1f8, 0x1f9, 0x1fa, 0x1fb],
        "King's Court":     [0x1fc, 0x1fd, 0x1fe, 0x1ff, 0x200, 0x201, 0x202, 0x203],
        "Wild West":        [0x204, 0x205, 0x206, 0x207, 0x208, 0x209, 0x20a, 0x20b],
        "Rah's Revenge":    [0x20c, 0x20d, 0x20e, 0x20f, 0x210, 0x211, 0x212, 0x213],
        "Spook-o-Rama":     [0x214, 0x215, 0x216, 0x217, 0x218, 0x219, 0x21a, 0x21b],
        "Amazeon":          [0x21c, 0x21d, 0x21e, 0x21f, 0x220, 0x221, 0x222, 0x223],
        "Barker's Shop":    [0x224, 0x225, 0x226, 0x227, 0x228, 0x229, 0x22a],
        "Cat Jester":       [0x1fe]
    }
    offsets = area_shop_offsets.get(area_name)
    if offsets is None:
        return None
    return offsets


def coin_logic(area_name):
    logic = []
    logic.append(player2_not_barker)
    maps = get_area_maps(area_name)
    for i, x in enumerate(maps):
        if i == len(maps) - 1:
            logic.append(map == map_pull(x))
        else:
            logic.append(or_next(map == map_pull(x)))

    coin_ptrs = get_coin_pointers(area_name)
    for x in coin_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(delta(byte(x))))
    logic.append(add_address(main_pointer))
    logic.append(delta(byte(coin_ptrs[-1])) == 2)

    for x in coin_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(byte(x)))
    logic.append(add_address(main_pointer))
    logic.append(measured(byte(coin_ptrs[-1]) == 3))

    return logic


def puzzle_logic(area_name):
    logic = []
    logic.append(player2_not_barker)
    maps = get_area_maps(area_name)
    for i, x in enumerate(maps):
        if i == len(maps) - 1:
            logic.append(map == map_pull(x))
        else:
            logic.append(or_next(map == map_pull(x)))

    puzzle_ptrs = get_puzzle_pointers(area_name)
    for x in puzzle_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(delta(byte(x))))
    logic.append(add_address(main_pointer))
    logic.append(delta(byte(puzzle_ptrs[-1])) == 2)

    for x in puzzle_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(byte(x)))
    logic.append(add_address(main_pointer))
    logic.append(measured(byte(puzzle_ptrs[-1]) == 3))

    return logic


def shop_logic(area_name):
    logic = []
    if area_name != "Cat Jester":
        logic.append(player2_not_barker)
    else:
        logic.append(special_player2_not_barker)
    
    shop_ptrs = get_shop_pointers(area_name)

    for x in shop_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(delta(byte(x))))
    if area_name == "Cat Jester":
        logic.append(add_address(main_pointer))
        logic.append(delta(byte(shop_ptrs[-1])) == len(shop_ptrs) - 1)
    else:
        logic.append(add_address(main_pointer))
        logic.append(delta(byte(shop_ptrs[-1])) == len(shop_ptrs) - 1)

    for x in shop_ptrs[:-1]:
        logic.append(add_address(main_pointer))
        logic.append(add_source(byte(x)))

    if area_name == "Cat Jester":
        logic.append(add_address(main_pointer))
        logic.append(byte(shop_ptrs[-1]) == len(shop_ptrs))
    else:
        logic.append(add_address(main_pointer))
        logic.append(measured(byte(shop_ptrs[-1]) == len(shop_ptrs)))

    return logic


def hidden_logic(area_name):
    logic = []
    logic.append(special_player2_not_barker)
    logic.append(area_id == areas.index(area_name))

    hidden_ptrs = get_hidden_unlock_pointers(area_name)
    x = hidden_ptrs[0]

    logic.append(add_address(main_pointer))
    logic.append(delta(byte(x)) == 0x00)

    logic.append(add_address(main_pointer))
    logic.append(byte(x) == 0x01)

    return logic


def minigame_logic(map_name, reset_on_failed=True, pause_on_loading=True, should_measure=False, extra_conditions=None):
    logic = []
    logic.append(player2_not_barker)
    logic.append((map == map_pull(map_name)))
    logic.append(reset_if((main_pointer >> dword_be(0x19c)) == 0x00))
    logic.append(reset_if(shot == 0x00))

    start_state, in_game_state, trigger_state = MINIGAME_STATES.get(map_name, (0x03, 0x04, 0x06))

    if pause_on_loading:
        logic.append(pause_if(mg_state > 0x11))

    if reset_on_failed:
        logic.append(reset_if(mg_failed == 0x01))

    logic.append(reset_if(mg_state == 0x00))
    logic.append((mg_state == start_state).with_hits(1))

    if extra_conditions:
        logic.extend(extra_conditions)
    logic.append(mg_state.delta() != trigger_state)
    logic.append(trigger(mg_state == trigger_state))

    return logic


def course_logic(map_name, max_shots=None, min_coins=None, no_egg_damage=False, min_flipper_coins=None, extra_conditions=None):
    logic = []
    logic.append(special_player2_not_barker)
    logic.append(map == map_pull(map_name))
    logic.append((main_pointer >> dword_be(0x19c)) != 0x00)

    if map_name != "Troll Bridge":
        logic.append(hole_complete.delta() == 0x00)
        logic.append(trigger(hole_complete == 0x01))

    if max_shots is not None:
        logic.append(shot <= max_shots)

    if min_coins is not None:
        logic.append(coins_collected.prior() < min_coins)
        logic.append(trigger(coins_collected >= min_coins))

    if min_flipper_coins is not None:
        logic.append(flipper_coins.delta() < min_flipper_coins)
        logic.append(trigger(flipper_coins >= min_flipper_coins))

    if no_egg_damage:
        logic.append((shot == 1).with_hits(1))
        logic.append(reset_if(prior(egg_state) == 0x03))

    if extra_conditions:
        logic.extend(extra_conditions)

    return logic


areas = ["Rah's Revenge", "Spook-o-Rama", "Amazeon", "King's Court", "Wild West", "Prehistoria", "Barn Yard", "Pirate's Delight", "Fairytella"]

# ===========================================================================
# TITLES AND DESCRIPTIONS
# Edit these to customise achievement names and descriptions per area/map.
# ===========================================================================

def titles_coins(area):
    return {
        "Rah's Revenge":    "Pharaoh's Curse",
        "Spook-o-Rama":     "Trick or Treat? Trick!",
        "Amazeon":          "Deep in the Jungle",
        "King's Court":     "Off With His Head!",
        "Wild West":        "You Drew Too Late",
        "Prehistoria":      "Prehistoric Thrashing",
        "Barn Yard":        "Thrown to the Slop Bucket",
        "Pirate's Delight": "Sent to Davy Jones' Locker!",
        "Fairytella":       "Once Upon a Birdie",
    }.get(area)

def descs_coins(area):
    return {
        "Rah's Revenge":    "Beat Barker on every course in Rah's Revenge",
        "Spook-o-Rama":     "Beat Barker on every course in Spook-o-Rama",
        "Amazeon":          "Beat Barker on every course in Amazeon",
        "King's Court":     "Beat Barker on every course in King's Court",
        "Wild West":        "Beat Barker on every course in Wild West",
        "Prehistoria":      "Beat Barker on every course in Prehistoria",
        "Barn Yard":        "Beat Barker on every course in Barn Yard",
        "Pirate's Delight": "Beat Barker on every course in Pirate's Delight",
        "Fairytella":       "Beat Barker on every course in Fairytella",
    }.get(area)


def titles_puzzles(area):
    return {
        "Rah's Revenge":    "King Tut's Scepter",
        "Spook-o-Rama":     "Spooky Spooky",
        "Amazeon":          "Voodoo? What Did Voo Do?",
        "King's Court":     "By Order of the King",
        "Wild West":        "Rather Have Thomas",
        "Prehistoria":      "Dinosaur!",
        "Barn Yard":        "One Hell of a Needle in the Hay Stack",
        "Pirate's Delight": "Going Down!",
        "Fairytella":       "Now I Can Be a Fairy Godmother",
    }.get(area)

def descs_puzzles(area):
    clubs = {
        "Rah's Revenge":    "Scepter Club",
        "Spook-o-Rama":     "Halloween Club",
        "Amazeon":          "Voodoo Club",
        "King's Court":     "Knight Club",
        "Wild West":        "Choo Choo Club",
        "Prehistoria":      "Tooth Club",
        "Barn Yard":        "Hay Club",
        "Pirate's Delight": "Anchor Club",
        "Fairytella":       "Falling Star Club",
    }
    club = clubs.get(area)
    return f'Unlock the "{club}" by collecting every Puzzle Piece in {area}'


def titles_shops(area):
    return {
        "Rah's Revenge":    "So Many Sand Coins",
        "Spook-o-Rama":     "Trick or Treat? Treat!",
        "Amazeon":          "Amazeon Prime",
        "King's Court":     "All In a Knight's Work",
        "Wild West":        "I Thought Things Were Cheaper Back in the Day",
        "Prehistoria":      "Prehistoric Spending",
        "Barn Yard":        "This Coin Is Pungent...",
        "Pirate's Delight": "So Much Gold!",
        "Fairytella":       "A Price to Pay to Be a Fairytale",
        "Barker's Shop":    "Identity Thief",
        "Cat Jester":       "Hit It, Jester!",
    }.get(area)

def descs_shops(area):
    return {
        "Rah's Revenge":    "Buy every item in the Rah's Revenge shop",
        "Spook-o-Rama":     "Buy every item in the Spook-o-Rama shop",
        "Amazeon":          "Buy every item in the Amazeon shop",
        "King's Court":     "Buy every item in the King's Court shop",
        "Wild West":        "Buy every item in the Wild West shop",
        "Prehistoria":      "Buy every item in the Prehistoria shop",
        "Barn Yard":        "Buy every item in the Barn Yard shop",
        "Pirate's Delight": "Buy every item in the Pirate's Delight shop",
        "Fairytella":       "Buy every item in the Fairytella shop",
        "Barker's Shop":    "Buy every item in Barker's Shop",
        "Cat Jester":       "Purchase the Cat Jester",
    }.get(area)


def titles_hidden(area):
    return {
        "Wild West":        "Wrong Era, Wrong Continent",
        "Rah's Revenge":    "Florence and the Desert",
        "Barn Yard":        "Matchmaker",
        "Spook-o-Rama":     "Here Be Dragons",
        "Amazeon":          "Get Off My Back!",
        "Prehistoria":      "1/6 of a Fursuit",
        "King's Court":     "Somewhere Over the Rainbow",
        "Fairytella":       "Wearing My Best Sunday Shoes",
        "Pirate's Delight": "Blahaj",
    }.get(area)

def descs_hidden(area):
    items = {
        "Wild West":        "Samurai Face",
        "Rah's Revenge":    "Florence Mask",
        "Barn Yard":        "Cupid Wings",
        "Spook-o-Rama":     "Dragon Wings",
        "Amazeon":          "Monkey-on-my-Back",
        "Prehistoria":      "Lion Paws",
        "King's Court":     "Rainbow Shoes",
        "Fairytella":       "Sunday Shoes",
        "Pirate's Delight": "Sharkster Shoes",
    }
    item = items.get(area)
    return f'Unlock the hidden "{item}" in {area}'


def titles_course(map_name):
    return {
        "Troll Bridge":      "Rich Troll",
        "Dino-Mite":         "A Prehistoric Boom!",
        "Egghead":           "Not So Cracking Shot",
        "Pirate's Crossing": "Plundering the Crossing",
        "Dynamite":          "A Western Boom!",
        "Knight's Gauntlet": "Defending the Crossing",
        "Devil's Brew":      "Witch-y Business",
        "Big Mouth Juju":    "Bad Juju",
        "Egyptian Way":      "Putt Like An Egyptian",
    }.get(map_name)

def descs_course(map_name):
    return {
        "Troll Bridge":      'Complete "Troll Bridge" with 50 coins from the pinball minigame',
        "Dino-Mite":         'Complete "Dino-Mite" with a Hole in One',
        "Egghead":           'Complete "Egghead" without breaking the big egg and within 4 shots',
        "Pirate's Crossing": 'Complete "Pirate\'s Crossing" with every coin collected',
        "Dynamite":          'Complete "Dynamite" with a Hole in One',
        "Knight's Gauntlet": 'Complete "Knight\'s Gauntlet" within 2 shots',
        "Devil's Brew":      'Complete "Devil\'s Brew" within 3 shots',
        "Big Mouth Juju":    'Complete "Big Mouth Juju" within 2 shots',
        "Egyptian Way":      'Complete "Egyptian Way" within 3 shots',
    }.get(map_name)


def titles_minigame(map_name):
    return {
        "Downhill Slide":      "A Rich G-Nome",
        "Pterodactyl's Roost": "An Expensive Flight",
        "Hog Heaven":          "These Eggs Are So Bouncy",
        "Skull Isle":          "Sea of Thieves?",
        "Old #7":              "Ghostbusters",
        "Crooked Walk":        "The Fox, Chicken and... Flaming Skull Problem?",
        "Old Toothy":          "Ghoulbusters",
        "Going Tribal":        "Guitar Hero: Kids Edition",
        "Sky City":            "A-Maze-ing!",
    }.get(map_name)

def descs_minigame(map_name):
    return {
        "Downhill Slide":      'Complete "The G-Nome Project" in Downhill Slide without missing any coins',
        "Pterodactyl's Roost": 'Complete "Pterodactyl\'s Run" in Pterodactyl\'s Roost without missing any coins',
        "Hog Heaven":          'Complete "The Scrambler" in Hog Heaven without missing more than 5 coins or eggs',
        "Skull Isle":          'Complete "Cannon Fodder" in Skull Isle without missing any coins',
        "Old #7":              'Complete "Mine Shaft Madness" in Old #7 without missing any coins or ghosts',
        "Crooked Walk":        'Complete "Juggles" in Crooked Walk without missing any coins',
        "Old Toothy":          'Complete "Ghoul Hunter" in Old Toothy with 30 kills and without missing any coins',
        "Going Tribal":        'Complete "Jungle Bogey" in Going Tribal without missing any notes',
        "Sky City":            'Complete "Maze-o-Rama" in Sky City without missing any coins and in under 45 seconds',
    }.get(map_name)


# ===========================================================================
# ACHIEVEMENT GENERATION
# ===========================================================================

# Collect all (title, description, points, area/map) for CSV export
csv_rows = []  # (category, area_or_map, title, description, points)

# Barker Coins
for area in areas:
    t, d, p = titles_coins(area), descs_coins(area), 3
    ach = Achievement(t, d, p)
    ach.add_core(coin_logic(area))
    #mySet.add_achievement(ach)
    csv_rows.append(("Coins", area, t, d, p))

# Clubs / Puzzle Pieces
for area in areas:
    t, d, p = titles_puzzles(area), descs_puzzles(area), 3
    ach = Achievement(t, d, p)
    ach.add_core(puzzle_logic(area))
    #mySet.add_achievement(ach)
    csv_rows.append(("Puzzles", area, t, d, p))

# Shops — areas
for area in areas:
    t, d, p = titles_shops(area), descs_shops(area), 10
    ach = Achievement(t, d, p)
    ach.add_core(shop_logic(area))
    #mySet.add_achievement(ach)
    csv_rows.append(("Shop", area, t, d, p))

# Shops — specials
for key, pts in [("Barker's Shop", 10), ("Cat Jester", 1)]:
    t, d, p = titles_shops(key), descs_shops(key), pts
    ach = Achievement(t, d, p)
    ach.add_core(shop_logic(key))
    #mySet.add_achievement(ach)
    csv_rows.append(("Shop", key, t, d, p))

# Hidden Unlocks
for area in areas:
    t, d, p = titles_hidden(area), descs_hidden(area), 1
    ach = Achievement(t, d, p)
    ach.add_core(hidden_logic(area))
    #mySet.add_achievement(ach)
    csv_rows.append(("Hidden", area, t, d, p))

# Course challenges
course_entries = [
    ("Troll Bridge",      dict(min_flipper_coins=50)),
    ("Dino-Mite",         dict(max_shots=1)),
    ("Egghead",           dict(max_shots=4, no_egg_damage=True)),
    ("Pirate's Crossing", dict(min_coins=22)),
    ("Dynamite",          dict(max_shots=1)),
    ("Knight's Gauntlet", dict(max_shots=2)),
    ("Devil's Brew",      dict(max_shots=3)),
    ("Big Mouth Juju",    dict(max_shots=2)),
    ("Egyptian Way",      dict(max_shots=3)),
]
for map_name, kwargs in course_entries:
    t, d, p = titles_course(map_name), descs_course(map_name), 5
    ach = Achievement(t, d, p)
    ach.add_core(course_logic(map_name, **kwargs))
    mySet.add_achievement(ach)
    csv_rows.append(("Course", map_name, t, d, p))

# Minigame challenges
ach = Achievement(titles_minigame("Downhill Slide"), descs_minigame("Downhill Slide"), 3)
ach.add_core(minigame_logic("Downhill Slide", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Downhill Slide", titles_minigame("Downhill Slide"), descs_minigame("Downhill Slide"), 10))

ach = Achievement(titles_minigame("Pterodactyl's Roost"), descs_minigame("Pterodactyl's Roost"), 10)
ach.add_core(minigame_logic("Pterodactyl's Roost", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Pterodactyl's Roost", titles_minigame("Pterodactyl's Roost"), descs_minigame("Pterodactyl's Roost"), 10))

ach = Achievement(titles_minigame("Hog Heaven"), descs_minigame("Hog Heaven"), 10)
ach.add_core(minigame_logic("Hog Heaven", should_measure=True, extra_conditions=[
    measured(mg_items_missed <= 5),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Hog Heaven", titles_minigame("Hog Heaven"), descs_minigame("Hog Heaven"), 10))

ach = Achievement(titles_minigame("Skull Isle"), descs_minigame("Skull Isle"), 5)
ach.add_core(minigame_logic("Skull Isle", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Skull Isle", titles_minigame("Skull Isle"), descs_minigame("Skull Isle"), 10))

ach = Achievement(titles_minigame("Old #7"), descs_minigame("Old #7"), 3)
ach.add_core(minigame_logic("Old #7", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
    measured(mg_ghosts == 0x16),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Old #7", titles_minigame("Old #7"), descs_minigame("Old #7"), 10))

ach = Achievement(titles_minigame("Crooked Walk"), descs_minigame("Crooked Walk"), 3)
ach.add_core(minigame_logic("Crooked Walk", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Crooked Walk", titles_minigame("Crooked Walk"), descs_minigame("Crooked Walk"), 10))

# add in reset if game state is > 7 but the ghost counter is < 1d, to prevent softlock from intentionally missing ghosts to preserve coins for later attempts
ach = Achievement(titles_minigame("Old Toothy"), descs_minigame("Old Toothy"), 5)
ach.add_core(minigame_logic("Old Toothy", should_measure=True, extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
    measured(mg_secondary >= 30)
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Old Toothy", titles_minigame("Old Toothy"), descs_minigame("Old Toothy"), 10))

ach = Achievement(titles_minigame("Going Tribal"), descs_minigame("Going Tribal"), 5)
ach.add_core(minigame_logic("Going Tribal", should_measure=True, extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
    measured(mg_secondary >= 25)
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Going Tribal", titles_minigame("Going Tribal"), descs_minigame("Going Tribal"), 10))

ach = Achievement(titles_minigame("Sky City"), descs_minigame("Sky City"), 5)
ach.add_core(minigame_logic("Sky City", extra_conditions=[
    remember(mg_total_coins),
    trigger(mg_coins == recall()),
    mg_timer >= 15.0,
]))
mySet.add_achievement(ach)
csv_rows.append(("Minigame", "Sky City", titles_minigame("Sky City"), descs_minigame("Sky City"), 10))


# ===========================================================================
# CSV EXPORT
# ===========================================================================

csv_path = Path(__file__).parent / "35587_achievements.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Description"])
    for row in csv_rows:
        writer.writerow([row[2], row[3]])

print(f"CSV written to {csv_path}")


# ===========================================================================
# LEADERBOARDS
# ===========================================================================

map_names = {
    "Sky City":            "Rah's Revenge",
    "Egyptian Way":        "Rah's Revenge",
    "That Sphinx":         "Rah's Revenge",
    "Old Toothy":          "Spook-o-Rama",
    "Devil's Brew":        "Spook-o-Rama",
    "Windy Lane":          "Spook-o-Rama",
    "Going Tribal":        "Amazeon",
    "Big Mouth Juju":      "Amazeon",
    "Rickety Ride":        "Amazeon",
    "Crooked Walk":        "King's Court",
    "Knight's Gauntlet":   "King's Court",
    "Castle Siege":        "King's Court",
    "Old #7":              "Wild West",
    "Dynamite":            "Wild West",
    "Gunslinger":          "Wild West",
    "Pterodactyl's Roost": "Prehistoria",
    "Dino-Mite":           "Prehistoria",
    "Magma Madness":       "Prehistoria",
    "Hog Heaven":          "Barnyard",
    "Egghead":             "Barnyard",
    "Old Mcdoogle":        "Barnyard",
    "Skull Isle":          "Pirate's Delight",
    "Pirate's Crossing":   "Pirate's Delight",
    "Deck Hand":           "Pirate's Delight",
    "Downhill Slide":      "Fairytella",
    "Troll Bridge":        "Fairytella",
    "Flower Power":        "Fairytella",
}

lborder = 158801
for name, area in map_names.items():
    lb = Leaderboard(
        id=lborder,
        title=f"{area} - {name} - Fewest Shots",
        description=f"How well can you putt? Complete {name} in as few shots as possible",
        format=LeaderboardFormat.VALUE,
        lower_is_better=True
    )
    lb.set_start([
        player2_not_barker,
        map == map_pull(name),
        hole_complete.delta() == 0x00,
        hole_complete == 0x01,
    ])
    lb.set_cancel([
        main_pointer >> dword_be(0x19c) == 0x00
    ])
    lb.set_submit([
        hole_complete.delta() == 0x00,
        hole_complete == 0x01
    ])
    lb.set_value([
        measured(shot)
    ])
    mySet.add_leaderboard(lb)
    lborder += 1

most_flipper_coins = Leaderboard(
    id=lborder,
    title="Fairytella - Troll Bridge - Most coins earned during pinball",
    description="Earn as many coins as possible in the pinball minigame, then complete the course",
    format=LeaderboardFormat.VALUE,
    lower_is_better=False
)
most_flipper_coins.set_start([
    player2_not_barker,
    map == map_pull("Troll Bridge"),
    hole_complete.delta() == 0x00,
    hole_complete == 0x01,
])
most_flipper_coins.set_cancel([
    main_pointer >> dword_be(0x19c) == 0x00
])
most_flipper_coins.set_submit([
    hole_complete.delta() == 0x00,
    hole_complete == 0x01
])
most_flipper_coins.set_value([
    measured(flipper_coins)
])
mySet.add_leaderboard(most_flipper_coins)

lb = Leaderboard(
        id=lborder,
        title=f"Pirate's Delight - Pirate's Crossing - Fewest shots while collecting every coin",
        description=f"How well can you putt? Complete Pirate's Crossing in as few shots as possible while collecting every coin",
        format=LeaderboardFormat.VALUE,
        lower_is_better=True
    )
lb.set_start([
        player2_not_barker,
        map == map_pull("Pirate's Crossing"),
        hole_complete.delta() == 0x00,
        hole_complete == 0x01,
        coins_collected == 22
    ])
lb.set_cancel([
        main_pointer >> dword_be(0x19c) == 0x00
    ])
lb.set_submit([
        hole_complete.delta() == 0x00,
        hole_complete == 0x01,
        coins_collected == 22
    ])
lb.set_value([
        measured(shot)
    ])
#mySet.add_leaderboard(lb)

laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

if laptopPath.exists():
    mySet.save(laptopPath)
elif pcPath.exists():
    mySet.save(pcPath)
else:
    mySet.save()