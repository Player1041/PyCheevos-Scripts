start = 0x009b2da4

achievements = [
    "Wood!",
    "Rockin' It",
    "Smudged",
    "Going Deeper",
    "Shiny!",
    "Deep Find",
    "Ew, Gross",
    "Soft",
    "Getting Started",
    "Stone Age",
    "Iron Will",
    "Golden Touch",
    "Best Pick",
    "Lumberjack",
    "Stone Chopper",
    "Iron Woodsman",
    "Gold Logger",
    "Final Cut",
    "En Garde!",
    "Stone Warrior",
    "Knight's Blade",
    "All That Glitters",
    "Excalibur",
    "Digging Dirt",
    "Stone Digger",
    "Hard Labor",
    "Gilded Spade",
    "Six Feet Deep",
    "Getting Crafty",
    "Smelting",
    "Heating Up",
    "On the Anvil",
    "An Apple a Day",
    "Baker",
    "Let There Be Light",
    "Ahh, My Eyes",
    "Pack Rat",
    "Going Under",
    "Deeper Darkness",
    "Into the Deep",
    "Sky High",
    "Air Apparent",
    "One More Turn...",
    "Back for More",
    "Respawned",
    "Hungry?",
    "Under the Water",
    "Slime Slayer",
    "Frostbite",
    "Zombie Killer",
    "Frozen Dead",
    "Monster Hunter",
    "Green Thumb",
    "Botanist",
    "Hidden Achievement 1",
    "Hidden Achievement 2",
    "Power Within",
    "And That's a Wrap!",
    "Nice Try",
    "Prickly Up Here",
    "Snowball Fight!",
    "Well That Was Quick!?",
]

lines = []
for i, name in enumerate(achievements):
    base = start + i * 0xc
    unlocked_note = ""
    timestamp_note = ""
    playtime_note  = ""
    lines.append(f'N0:0x{base:08x}:"{unlocked_note}"')
    lines.append(f'N0:0x{base + 0x4:08x}:"{timestamp_note}"')
    lines.append(f'N0:0x{base + 0x8:08x}:"{playtime_note}"')

with open("notes_output.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {len(lines)} entries to notes_output.txt")