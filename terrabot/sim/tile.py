from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

from terrabot.sim.event import EventTrigger, PassTrigger
from terrabot.sim.cult import Cult, CultDelta
from terrabot.sim.resource import ResourceDelta

class TileType(Enum):
    ROUND = auto()
    BONUS = auto()
    FAVOR = auto()
    TOWN = auto()


@dataclass
class CultBonus:
    cult: Cult
    steps: int
    bonus_resources: ResourceDelta = ResourceDelta()
    bonus_spades: int = 0


@dataclass
class Tile:
    name: str
    tile_type: TileType
    action_slot: str = None # by action_id
    event_trigger: EventTrigger = None
    pass_trigger: PassTrigger = None
    immediate_resources = ResourceDelta()
    immediate_cult = CultDelta()
    income: ResourceDelta = ResourceDelta()
    shipping_modifier: int = 0
    town_size_modifier: int = 0
    cult_bonus: CultBonus = None


@dataclass
class TileSet:
    bonus_tiles: Tuple[Tile, ...] = ()
    favor_tiles: Tuple[Tile, ...] = ()
    town_tiles: Tuple[Tile, ...] = ()

    def get_all(self) -> Tuple[Tile, ...]:
        return self.bonus_tiles + self.favor_tiles + self.town_tiles

