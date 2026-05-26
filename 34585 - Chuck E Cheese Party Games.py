import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
from pycheevos.models.leaderboard import Leaderboard
from pathlib import Path
import struct

mySet = AchievementSet(game_id=34585, title="Chuck E. Cheese's Party Games")
platform = "Wii"

PROGRESSION = {
    "intro":          ("Welcome to Chuck E. Cheese's!",  "Complete all of the Basic Tutorials and unlock Chuck E. Cheese's Hall of Fame"),
    "gameroom_1":     ("Prize Winner",                   "Unlock all of the Game Room 1 games"),
    "gameroom_2":     ("Make Yourself at Home",          "Unlock all of the Game Room 2 games"),
    "ultimate_prize":   ("Hall of Famer",                  "Purchase the Ultimate Prize from the Prize Counter"),
    "ticket_blaster": ("Ticket Blaster!",                "Earn a play on the Ticket Buster")
}


GAMES = {
    "space": ("To Infinity and Cheese!", 	"Purchase \"Chuck E. Space\" from the Prize Counter"),
    "helen": ("Super Helen Run", 	"Purchase \"Helen Run\" from the Prize Counter"),
    "chuck": ("It's Chuck E!", 	"Purchase \"Chuck E. Cheese's\" from the Prize Counter"),
}

DOLLS = {
    "chuck_doll": ("Huggable Icon", 	"Purchase the \"Chuck E. Cheese Doll\" from the Prize Counter"),
    "helen_doll": ("Best Friend: Plush Edition", 	"Purchase the \"Helen Doll\" from the Prize Counter"),
    "mr_munch_doll": ("Stuff This Guy", 	"Purchase the \"Mr. Munch Doll\" from the Prize Counter"),
    "jasper_doll": ("Ain't Nothing But a Hound Dog", 	"Purchase the \"Jasper Doll\" from the Prize Counter"),
    "pasqually_doll": ("He Comes with the Set", 	"Purchase the \"Pasqually Doll\" from the Prize Counter"),
}
SHIRTS = {
    "chuck_shirt": ("Dress to Impress", 	"Purchase \"Chuck E.'s Shirt\" from the Prize Counter"),
    "pasqually_shirt": ("Chef's Wardrobe", 	"Purchase \"Pasqually's Shirt\" from the Prize Counter"),
    "helen_shirt": ("Fashion Forward", 	"Purchase \"Helen's Shirt\" from the Prize Counter"),
    "jasper_shirt": ("Country Couture", 	"Purchase \"Jasper's Shirt\" from the Prize Counter"),
    "mr_munch_shirt": ("This Is My Munching Shirt", 	"Purchase \"Mr. Munch's Shirt\" from the Prize Counter"),
}
EXTRAS = {
    "extras": ("Party Animal", 	"Purchase the \"Party Poppers\", \"Rocket\", \"Fortune Cookies\" and \"Soda Can\" from the Prize Counter"),
    "decor": ("Interior Decorator", 	"Purchase the \"Clock\", \"Carpet\" and \"Lights\" for one child from the Prize Counter"),
    "one_child": ("You're Really Winning Everything, Huh?",	"Purchase every item as one child from the Prize Counter"),
    "everyone": ("Everyone Gets a Prize!",  "Purchase every item except for the Ultimate Prizes as every child from the Prize Counter"),
}

TROPHIES = {
    "pizza_mania":    ("A Thousand Pizzas Deep",          "Earn the \"Master of Pizza Mania\" trophy by making 1,000 Pizzas"),
    "made_to_order":  ("At Your Service, Chuck",        "Earn the \"Master of Made to Order\" trophy by serving Chuck E. 500 times"),
    "balloon":        ("A to Z, Call Me Amazon",    "Earn the \"Master of Balloon Alphabets\" trophy by completing all of the Alphabets in a single game"),
    "smash_a_munch":  ("Three Thousand Pegs of Fury",        "Earn the \"Master of Smash a Munch\" trophy by hitting 3,000 Mr. Munch Pegs"),
    "basketball":     ("Nothing but Net",           "Earn the \"Master of Basketball\" trophy by shooting 3,000 Balls into the Basket"),
    "air_hockey":     ("Undisputed!",           "Earn the \"Master of Air Hockey\" trophy by winning 100 games"),
    "alley_roller":   ("Fifty Times ",         "Earn the \"Master of Alley Roller\" trophy by rolling 50 Balls into the 50 Points Hole"),
    "mr_munch_tp":    ("Mr. Munch's Worst Nightmare",      "Earn the \"Master of Mr. Munch's Target Practice\" trophy by shooting 1,000 Mr. Munch Targets"),
    "jaspers_racing": ("Jasper Motorsports",      "Earn the \"Master of Jasper's Racing\" trophy by reaching 100,000m"),
    "galaxy_shooter": ("5,000 Down",       "Earn the \"Master of Galaxy Shooter\" trophy by shooting 5,000 Enemy Ships"),
    "dancing_queen":  ("You Can Dance, You Can Jive, Having the Time of Your Life",        "Earn the \"Master of Dancing Queen with Helen\" trophy by completing Level 4"),
    "cowboy_jasper":  ("The Lone Ranger",        "Earn the \"Master of Cowboy Jasper\" trophy by catching 3,000 Cows"),
    "counting":       ("I Can Only Count to 4!",             "Earn the \"Master of Counting\" trophy by answering 1,000 Quizzes correctly"),
    "photo_hunt":     ("Found You!",           "Earn the \"Master of Chuck E. Cheese's Photo Hunt\" trophy by finding 5,000 different spots"),
    "connect_stars":  ("Wishing Upon a Star",    "Earn the \"Master of Connect the Stars\" trophy by completing 1,000 Stars"),
    "matching":       ("Two by Two",             "Earn the \"Master of Matching\" trophy by matching 1,000 Pairs of Cards"),
    "legend":         ("The Legend of Chuck E. Cheese's","Earn the \"The Legend of Chuck E. Cheese's Party Games\" trophy by purchasing all 10 Ultimate Prizes")
}



