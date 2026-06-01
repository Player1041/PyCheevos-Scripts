from pycheevos.core.helpers import *
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.achievement import Achievement
from pycheevos.models.set import AchievementSet
from notes_10713 import *

my_set = AchievementSet(game_id=10713, title="Imported Achievements")

# --- Entry-Level Explosives ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_Z:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=0
ach_608412_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_next_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x00),
]
ach_608412 = Achievement(
    title="""Entry-Level Explosives""",
    description="""Complete the small board without pressing reveal on a revealed tile""",
    points=2, type=AchievementType.PROGRESSION,
    id=608412, badge="690201"
)
ach_608412.add_core(ach_608412_logic)
my_set.add_achievement(ach_608412)

# --- Medium Rare ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_Z:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=1
ach_608410_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_next_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x01),
]
ach_608410 = Achievement(
    title="""Medium Rare""",
    description="""Complete the medium board without pressing reveal on a revealed tile""",
    points=4, type=AchievementType.PROGRESSION,
    id=608410, badge="690199"
)
ach_608410.add_core(ach_608410_logic)
my_set.add_achievement(ach_608410)

# --- Full Clearance ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_Z:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=2
ach_608411_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_next_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x02),
]
ach_608411 = Achievement(
    title="""Full Clearance""",
    description="""Complete the large board without pressing reveal on a revealed tile""",
    points=5, type=AchievementType.PROGRESSION,
    id=608411, badge="690200"
)
ach_608411.add_core(ach_608411_logic)
my_set.add_achievement(ach_608411)

# --- Unmarked Territory ---
# Logic: 0xH0342=0_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0SK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031dSK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:0xQ0182=1_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xQ0182=1_I:{recall}_N:0xR0182=0_R:d0xH1fb5!=10
ach_608407_logic = [
    (byte(0x0342) == 0x00),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
]
ach_608407_alt1 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
]
ach_608407_alt2 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    add_address(recall()),
    and_next((grid_bounds == 0x00)),
    reset_if((byte(0x1fb5).delta() != 0x0a)),
]
ach_608407 = Achievement(
    title="""Unmarked Territory""",
    description="""Complete the small board without placing any flags and without pressing reveal on a revealed tile""",
    points=5,
    id=608407, badge="690196"
)
ach_608407.add_core(ach_608407_logic)
ach_608407.add_alt(ach_608407_alt1)
ach_608407.add_alt(ach_608407_alt2)
my_set.add_achievement(ach_608407)

# --- No Flags? No Problem! ---
# Logic: 0xH0342=1_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0SK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031dSK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:0xQ0182=1_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xQ0182=1_I:{recall}_N:0xR0182=0_R:d0xH1fb5!=10
ach_608409_logic = [
    (byte(0x0342) == 0x01),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
]
ach_608409_alt1 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
]
ach_608409_alt2 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    add_address(recall()),
    and_next((grid_bounds == 0x00)),
    reset_if((byte(0x1fb5).delta() != 0x0a)),
]
ach_608409 = Achievement(
    title="""No Flags? No Problem!""",
    description="""Complete the medium board without placing any flags and without pressing reveal on a revealed tile""",
    points=5,
    id=608409, badge="690198"
)
ach_608409.add_core(ach_608409_logic)
ach_608409.add_alt(ach_608409_alt1)
ach_608409.add_alt(ach_608409_alt2)
my_set.add_achievement(ach_608409)

# --- The Purist ---
# Logic: 0xH0342=2_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0SK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031dSK:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:0xQ0182=1_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xQ0182=1_I:{recall}_N:0xR0182=0_R:d0xH1fb5!=10
ach_608408_logic = [
    (byte(0x0342) == 0x02),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
]
ach_608408_alt1 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
]
ach_608408_alt2 = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds == 0x01)),
    add_address(recall()),
    and_next((grid_bounds == 0x00)),
    reset_if((byte(0x1fb5).delta() != 0x0a)),
]
ach_608408 = Achievement(
    title="""The Purist""",
    description="""Complete the large board without placing any flags and without pressing reveal on a revealed tile""",
    points=10,
    id=608408, badge="690197"
)
ach_608408.add_core(ach_608408_logic)
ach_608408.add_alt(ach_608408_alt1)
ach_608408.add_alt(ach_608408_alt2)
my_set.add_achievement(ach_608408)

# --- Speed Sweeper ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=0_R:0xH0327>=144
ach_608413_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x00),
    reset_if((byte(0x0327) >= 0x90)),
]
ach_608413 = Achievement(
    title="""Speed Sweeper""",
    description="""Complete the small board without pressing reveal on a revealed tile within 90 seconds""",
    points=5,
    id=608413, badge="690206"
)
ach_608413.add_core(ach_608413_logic)
my_set.add_achievement(ach_608413)

# --- I Got Light Grey, Medium Grey and Dark Grey! ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=1_N:0xH0328>=1_R:0xH0327>=128
ach_608414_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x01),
    and_next((byte(0x0328) >= 0x01)),
    reset_if((byte(0x0327) >= 0x80)),
]
ach_608414 = Achievement(
    title="""I Got Light Grey, Medium Grey and Dark Grey!""",
    description="""Complete the medium board without pressing reveal on a revealed tile within 180 seconds""",
    points=5,
    id=608414, badge="690207"
)
ach_608414.add_core(ach_608414_logic)
my_set.add_achievement(ach_608414)

# --- Bomb Disposal Expert ---
# Logic: K:d0xH0317*d0xH0312_K:{recall}+d0xH0316_I:{recall}_N:d0xU0182>=3_K:0xH0317*0xH0312_K:{recall}+0xH0316_I:{recall}_N:0xU0182>=3_N:d0xH1fb5!=10_R:0x 031d<d0x 031d_0xH0181=1.1._N:d0x 031d=1_T:0x 031d=0_0xH0342=2_N:0xH0328>=3_R:0xH0327>=96
ach_608415_logic = [
    remember(byte(0x0317).delta()),
    remember(recall()+d0x0316),
    add_address(recall()),
    and_next((grid_bounds.delta() >= 0x03)),
    remember(byte(0x0317)),
    remember(recall()+0x0316),
    add_address(recall()),
    and_next((grid_bounds >= 0x03)),
    and_next((byte(0x1fb5).delta() != 0x0a)),
    reset_if((tile_counter < tile_counter.delta())),
    (used_to_check_board_loading == 0x01).with_hits(1),
    and_next((tile_counter.delta() == 0x01)),
    trigger((tile_counter == 0x00)),
    (byte(0x0342) == 0x02),
    and_next((byte(0x0328) >= 0x03)),
    reset_if((byte(0x0327) >= 0x60)),
]
ach_608415 = Achievement(
    title="""Bomb Disposal Expert""",
    description="""Complete the large board without pressing reveal on a revealed tile within 360 seconds""",
    points=10,
    id=608415, badge="690208"
)
ach_608415.add_core(ach_608415_logic)
my_set.add_achievement(ach_608415)

my_set.save()