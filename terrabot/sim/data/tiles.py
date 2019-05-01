from terrabot.sim.cult import Cult
from terrabot.sim.event import EventTrigger, EventType
from terrabot.sim.resource import ResourceDelta
from terrabot.sim.tile import Tile, TileType, CultBonus

ROUND_TILES = (
        Tile(
                name = "RoundTile-4Water-Spade",
                tile_type = TileType.ROUND,
                cult_bonus = CultBonus(Cult.WATER, 4, bonus_spades=1),
                event_trigger = EventTrigger(
                        listens_for = EventType.BUILD_TRADING_POST,
                        provides = ResourceDelta(victory_points=3))),
        None,
        None,
        None,
        None,
        None,
        None,
        None)

BONUS_TILES = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None)

FAVOR_TILES = ( )

TOWN_TILES = ( )




