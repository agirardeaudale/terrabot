from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

from frozendict import frozendict

class StructureType(Enum):
    DWELLING = auto()
    TRADING_POST = auto()
    TEMPLE = auto()
    SANCTUARY = auto()
    STRONGHOLD = auto()
    BRIDGE = auto()


@dataclass
class Structure:
    structure_type: StructureType
    location: str # by location_id


@dataclass
class PlayerStructureState:
    structures: Tuple[Structure, ...] = ()
    location_mapping: frozendict = frozendict()
    type_mapping: frozendict = frozendict()

    def __init__(self, structures: Tuple[Structure, ...] = ()):
        self.structures = structures
        self.location_mapping = frozendict({s.location: s for s in structures})
        self.type_mapping = frozendict(
                {st: (s for s in structures if s.structure_type == st) for st in StructureType})



