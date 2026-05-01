import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement
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


PRIZE_COUNTER = {
    "prize": ("title", 	"Purchase \"Chuck E. Space\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Helen Run\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Chuck E. Cheese's\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Chuck E. Cheese Doll\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Helen Doll\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Mr. Munch Doll\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Jasper Doll\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Pasqually Doll\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Chuck E.'s Shirt\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Pasqually's Shirt\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Helen's Shirt\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Jasper's Shirt\" from the Prize Counter"),
    "prize": ("title", 	"Purchase \"Mr. Munch's Shirt\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Party Poppers\", \"Rocket\", \"Fortune Cookies\" and \"Soda Can\" from the Prize Counter"),
    "prize": ("title", 	"Purchase the \"Clock\", \"Carpet\" and \"Lights\" for one child from the Prize Counter"),
    "prize": ("You're Really Winning Everything, Huh?",	"Purchase every item as one child from the Prize Counter"),
    "prize": ("title",  "Purchase every item except for the Ultimate Prizes as every child from the Prize Counter"),
}

TROPHIES = {
    "pizza_mania":    ("Master of Pizza Mania",          "Earn the \"Master of Pizza Mania\" trophy by making 1,000 Pizzas"),
    "made_to_order":  ("Master of Made to Order",        "Earn the \"Master of Made to Order\" trophy by serving Chuck E. 500 times"),
    "balloon":        ("Master of Balloon Alphabets",    "Earn the \"Master of Balloon Alphabets\" trophy by completing all of the Alphabets in a single game"),
    "smash_a_munch":  ("Master of Smash-A-Munch",        "Earn the \"Master of Smash a Munch\" trophy by hitting 3,000 Mr. Munch Pegs"),
    "basketball":     ("Master of Basketball",           "Earn the \"Master of Basketball\" trophy by shooting 3,000 Balls into the Basket"),
    "air_hockey":     ("Master of Air Hockey",           "Earn the \"Master of Air Hockey\" trophy by winning 100 games"),
    "alley_roller":   ("Master of Alley Roller",         "Earn the \"Master of Alley Roller\" trophy by rolling 50 Balls into the 50 Points Hole"),
    "mr_munch_tp":    ("Master of Target Practice",      "Earn the \"Master of Mr. Munch's Target Practice\" trophy by shooting 1,000 Mr. Munch Targets"),
    "jaspers_racing": ("Master of Jasper's Racing",      "Earn the \"Master of Jasper's Racing\" trophy by reaching 100,000m"),
    "galaxy_shooter": ("Master of Galaxy Shooter",       "Earn the \"Master of Galaxy Shooter\" trophy by shooting 5,000 Enemy Ships"),
    "dancing_queen":  ("Master of Dancing Queen",        "Earn the \"Master of Dancing Queen with Helen\" trophy by completing Level 4"),
    "cowboy_jasper":  ("Master of Cowboy Jasper",        "Earn the \"Master of Cowboy Jasper\" trophy by catching 3,000 Cows"),
    "counting":       ("Master of Counting",             "Earn the \"Master of Counting\" trophy by answering 1,000 Quizzes correctly"),
    "photo_hunt":     ("Master of Photo Hunt",           "Earn the \"Master of Chuck E. Cheese's Photo Hunt\" trophy by finding 5,000 different spots"),
    "connect_stars":  ("Master of Connect the Stars",    "Earn the \"Master of Connect the Stars\" trophy by completing 1,000 Stars"),
    "matching":       ("Master of Matching",             "Earn the \"Master of Matching\" trophy by matching 1,000 Pairs of Cards"),
    "legend":         ("The Legend of Chuck E. Cheese's","Earn the \"The Legend of Chuck E. Cheese's Party Games\" trophy by purchasing all 10 Ultimate Prizes")

}