HIGH_SCORES = {
    "pizza_mania":    ("Pizza Chef",              "Earn at least 50 tokens on the \"Pizza Mania\" minigame", 50, 0),
    "made_to_order":  ("Short Order Cook",        "Earn a score of at least 700 on the \"Made to Order\" minigame", 700, 0),
    "balloon":        ("Balloon Animal Artist",   "Earn a score of at least 11,000 on the \"Balloon Alphabet\" minigame", 11000 , 0),
    "smash_a_munch":  ("Munch Masher",            "Smash at least 167 Pegs on the \"Smash a Munch\" minigame", 167, 1),
    "basketball":     ("Slam Dunk",               "Shoot at least 60 Balls into the Basket  on the \"Basketball\" minigame", 60, 0),
    "air_hockey":     ("Puck Pro",                "Complete Level 4 without the opponent scoring on the \"Air Hockey\" minigame", None, 0),
    "alley_roller":   ("Alley Cat",               "Earn a score of at least 1,800 on the \"Alley Roller\" minigame", 1800, 0),
    "mr_munch_tp":    ("Deadeye",                 "Earn a score of 20,000 on the \"Mr. Munch's Target Practice\" minigame", 20000 , 0),
    "jaspers_racing": ("Speed Demon",             "Drive at least 2,500m on the \"Jasper's Racing\" minigame", 125000, 0),
    "galaxy_shooter": ("Ace Pilot",               "Earn a score of at least 22,000 on the \"Galaxy Shooter\" minigame", 22000, 0),
    "dancing_queen":  ("Dancing Queen",            "Earn a score of at least 13,000 on the \"Dancing Queen with Helen\" minigame", 13000, 0),
    "cowboy_jasper":  ("Giddy Up, Cowboy",                "Earn a score of at least 10,000 on the \"Counting\" minigame", 10000, 0),
    "counting":       ("Mathlete",               "Earn a score of at least 18,000 on the \"Photo Hunt\" minigame", 18000, 0),
    "photo_hunt":     ("Eagle Eye",       "Catch 32 Cows on the \"Cowboy Jasper\" minigame", 32, 0),
    "connect_stars":  ("Stargazer",               "Earn a score of 9,000 on the \"Connect the Stars\" minigame", 9000, 0),
    "matching":       ("Memory Master",           "Match at least 75 Pairs of Cards on the \"Matching\" minigame", 75, 1),
}

# --- helpers ---

def title(category: dict, id: str) -> str:
    return category[id][0]

def desc(category: dict, id: str) -> str:
    return category[id][1]

profile = dword_be(0x002600a4)
remember_logic = [
    and_next(profile == profile.delta()),
    add_source(value(0x1adb94)),
    remember(value(0x260) * profile)
]

def get_mode_hex(mode: str) -> str:
    indicators = {
        "pizza_mania":    "PM.",
        "made_to_order":  "MTO",
        "balloon":        "BA.",
        "smash_a_munch":  "SM.",
        "basketball":     "BB.",
        "air_hockey":     "AH.",
        "alley_roller":   "AR.",
        "mr_munch_tp":    "MTP",
        "jaspers_racing": "JRC",
        "galaxy_shooter": "GST",
        "dancing_queen":  "DQ.",
        "cowboy_jasper":  "CB.",
        "counting":       "FM.",
        "photo_hunt":     "PH.",
        "connect_stars":  "DC.",
        "matching":       "MC.",
    }
    ascii_str = indicators.get(mode.strip().lower())
    return "0x" + "".join(f"{ord(c):02x}" for c in ascii_str) if ascii_str else f"Unknown mode: '{mode}'"

# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------
 
class Minigame:
    """All save data addresses for a single minigame, bundled together."""
    def __init__(self, name, unlock=None, trophy=None, trophy_goal=None, progress=None,
                 attempts=None, tickets=None, tokens=None, score=None, state=None,
                 tickets_state=None):
        self.name          = name
        self.unlock        = unlock    # byte()
        self.trophy        = trophy    # byte()
        self.trophy_goal   = trophy_goal  # int or None if no progress check for trophy
        self.progress      = progress  # dword_be()
        self.attempts      = attempts  # dword_be()
        self.tickets       = tickets   # dword_be()
        self.tokens        = tokens    # dword_be() -- pizza/made-to-order only
        self.score         = score     # dword_be() -- live minigame score
        self.state         = state     # dword_be() or byte() -- live minigame state
        self.tickets_state = tickets_state  # int -- state value when the tickets screen is shown
 
    def __repr__(self):
        return f"<Minigame {self.name!r}>"
 
 
class AirHockey:
    """Air Hockey has two scores so it gets its own container."""
    name          = "Air Hockey"
    unlock        = bitcount(0x023)
    trophy        = byte(0x03B)
    trophy_goal   = 0x64          # 100 wins
    progress      = dword_be(0x068)
    attempts      = dword_be(0x1A4)
    tickets       = dword_be(0x204)
    player_score  = dword_be(0x26013C)
    opponent_score= dword_be(0x260140)
    level         = dword_be(0x2600f8)
    state         = dword_be(0x2600FC)
    tickets_state = 0x06
    # 0x00 - Not in a game
    # 0x02 - Loading in/Ready
    # 0x03 - Playing
    # 0x04 - Next Level
    # 0x05 - Game Over
    # 0x06 - Tickets
 
    def __repr__(self):
        return "<Minigame 'Air Hockey'>"
 
 
class Cosmetic:
    """Carpet/clock/lights addresses for one character."""
    def __init__(self, name, char_index):
        self.name   = name
        self.carpet = bitcount(0x14C + char_index * 3 + 0)
        self.clock  = bitcount(0x14C + char_index * 3 + 1)
        self.lights = bitcount(0x14C + char_index * 3 + 2)
 
    def __repr__(self):
        return f"<Cosmetic {self.name!r}>"
 
 
class UltimatePrize:
    """Ultimate prize address for one character."""
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = bitcount(addr)
 
    def __repr__(self):
        return f"<UltimatePrize {self.name!r}>"
 
 
class Shirt:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = bitcount(addr)
 
    def __repr__(self):
        return f"<Shirt {self.name!r}>"
 
 
class Doll:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = bitcount(addr)
 
    def __repr__(self):
        return f"<Doll {self.name!r}>"
 
 
class ArcadeGame:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = bitcount(addr)
 
    def __repr__(self):
        return f"<ArcadeGame {self.name!r}>"
 
 
# ---------------------------------------------------------------------------
# SaveData
# ---------------------------------------------------------------------------
 
