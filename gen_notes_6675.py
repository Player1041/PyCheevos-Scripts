saveSlotEntry = [0x001fade4]

levelNames = {
    "Rolling River Creek": ["Frogger", "Positive", "Rolling River Creek"],
    "Bog Town": ["Bruiser", "Pike Fish", "Bog Town"],
    "Slick Willy's River Boat": ["Slick Willy", "Lumpy", "Slick Willy's Riverboat"],
    "River Town": ["Snakes", "Scat", "River Town"],
    "Mushroom Valley": ["Fairy Frog Mother", "Mrs. Boxy", "Mushroom Valley"],
    "Fairy Town in Spring": ["Phroi", "Lilly", "Fairy Town"],
    "The Tree of Knowledge": ["Mrs. Fine", "Mr. D", "Tree of Knowledge"],
    "Fairy Town in Summer": ["Mrs. Stein", "Dusty", "Long River"],
    "The Cat Dragon's Lair": ["Wuku", "Hiss", "Cat Dragon's Lair"],
    "Fairy Town in Autumn": ["Princess Holly", "Geeky Bill", "Third Kingdom"],
    "The Dark Trail Ruins": ["Wild Thing", "Bone Cruncher", "Ruins of Dark Trail"],
    "Dr. Starkenstein's Castle": ["Dr. Starkenstein", "Metal Chicken Ray", "Dr. Darkenstein's Castle"],
    "The Catacombs": ["Count Blah", "Princess Dar", "Catacombs"],
    "Goblin Trail": ["Itty Bitty", "Bumbly Dumbly", "Goblin Trail"],
    "The Goblin Fort": ["King Ijnek", "Big Bertha", "Joy Town"],
    "Joy Castle": ["Sir Ian", "Magical General", "Joy Castle"],
    "The Towers of Joy Castle": ["Princess Joy", "Grim Bite", "Battle for Joy Castle"]
}

teamOffsets = [
    (0x0,  "[32-bit] {area} - {item1} Price"),
    (0x50, "[32-bit] {area} - {item2} Price"),
    (0xa0, "[32-bit] {area} - {item3} Price")
]

output_lines = []

for slot_index, base_address in enumerate(saveSlotEntry, start=1):
    for area_index, (area, (item1, item2, item3)) in enumerate(levelNames.items()):
        print(f"{hex(area_index)} - {area}")
        area_base = base_address + (area_index * 0xf0)
        for offset, desc_template in teamOffsets:
            final_address = area_base + offset
            description = desc_template.format(area=area, item1=item1, item2=item2, item3=item3)
            formatted_line = f'N0:0x{final_address:x}:"{description}"'
            output_lines.append(formatted_line)

for line in output_lines:
    print(line)

with open("output.txt", "w") as f:
    f.write("\n".join(output_lines))

print(f"\n\nTotal entries generated: {len(output_lines)}")
print("Output written to output.txt")