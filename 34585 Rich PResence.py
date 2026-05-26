from pycheevos.core.helpers import *
from pycheevos.core.helpers import tbyte_be, dword_be, word_be, value
from pycheevos.models.rich_presence import RichPresence
 
# ---------------------------------------------------------------------------
# Minigame mode indicators (3-char ASCII packed into a tbyte)
# ---------------------------------------------------------------------------
 
def mode_val(key: str) -> int:
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
    s = indicators[key]
    return int("0x" + "".join(f"{ord(c):02x}" for c in s), 16)
 
# ---------------------------------------------------------------------------
# Memory addresses (mirrored from SaveData / main script)
# ---------------------------------------------------------------------------
 
mode_addr   = tbyte_be(0x001b1053)
tickets_addr = "N:0xG002600a4=d0xG002600a4_A:1760148_K:608*0xG002600a4_I:{recall}_M:0xG0000018"       # SaveData.tickets
tokens_addr  = "N:0xG002600a4=d0xG002600a4_A:1760148_K:608*0xG002600a4_I:{recall}_M:0xG0000014"     # SaveData.tokens
 
# Scores keyed by mode key
SCORES = {
    "pizza_mania":    dword_be(0x260E7C),
    "made_to_order":  word_be(0x00260dbc),
    "balloon":        dword_be(0x260D24),
    "smash_a_munch":  dword_be(0x260A14),
    "basketball":     dword_be(0x2602A4),
    "air_hockey":     dword_be(0x26013C),   # player score
    "alley_roller":   dword_be(0x260214),
    "mr_munch_tp":    dword_be(0x2608C8),
    "jaspers_racing": dword_be(0x260670),   # raw distance; divide by 50 for display
    "galaxy_shooter": dword_be(0x260560),
    "dancing_queen":  dword_be(0x2604A4),
    "cowboy_jasper":  dword_be(0x260300),
    "counting":       dword_be(0x2604F0),
    "photo_hunt":     dword_be(0x2608F4),
    "connect_stars":  dword_be(0x2603A4),
    "matching":       dword_be(0x2607CC),
}
 
# Display names for each minigame
NAMES = {
    "pizza_mania":    "Pizza Mania",
    "made_to_order":  "Made to Order",
    "balloon":        "Balloon Alphabet",
    "smash_a_munch":  "Smash a Munch",
    "basketball":     "Basketball",
    "air_hockey":     "Air Hockey",
    "alley_roller":   "Alley Roller",
    "mr_munch_tp":    "Mr. Munch's Target Practice",
    "jaspers_racing": "Jasper's Racing",
    "galaxy_shooter": "Galaxy Shooter",
    "dancing_queen":  "Dancing Queen with Helen",
    "cowboy_jasper":  "Cowboy Jasper",
    "counting":       "Counting",
    "photo_hunt":     "Chuck E. Cheese's Photo Hunt",
    "connect_stars":  "Connect the Stars",
    "matching":       "Matching",
}
 
# Score label per minigame (shown before the value)
SCORE_LABELS = {
    "pizza_mania":    "Tokens",
    "made_to_order":  "Score",
    "balloon":        "Score",
    "smash_a_munch":  "Pegs",
    "basketball":     "Balls",
    "air_hockey":     "Score",
    "alley_roller":   "Score",
    "mr_munch_tp":    "Score",
    "jaspers_racing": "Distance",
    "galaxy_shooter": "Score",
    "dancing_queen":  "Score",
    "cowboy_jasper":  "Cows",
    "counting":       "Score",
    "photo_hunt":     "Score",
    "connect_stars":  "Score",
    "matching":       "Pairs",
}
 
# ---------------------------------------------------------------------------
# Build rich presence
# ---------------------------------------------------------------------------
 
rp = RichPresence()
 
# Formats
rp.add_format("Score",    "VALUE")
rp.add_format("Tickets",  "VALUE")
rp.add_format("Tokens",   "VALUE")
rp.add_format("Distance", "VALUE")
 
# One conditional display per minigame
for key, name in NAMES.items():
    mv     = mode_val(key)
    score  = SCORES[key]
    label  = SCORE_LABELS[key]
    cond   = (mode_addr == mv).render()
 
    if key == "jaspers_racing":
        score_str = f"{label}: @Distance({(score / value(0x32)).render()})m"
    else:
        score_str = f"{label}: @Score({score.render()})"
 
    tickets_str = f"🎫 @Tickets({tickets_addr})"  # :ticketemoji:
    tokens_str  = f"🪙 @Tokens({tokens_addr})"  # :coinemoji:
 
    text = f"Playing the {name} machine | {score_str} | {tickets_str} | {tokens_str}"
    rp.add_display(cond, text)
 
# Default fallback
rp.add_display(None, f"Browsing Chuck E. Cheese's | 🎫 @Tickets({tickets_addr}) | 🪙 @Tokens({tokens_addr})")
 
print(rp.render())
 