class SaveData:
 
    CHARACTERS = [
        "Ming", "Russel", "Tommy", "Neil", "Nukul",
        "Arial", "Farah", "Jenny", "Hikaru", "Abbie"
    ]
 
    UNLOCK = {0: "Locked", 1: "Unlocked", 2: "Unlocked (New)"}
    PRIZE  = {0: "Locked", 1: "Bought",   2: "Bought (New)"}
 
    # -----------------------------------------------------------------------
    # Player / currency
    # -----------------------------------------------------------------------
 
    character_id = byte(0x011)
    tokens       = dword_be(0x014)
    tickets      = dword_be(0x018)
 
    # -----------------------------------------------------------------------
    # Unlocked content
    # -----------------------------------------------------------------------
 
    arcade         = bitcount(0x24D)
    pizza_mania    = bitcount(0x24E)
    hall_of_fame   = bitcount(0x250)
    prizes         = bitcount(0x252)
    my_room        = bitcount(0x253)
    lucky_wheel    = bitcount(0x01E)
 
    # -----------------------------------------------------------------------
    # Story progress
    # -----------------------------------------------------------------------
 
    progress = byte(0x25D)
 
    # -----------------------------------------------------------------------
    # Legend trophy
    # -----------------------------------------------------------------------
 
    trophy_legend   = byte(0x047)
    progress_legend = dword_be(0x098)   # goal: 10 ultimate prizes
 
    # -----------------------------------------------------------------------
    # Gameroom 1  (balloon -> galaxy_shooter)
    # -----------------------------------------------------------------------


    ticket_blaster = Minigame(
        name     = "Ticket Blaster",
        unlock   = byte(0x248),
        progress = byte(0x249)
    )

    balloon = Minigame(
        name         = "Balloon Alphabet",
        unlock       = bitcount(0x020),
        trophy       = bitcount(0x038),
        trophy_goal  = None,                # balloon: no progress check
        progress     = dword_be(0x05C),
        attempts     = dword_be(0x198),
        tickets      = dword_be(0x1F8),
        score         = dword_be(0x260D24),
        state         = dword_be(0x260D18),
        tickets_state = 0x06,
        # 0x01 - Ready
        # 0x02 - Playing
        # 0x03 - Next Level
        # 0x04 - ??
        # 0x05 - Game Over
        # 0x06 - Tickets
        # 0x07 - Unloading
    )

    smash_a_munch = Minigame(
        name         = "Smash a Munch",
        unlock       = bitcount(0x021),
        trophy       = bitcount(0x039),
        trophy_goal  = 0xBB8,               # 3,000 pegs
        progress     = dword_be(0x060),
        attempts     = dword_be(0x19C),
        tickets      = dword_be(0x1FC),
        score         = dword_be(0x260A14),
        state         = dword_be(0x260A0C),
        tickets_state = 0x04,
        # 0x01 - Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Tickets
        # 0x05 - Unloading
    )

    basketball = Minigame(
        name         = "Basketball",
        unlock       = bitcount(0x022),
        trophy       = bitcount(0x03A),
        trophy_goal  = 0xBB8,               # 3,000 balls
        progress     = dword_be(0x064),
        attempts     = dword_be(0x1A0),
        tickets      = dword_be(0x200),
        score         = dword_be(0x2602A4),
        state         = dword_be(0x26023F),
        tickets_state = 0x04,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Tickets
        # 0x05 - Unloading
    )

    air_hockey = AirHockey()
    # AirHockey.trophy_goal = 0x64          # 100 wins -- set on the class directly if needed

    alley_roller = Minigame(
        name         = "Alley Roller",
        unlock       = bitcount(0x024),
        trophy       = bitcount(0x03C),
        trophy_goal  = 0x32,                # 50x in 50pt hole
        progress     = dword_be(0x06C),
        attempts     = dword_be(0x1A8),
        tickets      = dword_be(0x208),
        score         = dword_be(0x260214),
        state         = dword_be(0x2601B0),
        tickets_state = 0x04,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Increase in level
        # 0x04 - Tickets
    )

    mr_munch_target_practice = Minigame(
        name         = "Mr. Munch's Target Practice",
        unlock       = bitcount(0x025),
        trophy       = bitcount(0x03D),
        trophy_goal  = 0x3E8,               # 1,000 targets
        progress     = dword_be(0x070),
        attempts     = dword_be(0x1AC),
        tickets      = dword_be(0x20C),
        score         = dword_be(0x2608C8),
        state         = dword_be(0x2608A4),
        tickets_state = 0x05,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Increase in level
        # 0x04 - Time's Up!
        # 0x05 - Tickets
        # 0x06 - Unloading
    )

    jaspers_racing = Minigame(
        name         = "Jasper's Racing",
        unlock       = bitcount(0x026),
        trophy       = bitcount(0x03E),
        trophy_goal  = 0x186A0,             # 100,000m
        progress     = dword_be(0x074),
        attempts     = dword_be(0x1B0),
        tickets      = dword_be(0x210),
        score         = dword_be(0x260670),
        state         = dword_be(0x260668),
        tickets_state = 0x04,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Increase in level
        # 0x04 - Tickets
        # 0x05 - Unloading
    )

    galaxy_shooter = Minigame(
        name         = "Galaxy Shooter",
        unlock       = bitcount(0x027),
        trophy       = bitcount(0x03F),
        trophy_goal  = 0x1388,              # 5,000 ships
        progress     = dword_be(0x078),
        attempts     = dword_be(0x1B4),
        tickets      = dword_be(0x214),
        score         = dword_be(0x260560),
        state         = dword_be(0x260548),
        tickets_state = 0x04,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Tickets
        # 0x05 - Unloading
    )

    dancing_queen_with_helen = Minigame(
        name         = "Dancing Queen with Helen",
        unlock       = bitcount(0x028),
        trophy       = bitcount(0x040),
        trophy_goal  = None,                # dancing queen: no progress check (complete level 4)
        progress     = dword_be(0x07C),
        attempts     = dword_be(0x1B8),
        tickets      = dword_be(0x218),
        score         = dword_be(0x2604A4),
        state         = dword_be(0x2604A0),
        tickets_state = 0x06,
        # 0x00 - Not in a game
        # 0x01 - Ready
        # 0x02 - In game
        # 0x05 - Game over
        # 0x06 - Tickets
    )

    cowboy_jasper = Minigame(
        name         = "Cowboy Jasper",
        unlock       = bitcount(0x02A),
        trophy       = bitcount(0x042),
        trophy_goal  = 0xBB8,               # 3,000 cows
        progress     = dword_be(0x084),
        attempts     = dword_be(0x1C8),
        tickets      = dword_be(0x228),
        score         = dword_be(0x260300),
        state         = dword_be(0x2602D8),
        tickets_state = 0x04,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Tickets
        # 0x05 - Unloading
    )

    counting = Minigame(
        name         = "Counting",
        unlock       = bitcount(0x02B),
        trophy       = bitcount(0x043),
        trophy_goal  = 0x3E8,               # 1,000 correct
        progress     = dword_be(0x088),
        attempts     = dword_be(0x1C0),
        tickets      = dword_be(0x220),
        score         = dword_be(0x2604F0),
        state         = dword_be(0x2604B0),
        tickets_state = 0x05,
        # 0x00 - Not in a game
        # 0x01 - Ready
        # 0x02 - In game
        # 0x03 - Game Over
        # 0x04 - Unloading
        # 0x05 - Tickets
    )

    photo_hunt = Minigame(
        name         = "Photo Hunt",
        unlock       = bitcount(0x02C),
        trophy       = bitcount(0x044),
        trophy_goal  = 0x1388,              # 5,000 spots
        progress     = dword_be(0x08C),
        attempts     = dword_be(0x1C4),
        tickets      = dword_be(0x224),
        score         = dword_be(0x2608F4),
        state         = dword_be(0x2608D8),
        tickets_state = 0x06,
        # 0x00 - Not in a game
        # 0x01 - Start
        # 0x02 - Unused
        # 0x03 - New photo inbound
        # 0x04 - Playing
        # 0x05 - Game Over
        # 0x06 - Tickets
    )

    connect_the_stars = Minigame(
        name         = "Connect the Stars",
        unlock       = bitcount(0x02D),
        trophy       = bitcount(0x045),
        trophy_goal  = 0x3E8,               # 1,000 stars
        progress     = dword_be(0x090),
        attempts     = dword_be(0x1CC),
        tickets      = dword_be(0x22C),
        score         = dword_be(0x2603A4),
        state         = dword_be(0x260384),
        tickets_state = 0x07,
        # 0x00 - Not in a game
        # 0x01 - Loading in/Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Unloading
        # 0x07 - Tickets
    )

    matching = Minigame(
        name         = "Matching",
        unlock       = bitcount(0x02E),
        trophy       = bitcount(0x046),
        trophy_goal  = 0x3E8,               # 1,000 pairs
        progress     = dword_be(0x094),
        attempts     = dword_be(0x1D0),
        tickets      = dword_be(0x230),
        score         = dword_be(0x2607CC),
        state         = dword_be(0x2607B0),
        tickets_state = 0x07,
        # 0x01 - Ready
        # 0x02 - New level
        # 0x03 - New pair appearing
        # 0x04 - Showing card
        # 0x05 - Choosing cards
        # 0x06 - Game over
        # 0x07 - Tickets
        # 0x0a - Unloading
    )

    pizza_mania_game = Minigame(
        name         = "Pizza Mania",
        unlock       = None,
        trophy       = bitcount(0x034),
        trophy_goal  = 0x3E8,               # 1,000 pizzas
        progress     = dword_be(0x04C),
        attempts     = dword_be(0x188),
        tokens       = dword_be(0x1E8),
        score        = dword_be(0x260E7C),
        # No state address found in memory map
    )

    made_to_order = Minigame(
        name         = "Made to Order",
        unlock       = None,
        trophy       = bitcount(0x035),
        trophy_goal  = 0x1F4,               # 500 serves
        progress     = dword_be(0x050),
        attempts     = dword_be(0x18C),
        tokens       = dword_be(0x1EC),
        score         = word_be(0x00260dbc),
        state         = byte(0x260DB9),
        tickets_state = 0x04,
        # 0x01 - Ready
        # 0x02 - Playing
        # 0x03 - Game Over
        # 0x04 - Tokens
        # 0x05 - Unloading
    )
 
    # -----------------------------------------------------------------------
    # Global live score
    # -----------------------------------------------------------------------
 
    tickets_earned = dword_be(0x2610C0)
 
    # -----------------------------------------------------------------------
    # Prizes: ultimate (one per character)
    # -----------------------------------------------------------------------
 
    ULTIMATE_PRIZES = [
        UltimatePrize("Ming",    0x0AC),
        UltimatePrize("Russel",  0x0AD),
        UltimatePrize("Tommy",   0x0AE),
        UltimatePrize("Neil",    0x0AF),
        UltimatePrize("Nukul",   0x0B0),
        UltimatePrize("Ariel",   0x0B1),
        UltimatePrize("Farah",   0x0B2),
        UltimatePrize("Jenny",   0x0B3),
        UltimatePrize("Hikaru",  0x0B4),
        UltimatePrize("Abbie",   0x0B5),
    ]
 
    # -----------------------------------------------------------------------
    # Prizes: shirts
    # -----------------------------------------------------------------------
 
    SHIRTS = [
        Shirt("Chuck E.",   0x132),
        Shirt("Pasqually",  0x133),
        Shirt("Helen",      0x134),
        Shirt("Jasper",     0x135),
        Shirt("Mr. Munch",  0x136),
    ]
 
    # -----------------------------------------------------------------------
    # Prizes: dolls
    # -----------------------------------------------------------------------
 
    DOLLS = [
        Doll("Chuck E.",   0x137),
        Doll("Helen",      0x138),
        Doll("Mr. Munch",  0x139),
        Doll("Jasper",     0x13A),
        Doll("Pasqually",  0x13B),
    ]
 
    # -----------------------------------------------------------------------
    # Prizes: arcade game unlocks
    # -----------------------------------------------------------------------
 
    ARCADE_GAMES = [
        ArcadeGame("Chuck E. Space",    0x13D),
        ArcadeGame("Helen Run",         0x13E),
        ArcadeGame("Chuck E. Cheese's", 0x13F),
    ]
 
    # -----------------------------------------------------------------------
    # Prizes: standard (no grouping needed, iterable list)
    # -----------------------------------------------------------------------
 
    EXTRAS = [
        ("party_poppers",    bitcount(0x126)),
        ("rocket",           bitcount(0x127)),
        ("fortune_cookies",  bitcount(0x128)),
        ("soda_can",         bitcount(0x129)),
    ]

    STANDARD_PRIZES = [
        ("flower",           bitcount(0x124)),
        ("punch_out_robot",  bitcount(0x125)),
        ("piggy_bank",       bitcount(0x12A)),
        ("mr_munch_hammer",  bitcount(0x12B)),
        ("token",            bitcount(0x12C)),
        ("baseball_glove",   bitcount(0x12D)),
        ("soap_gun",         bitcount(0x12E)),
        ("space_globe",      bitcount(0x12F)),
        ("hanging_mobile",   bitcount(0x130)),
        ("basketball_item",  bitcount(0x131)),
    ]
 
    # -----------------------------------------------------------------------
    # Cosmetics (per character)
    # -----------------------------------------------------------------------
 
    COSMETICS = [
        Cosmetic(name, i)
        for i, name in enumerate(CHARACTERS)
    ]
 
    # -----------------------------------------------------------------------
    # Iterable groups
    # -----------------------------------------------------------------------
 
    GAMEROOM_1 = [
        smash_a_munch,
        basketball,
        air_hockey,
        alley_roller,
        mr_munch_target_practice,
        jaspers_racing,
        galaxy_shooter,
    ]
 
    GAMEROOM_2 = [
        balloon,
        dancing_queen_with_helen,
        cowboy_jasper,
        counting,
        photo_hunt,
        connect_the_stars,
        matching,
    ]
 
    PIZZA_GAMES = [
        pizza_mania_game,
        made_to_order,
    ]
 
    # All arcade minigames in one flat list if needed
    ALL_MINIGAMES = GAMEROOM_1 + GAMEROOM_2 + PIZZA_GAMES