HIGH_SCORES = {
    "pizza_mania":    ("Pizza Chef",                     "Make at least 15 Pizzas without making a mistake on the \"Pizza Mania\" minigame"),
    "made_to_order":  ("Short Order Cook",               "Earn a score of at least 700 on the \"Made to Order\" minigame"),
    "balloon":        ("Balloon Animal Artist",          "Earn a score of at least 11,000 on the \"Balloon Alphabet\" minigame"),
    "smash_a_munch":  ("Munch Masher",                   "Smash at least 16 Pegs on the \"Smash a Munch\" minigame"),
    "basketball":     ("Slam Dunk",                      "Shoot at least 60 Balls into the Basket  on the \"Basketball\" minigame"),
    "air_hockey":     ("Puck Pro",                       "Complete Level 4 without the opponent scoring on the \"Air Hockey\" minigame"),
    "alley_roller":   ("Alley Cat",                      "Earn a score of at least 1,800 on the \"Alley Roller\" minigame"),
    "mr_munch_tp":    ("Deadeye",                        "Earn a score of 20,000 on the \"Mr. Munch's Target Practice\" minigame"),
    "jaspers_racing": ("Speed Demon",                    "Drive at least 2,500m on the \"Jasper's Racing\" minigame"),
    "galaxy_shooter": ("Ace Pilot",                      "Earn a score of at least 22,000 on the \"Galaxy Shooter\" minigame"),
    "dancing_queen":  ("Dancing King",                   "Earn a score of at least 13,000 on the \"Dancing Queen with Helen\" minigame"),
    "cowboy_jasper":  ("Cowboy Up",                      "Earn a score of at least 10,000 on the \"Counting\" minigame"),
    "counting":       ("Mathlete",                       "Earn a score of at least 18,000 on the \"Photo Hunt\" minigame"),
    "photo_hunt":     ("Eagle Eye",                      "Catch 32 Cows on the \"Cowboy Jasper\" minigame"),
    "connect_stars":  ("Stargazer",                      "Earn a score of 9,000 on the \"Connect the Stars\" minigame"),
    "matching":       ("Memory Master",                  "Match at least 75 Pairs of Cards on the \"Matching\" minigame"),
}


# --- helpers ---

def title(category: dict, id: str) -> str:
    return category[id][0]

def desc(category: dict, id: str) -> str:
    return category[id][1]

profile = dword_be(0x002600a4)
remember_logic = [
    profile.delta() != 0xffffffff,
    and_next(profile != 0xffffffff),
    add_source(value(0x1adb94)),
    remember(value(0x260) * profile)
]

# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------
 
class Minigame:
    """All save data addresses for a single minigame, bundled together."""
    def __init__(self, name, unlock=None, trophy=None, progress=None,
                 attempts=None, tickets=None, tokens=None, score=None):
        self.name     = name
        self.unlock   = unlock    # byte()
        self.trophy   = trophy    # byte()
        self.progress = progress  # dword_be()
        self.attempts = attempts  # dword_be()
        self.tickets  = tickets   # dword_be()
        self.tokens   = tokens    # dword_be() -- pizza/made-to-order only
        self.score    = score     # dword_be() -- live minigame score
 
    def __repr__(self):
        return f"<Minigame {self.name!r}>"
 
 
class AirHockey:
    """Air Hockey has two scores so it gets its own container."""
    name          = "Air Hockey"
    unlock        = byte(0x023)
    trophy        = byte(0x03B)
    progress      = dword_be(0x068)
    attempts      = dword_be(0x1A4)
    tickets       = dword_be(0x204)
    player_score  = dword_be(0x26013C)
    opponent_score= dword_be(0x260140)
 
    def __repr__(self):
        return "<Minigame 'Air Hockey'>"
 
 
class Cosmetic:
    """Carpet/clock/lights addresses for one character."""
    def __init__(self, name, char_index):
        self.name   = name
        self.carpet = byte(0x14C + char_index * 3 + 0)
        self.clock  = byte(0x14C + char_index * 3 + 1)
        self.lights = byte(0x14C + char_index * 3 + 2)
 
    def __repr__(self):
        return f"<Cosmetic {self.name!r}>"
 
 
