from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

class Cult(Enum):
    FIRE = auto()
    WATER = auto()
    EARTH = auto()
    AIR = auto()


@dataclass
class CultDelta:
    steps: Tuple[Cult, ...] = ()

    def by_cult(self, cult) -> int:
        return self.steps.count(cult)


@dataclass
class PlayerCultState:
    fire: int = 0
    water: int = 0
    earth: int = 0
    air: int = 0

    def by_cult(self, cult) -> Cult:
        if cult == Cult.FIRE:
            return self.fire
        elif cult == Cult.WATER:
            return self.water
        elif cult == Cult.EARTH:
            return self.earth
        elif cult == Cult.AIR:
            return self.air
        else:
            raise AssertionError("Unrecognized Cult")


@dataclass
class CultTrackState:
    player_states: Tuple[PlayerCultState, ...]
    priest_slots_fire: Tuple[str, str, str, str]
    priest_slots_fire: Tuple[str, str, str, str]

    def for_player(player_label: str) -> PlayerCultState:
        return


