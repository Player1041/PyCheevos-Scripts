from pycheevos.core.helpers import *
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.leaderboard import Leaderboard
from pycheevos.models.set import AchievementSet
from notes_10713 import *

my_set = AchievementSet(game_id=10713, title="Imported Leaderboards")

# --- LB: Small Board Clear ---
lb_162918_start = [
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
    (tile_counter == 0x00),
    (byte(0x0342) == 0x00),
]
lb_162918_cancel = [
    (value(0x00) == 0x01),
]
lb_162918_submit = [
    (value(0x00) == 0x00),
]
lb_162918_value = [
    add_source(byte(0x0328).bcd()),
    measured(byte(0x0327).bcd()),
]
lb_162918 = Leaderboard(
    title="""Small Board Clear""",
    description="""How fast can you clear a small board?""",
    id=162918,
    format=LeaderboardFormat.VALUE,
    lower_is_better=False
)
lb_162918.set_start(lb_162918_start)
lb_162918.set_cancel(lb_162918_cancel)
lb_162918.set_submit(lb_162918_submit)
lb_162918.set_value(lb_162918_value)
my_set.add_leaderboard(lb_162918)

# --- LB: Medium Board Clear ---
lb_162919_start = [
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
    (tile_counter == 0x00),
    (byte(0x0342) == 0x01),
]
lb_162919_cancel = [
    (value(0x00) == 0x01),
]
lb_162919_submit = [
    (value(0x00) == 0x00),
]
lb_162919_value = [
    add_source(byte(0x0328).bcd()),
    measured(byte(0x0327).bcd()),
]
lb_162919 = Leaderboard(
    title="""Medium Board Clear""",
    description="""How fast can you clear a medium board?""",
    id=162919,
    format=LeaderboardFormat.VALUE,
    lower_is_better=False
)
lb_162919.set_start(lb_162919_start)
lb_162919.set_cancel(lb_162919_cancel)
lb_162919.set_submit(lb_162919_submit)
lb_162919.set_value(lb_162919_value)
my_set.add_leaderboard(lb_162919)

# --- LB: Hard Board Clear ---
lb_162920_start = [
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
    (tile_counter == 0x00),
    (byte(0x0342) == 0x02),
]
lb_162920_cancel = [
    (value(0x00) == 0x01),
]
lb_162920_submit = [
    (value(0x00) == 0x00),
]
lb_162920_value = [
    add_source(byte(0x0328).bcd()),
    measured(byte(0x0327).bcd()),
]
lb_162920 = Leaderboard(
    title="""Hard Board Clear""",
    description="""How fast can you clear a hard board?""",
    id=162920,
    format=LeaderboardFormat.VALUE,
    lower_is_better=False
)
lb_162920.set_start(lb_162920_start)
lb_162920.set_cancel(lb_162920_cancel)
lb_162920.set_submit(lb_162920_submit)
lb_162920.set_value(lb_162920_value)
my_set.add_leaderboard(lb_162920)

my_set.save()