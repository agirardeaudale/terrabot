from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Tuple

from terrabot.sim.resource import ResourceDelta

class EventType(Enum):
    # Tiles
    BUILD_DWELLING = auto()
    BUILD_TRADING_POST = auto()
    BUILD_TEMPLE = auto()
    BUILD_STRONGHOLD = auto()
    BUILD_SANCTUARY = auto()
    BUILD_TOWN = auto()
    DIG = auto()

    # Other possibilities:
    # Carpet Ride
    # Tunnel


@dataclass
class EventTrigger:
    listens_for: Tuple[EventType, ...]
    provides: ResourceDelta

    def __init__(self, listens_for: Any, provides: ResourceDelta):
        if isinstance(listens_for, tuple):
            self.listens_for = listens_for
        elif isinstance(listens_for, EventType):
            self.listens_for = tuple([listens_for])
        else:
            raise TypeError("Unrecognized type for parameter listens_for: {type(listens_for)}")

        self.provides = provides


@dataclass
class PassTrigger:
    # Bonus Tiles: Points for structures
    # FAV12: Points for TPs
    # Expansion Bonus Tiles: Points for shipping
    # Engineers: Points for bridges
    pass


class PassTriggerType:
    STRUCTURE = auto()