class UltimatePrize:
    """Ultimate prize address for one character."""
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = byte(addr)
 
    def __repr__(self):
        return f"<UltimatePrize {self.name!r}>"
 
 
class Shirt:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = byte(addr)
 
    def __repr__(self):
        return f"<Shirt {self.name!r}>"
 
 
class Doll:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = byte(addr)
 
    def __repr__(self):
        return f"<Doll {self.name!r}>"
 
 
class ArcadeGame:
    def __init__(self, name, addr):
        self.name   = name
        self.unlock = byte(addr)
 
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
 
    arcade         = byte(0x24D)
    pizza_mania    = byte(0x24E)
    hall_of_fame   = byte(0x250)
    prizes         = byte(0x252)
    my_room        = byte(0x253)
    lucky_wheel    = byte(0x01E)
 
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
 
    balloon = Minigame(
        name     = "Balloon Alphabet",
        unlock   = bitcount(0x020),
        trophy   = byte(0x038),
        progress = dword_be(0x05C),     # goal: complete all alphabets in 1 game
        attempts = dword_be(0x198),
        tickets  = dword_be(0x1F8),
        score    = dword_be(0x260D24),
    )
 
    smash_a_munch = Minigame(
        name     = "Smash a Munch",
        unlock   = bitcount(0x021),
        trophy   = byte(0x039),
        progress = dword_be(0x060),     # goal: 3,000 pegs
        attempts = dword_be(0x19C),
        tickets  = dword_be(0x1FC),
        score    = dword_be(0x260A14),  # pegs hit
    )
 
    basketball = Minigame(
        name     = "Basketball",
        unlock   = bitcount(0x022),
        trophy   = byte(0x03A),
        progress = dword_be(0x064),     # goal: 3,000 balls
        attempts = dword_be(0x1A0),
        tickets  = dword_be(0x200),
        score    = dword_be(0x2602A4),
    )
 
    air_hockey = AirHockey()
 
    alley_roller = Minigame(
        name     = "Alley Roller",
        unlock   = bitcount(0x024),
        trophy   = byte(0x03C),
        progress = dword_be(0x06C),     # goal: 50x in 50pt hole
        attempts = dword_be(0x1A8),
        tickets  = dword_be(0x208),
        score    = dword_be(0x260214),
    )
 
    mr_munch_target_practice = Minigame(
        name     = "Mr. Munch's Target Practice",
        unlock   = bitcount(0x025),
        trophy   = byte(0x03D),
        progress = dword_be(0x070),     # goal: 1,000 targets
        attempts = dword_be(0x1AC),
        tickets  = dword_be(0x20C),
        score    = dword_be(0x2608C8),
    )
 
    jaspers_racing = Minigame(
        name     = "Jasper's Racing",
        unlock   = bitcount(0x026),
        trophy   = byte(0x03E),
        progress = dword_be(0x074),     # goal: 100,000m
        attempts = dword_be(0x1B0),
        tickets  = dword_be(0x210),
        score    = dword_be(0x260670),  # note: hex / 50-60 for distance
    )
 
    galaxy_shooter = Minigame(
        name     = "Galaxy Shooter",
        unlock   = bitcount(0x027),
        trophy   = byte(0x03F),
        progress = dword_be(0x078),     # goal: 5,000 ships
        attempts = dword_be(0x1B4),
        tickets  = dword_be(0x214),
        score    = dword_be(0x260560),
    )
 
    # -----------------------------------------------------------------------
    # Gameroom 2  (dancing_queen_with_helen -> matching)
    # -----------------------------------------------------------------------
 
    dancing_queen_with_helen = Minigame(
        name     = "Dancing Queen with Helen",
        unlock   = bitcount(0x028),
        trophy   = byte(0x040),
        progress = dword_be(0x07C),     # goal: complete level 4
        attempts = dword_be(0x1B8),
        tickets  = dword_be(0x218),
        score    = dword_be(0x2604A4),
    )
 
    cowboy_jasper = Minigame(
        name     = "Cowboy Jasper",
        unlock   = bitcount(0x02A),
        trophy   = byte(0x042),
        progress = dword_be(0x084),     # goal: 3,000 cows
        attempts = dword_be(0x1C8),
        tickets  = dword_be(0x228),
        score    = dword_be(0x260300),
    )
 
    counting = Minigame(
        name     = "Counting",
        unlock   = bitcount(0x02B),
        trophy   = byte(0x043),
        progress = dword_be(0x088),     # goal: 1,000 correct
        attempts = dword_be(0x1C0),
        tickets  = dword_be(0x220),
        score    = dword_be(0x2604F0),
    )
 
    photo_hunt = Minigame(
        name     = "Photo Hunt",
        unlock   = bitcount(0x02C),
        trophy   = byte(0x044),
        progress = dword_be(0x08C),     # goal: 5,000 spots
        attempts = dword_be(0x1C4),
        tickets  = dword_be(0x224),
        score    = dword_be(0x2608F4),
    )
 
    connect_the_stars = Minigame(
        name     = "Connect the Stars",
        unlock   = bitcount(0x02D),
        trophy   = byte(0x045),
        progress = dword_be(0x090),     # goal: 1,000 stars
        attempts = dword_be(0x1CC),
        tickets  = dword_be(0x22C),
        score    = dword_be(0x2603A4),
    )
 
    matching = Minigame(
        name     = "Matching",
        unlock   = bitcount(0x02E),
        trophy   = byte(0x046),
        progress = dword_be(0x094),     # goal: 1,000 pairs
        attempts = dword_be(0x1D0),
        tickets  = dword_be(0x230),
        score    = dword_be(0x2607CC),
    )

    ticket_blaster = Minigame(
        name     = "Ticket Blaster",
        unlock   = byte(0x248),
        progress = byte(0x249)
    )

 
    # -----------------------------------------------------------------------
    # Pizza games (token-based, not ticket-based)
    # -----------------------------------------------------------------------
 
    pizza_mania_game = Minigame(
        name     = "Pizza Mania",
        unlock   = None,                # unlocked via story, see SaveData.pizza_mania
        trophy   = byte(0x034),
        progress = dword_be(0x04C),     # goal: 1,000 pizzas
        attempts = dword_be(0x188),
        tokens   = dword_be(0x1E8),
        score    = dword_be(0x260E7C),  # pizzas created
    )
 
    made_to_order = Minigame(
        name     = "Made to Order",
        unlock   = None,                # unlocked via story
        trophy   = byte(0x035),
        progress = dword_be(0x050),     # goal: 500 serves
        attempts = dword_be(0x18C),
        tokens   = dword_be(0x1EC),
        score    = dword_be(0x261114),
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
 
    STANDARD_PRIZES = [
        ("flower",           byte(0x124)),
        ("punch_out_robot",  byte(0x125)),
        ("party_poppers",    byte(0x126)),
        ("rocket",           byte(0x127)),
        ("fortune_cookies",  byte(0x128)),
        ("soda_can",         byte(0x129)),
        ("piggy_bank",       byte(0x12A)),
        ("mr_munch_hammer",  byte(0x12B)),
        ("token",            byte(0x12C)),
        ("baseball_glove",   byte(0x12D)),
        ("soap_gun",         byte(0x12E)),
        ("space_globe",      byte(0x12F)),
        ("hanging_mobile",   byte(0x130)),
        ("basketball_item",  byte(0x131)),
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
            enumOver = SaveData.ULTIMATE_PRIZES
            for i, prize in enumerate(enumOver):
                if i == len(enumOver) - 1:
                    logic.append(recall() >> prize.unlock != prize.unlock.delta())
                else:
                    logic.append(recall() >> or_next(prize.unlock != prize.unlock.delta()))
        case "ticket_blaster":
            logic.append(recall() >> SaveData.ticket_blaster.unlock.delta() == 0x00)
            logic.append(recall() >> SaveData.ticket_blaster.unlock == 0x01)
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