TROPHY_MINIGAMES = {
    "pizza_mania":    SaveData.pizza_mania_game,
    "made_to_order":  SaveData.made_to_order,
    "balloon":        SaveData.balloon,
    "smash_a_munch":  SaveData.smash_a_munch,
    "basketball":     SaveData.basketball,
    "air_hockey":     SaveData.air_hockey,
    "alley_roller":   SaveData.alley_roller,
    "mr_munch_tp":    SaveData.mr_munch_target_practice,
    "jaspers_racing": SaveData.jaspers_racing,
    "galaxy_shooter": SaveData.galaxy_shooter,
    "dancing_queen":  SaveData.dancing_queen_with_helen,
    "cowboy_jasper":  SaveData.cowboy_jasper,
    "counting":       SaveData.counting,
    "photo_hunt":     SaveData.photo_hunt,
    "connect_stars":  SaveData.connect_the_stars,
    "matching":       SaveData.matching,
}


for x in PROGRESSION:
    logic = []
    ach = Achievement(title(PROGRESSION, x), desc(PROGRESSION, x), 2)
    logic.append(remember_logic)
    match x:
        case "intro":
            logic.append(recall() >> (SaveData.progress.delta() == 0x0b))
            logic.append(recall() >> (SaveData.progress == 0x0c))
        case "gameroom_1":
            enumOver = SaveData.GAMEROOM_1
            for i, game in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> game.unlock.delta() == (len(enumOver) - 1))
                else:
                    logic.append(recall() >> add_source(game.unlock.delta()))
            for i, game in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> measured(game.unlock == len(enumOver)))
                else:
                    logic.append(recall() >> add_source(game.unlock))
        case "gameroom_2":
            enumOver = SaveData.GAMEROOM_2
            for i, game in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> game.unlock.delta() == (len(enumOver) - 1))
                else:
                    logic.append(recall() >> add_source(game.unlock.delta()))
            for i, game in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> measured(game.unlock == len(enumOver)))
                else:
                    logic.append(recall() >> add_source(game.unlock))
        case "ultimate_prize":
            logic = []
            logic.append(value(0x00) == value(0x00))
            for i, prize in enumerate(SaveData.ULTIMATE_PRIZES):
                alt = []
                alt.append(remember_logic)
                alt.append(recall() >> (SaveData.character_id == i))
                alt.append(recall() >> (prize.unlock.delta() == 0))
                alt.append(recall() >> (prize.unlock == 1))
                ach.add_alt(alt)
        case "ticket_blaster":
            logic.append(recall() >> SaveData.ticket_blaster.unlock.delta() == 0x00)
            logic.append(recall() >> SaveData.ticket_blaster.unlock == 0x01)
    ach.add_core(logic)
    #mySet_add_achievement(ach)   


