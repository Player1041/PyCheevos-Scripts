from pycheevos.models.set import AchievementSet, Leaderboard
from pycheevos.models.achievement import Achievement
from pycheevos.core.helpers import byte, pause_if, reset_if, word, dword, trigger, value
from pycheevos.core.constants import AchievementType, LeaderboardFormat
from pathlib import Path

set = AchievementSet(29055, "~Hack~ PSXFunkin: Lullaby Mod")
platform = "Wii"

screen_id_fully_loaded = byte(0x1e437c)
screen_id = byte(0x1e437d)
MENU = (2)
STORY = (3)
FREE_PLAY = (4)
IN_GAME = (7)

song_id = byte(0x1e4398)
SAFTEY_LULLABY = (0)
LEFT_UNCHECKED = (1)
MONOCHROME = (2)
MISSINGNO = (3)
songs = {
    0: "Saftey Lullaby",
    1: "Left Unchecked",
    2: "Monochrome",
    3: "Missingno"
}

difficulty = byte(0x1e4399)
EASY = (0)
NORMAL = (1)
HARD = (2)
diffs = {
    0: "Easy",
    1: "Normal",
    2: "Hard"
}

ghost_tap = byte(0x1e4438)
OFF = (0)
ON = (1)

game_mode = byte(0x1e443c)
NORMAL_MODE = (0)
SWAP_MODE = (1)
TWO_PLAYER_MODE = (2)
modes = {
    0: "Normal",
    1: "Swap"
}

health = word(0x1e4538)
combo = word(0x1e453a)

score = dword(0x1e4540)

end_flag = byte(0x1fff90)

def get_score():
    return score * 10

def song_clear(id: int, prime=False):
    if not prime:
        return song_id == id and screen_id == IN_GAME and end_flag.delta() == (0) and end_flag == (1)
    elif prime:
        return [
            song_id == id,
            screen_id == IN_GAME,
            trigger(end_flag.delta() == (0)),
            trigger(end_flag == (1))
        ]

def prog_cheevo(song_id: int, title: str, points: int):
    ach = Achievement(
        title,
        "Clear " + songs[song_id],
        points,
        type=AchievementType.PROGRESSION
    )

    ach.add_core([
        ghost_tap == OFF,
        game_mode != TWO_PLAYER_MODE,
        song_clear(song_id)
    ])

    set.add_achievement(ach)

def fc_cheevo(s_id: int, title: str, points: int, mode=NORMAL_MODE):
    description = "Clear " + songs[s_id] + " without any misses on Hard and "
    if mode == NORMAL_MODE:
        description = description + "Normal Mode"
    elif mode == SWAP_MODE:
        description = description + "Swap Mode"

    ach = Achievement(
        title,
        description,
        points,
    )

    ach.add_core([
        ghost_tap == OFF,
        game_mode == mode,
        difficulty == HARD,
        song_clear(s_id, False),
        (pause_if(health < health.delta)).with_hits(1)
    ])

    ach.add_alt([
        reset_if(screen_id != IN_GAME),
        reset_if(song_id != s_id)
    ])

    set.add_achievement(ach)

def lb(s_id: int, diff: int, mode: int):
    title = "[" + diffs[diff] + ", " + modes[mode] + " Mode] " + songs[s_id] + " - Highest Score"
    description = "Get the highest score on this song!"

    lb = Leaderboard(
        title,
        description,
        format=LeaderboardFormat.VALUE
    )

    lb.set_start([
        ghost_tap == OFF,
        game_mode == mode,
        difficulty == difficulty,
        song_clear(s_id)
    ])

    lb.set_cancel(value(0) == value(1))
    lb.set_submit(value(0) == value(0))

    lb.set_value(score * value(10))

    set.add_leaderboard(lb)

for song in range(4):
    for diff in range(3):
        for mode in range(2):
            lb(song, diff, mode)



prog_cheevo(SAFTEY_LULLABY, "Saftey Lullaby", 1)



dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

match platform:
    case "Wii":
        if dolphinPath.exists():
            set.save(dolphinPath)
    case default:
        if laptopPath.exists():
            set.save(laptopPath)
        elif pcPath.exists():
            set.save(pcPath)
        else:
            set.save()