for (key, (ach_title, ach_desc)), prize in zip(GAMES.items(), SaveData.ARCADE_GAMES):
    logic = []
    ach = Achievement(ach_title, ach_desc, 1)
    logic.append(remember_logic)
    logic.append(recall() >> prize.unlock > prize.unlock.delta())
    ach.add_core(logic)
    #mySet_add_achievement(ach)

for (key, (ach_title, ach_desc)), doll in zip(DOLLS.items(), SaveData.DOLLS):
    logic = []
    ach = Achievement(ach_title, ach_desc, 1)
    logic.append(remember_logic)
    logic.append(recall() >> doll.unlock > doll.unlock.delta())
    ach.add_core(logic)
    #mySet_add_achievement(ach)

for (key, (ach_title, ach_desc)), shirt in zip(SHIRTS.items(), SaveData.SHIRTS):
    logic = []
    ach = Achievement(ach_title, ach_desc, 1)
    logic.append(remember_logic)
    logic.append(recall() >> shirt.unlock > shirt.unlock.delta())
    ach.add_core(logic)
    #mySet_add_achievement(ach)

for x in EXTRAS:
    logic = []
    ach = Achievement(title(EXTRAS, x), desc(EXTRAS, x), 2)
    logic.append(remember_logic)
    match x:
        case "extras":
            enumOver = SaveData.EXTRAS
            for i, (name, prize) in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> prize.delta() == (len(enumOver) - 1))
                else:
                    logic.append(recall() >> add_source(prize.delta()))
            for i, (name, prize) in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> prize == len(enumOver))
                else:
                    logic.append(recall() >> add_source(prize))
        case "decor":
            logic = []
            logic.append(value(0x00) == value(0x00))
            for i, cosmetic in enumerate(SaveData.COSMETICS):
                alt = []
                alt.append(remember_logic)
                alt.append(recall() >> (SaveData.character_id == i))
                # trigger: at least one item was just purchased (0 -> non-zero)
                alt.append(recall() >> add_source(cosmetic.carpet.delta()))
                alt.append(recall() >> add_source(cosmetic.clock.delta()))
                alt.append(recall() >> (cosmetic.lights.delta() == 2))  # last in chain, no add_source
                # state: all 3 are now bought (1 or 2)
                alt.append(recall() >> add_source(cosmetic.carpet))
                alt.append(recall() >> add_source(cosmetic.clock))
                alt.append(recall() >> (cosmetic.lights == 3))
                ach.add_alt(alt)

        case "one_child":
            logic = []
            logic.append(value(0x00) == value(0x00))
            _std = dict(SaveData.STANDARD_PRIZES)
            global_items = (
                    [g.unlock for g in SaveData.ARCADE_GAMES] +
                    [d.unlock for d in SaveData.DOLLS] +
                    [s.unlock for s in SaveData.SHIRTS] +
                    [p for _, p in SaveData.EXTRAS]
            )
            for i, cosmetic in enumerate(SaveData.COSMETICS):
                alt = []
                alt.append(remember_logic)
                alt.append(recall() >> (SaveData.character_id == i))
                cosmetic_items = [cosmetic.carpet, cosmetic.clock, cosmetic.lights]
                all_items = global_items + cosmetic_items
                for i, item in enumerate(all_items):
                    if i == len(all_items) - 1:
                        alt.append(recall() >> item.delta() == len(all_items) - 1)
                    else:
                        alt.append(recall() >> add_source(item.delta()))
                for i, item in enumerate(all_items):
                    if i == len(all_items) - 1:
                        alt.append(recall() >> measured(item == len(all_items)))
                    else:
                        alt.append(recall() >> add_source(item))
                ach.add_alt(alt)
        case "everyone":
            _std = dict(SaveData.STANDARD_PRIZES)
            global_items = (
                    [g.unlock for g in SaveData.ARCADE_GAMES] +
                    [d.unlock for d in SaveData.DOLLS] +
                    [s.unlock for s in SaveData.SHIRTS] +
                    [p for _, p in SaveData.EXTRAS]
            )
            cosmetic_items = []
            for i, cosmetic in enumerate(SaveData.COSMETICS):
                cosmetic_items.extend([cosmetic.carpet, cosmetic.clock, cosmetic.lights])
            all_items = global_items + cosmetic_items

            for i, item in enumerate(all_items):
                    if i == len(all_items) - 1:
                        logic.append(recall() >> item.delta() == len(all_items) - 1)
                    else:
                        logic.append(recall() >> add_source(item.delta()))
            for i, item in enumerate(all_items):
                    if i == len(all_items) - 1:
                        logic.append(recall() >> measured(item == len(all_items)))
                    else:
                        logic.append(recall() >> add_source(item))
    ach.add_core(logic)
    #mySet_add_achievement(ach)  

for x in TROPHIES:
    logic = []
    ach = Achievement(title(TROPHIES, x), desc(TROPHIES, x), 5)
    logic.append(remember_logic)
    match x:
        case "balloon":
            logic.append(recall() >> SaveData.balloon.trophy.delta() == 0)
            logic.append(recall() >> SaveData.balloon.trophy == 1)
        case "legend":
            logic.append(recall() >> SaveData.trophy_legend.delta() == 0)
            logic.append(recall() >> SaveData.trophy_legend == 1)
            logic.append(recall() >> measured(SaveData.progress_legend == 10))
        case _:
            mg = TROPHY_MINIGAMES[x]
            logic.append(recall() >> mg.trophy.delta() == 0)
            logic.append(recall() >> mg.trophy == 1)
            if mg.trophy_goal is not None:
                logic.append(recall() >> measured(mg.progress >= mg.trophy_goal))

    ach.add_core(logic)
    #mySet_add_achievement(ach)

for key, (ach_title, ach_desc, goal, increment) in HIGH_SCORES.items():
    logic = []
    ach = Achievement(ach_title, ach_desc, 5)
    mg = TROPHY_MINIGAMES[key]
    mode = int(get_mode_hex(key), 16)
    match key:
        case "air_hockey":
            logic.append((tbyte_be(0x001b1053) == mode))
            logic.append((SaveData.air_hockey.level == 0).with_hits(1))
            logic.append(reset_if(SaveData.air_hockey.opponent_score != 0))
            logic.append((SaveData.air_hockey.player_score > SaveData.air_hockey.opponent_score))
            logic.append((SaveData.air_hockey.level == 3))
            logic.append((float32_be(0x00260144) == 5400.0))
        case _:
            logic.append((tbyte_be(0x001b1053) == mode))
            logic.append((mg.score.delta() < goal))
            logic.append(mg.score >= goal)

    ach.add_core(logic)
    #mySet_add_achievement(ach)

for key, mg in TROPHY_MINIGAMES.items():
    match key:
        case "air_hockey":
            pass
        case "pizza_mania":
            pass
        case _:
            mode = int(get_mode_hex(key), 16)
            startLogic = []
            lb = Leaderboard(f"High Score - {mg.name}", "Score your highest!")

            startLogic.append((tbyte_be(0x001b1053) == mode))

            startLogic.append(mg.score != 0)  # any score value will do, just need to trigger on the right minigame
            startLogic.append(mg.state.delta() != mg.tickets_state)  # trigger when the tickets screen is shown, which is the last state before leaving the game and where the final score is stored)
            startLogic.append(mg.state == mg.tickets_state)  # trigger when the tickets screen is shown, which is the last state before leaving the game and where the final score is stored)
            lb.set_start(startLogic)

            lb.set_cancel(value(0x00) == value(0x01))
            lb.set_submit(value(0x00) == value(0x00))  # no special trigger for submit, just need to be in the right mode

            match key:
                case "jaspers_racing":
                    lb.set_value(measured(mg.score / value(0x32)))
                case _:
                    lb.set_value(measured(mg.score))

            #mySet_add_leaderboard(lb)


# Rich Presence



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