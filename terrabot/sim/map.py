from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple
from weakref import proxy, ProxyType

from frozendict import frozendict

from terrabot.sim.structure import StructureType

class Terrain(Enum):
    MOUNTAIN = auto()
    DESERT = auto()
    FIELD = auto()
    SWAMP = auto()
    LAKE = auto()
    FOREST = auto()
    WASTELAND = auto()


@dataclass
class Location:
    location_id: str

    # Unclear if map.py classes should be aware of whether a player has built on a given location.
    # Right now this information is duplicated in the Location and PlayerStructureState classes.
    built_by_player: str # player_id
    structure_type: StructureType # don't necessarily need both this and built_by_player


@dataclass
class Hex(Location):
    adjacent_hexes: Tuple["Hex", ...] # Actually Tuple[ProxyType[Hex], ...]
    bridge_slots: Tuple["BridgeSlot", ...] # Actually Tuple[ProxyType[BridgeSlot], ...]
    terrain: Terrain

    def get_hexes_within_shipping(self, shipping_level: int) -> Tuple["Hex", ...]:
        pass

    def get_hexes_of_distance(self, distance, exclude_river: bool = True) -> Tuple["Hex", ...]:
        """Distance defined as-the-crow-flies. Useful for e.g. the Dwarves or Fakirs."""
        pass

    def get_hexes_distance_two(self, exclude_river: bool = True) -> Tuple["Hex", ...]:
        return self.get_hexes_of_distance(2, exclude_river)

    def get_hexes_distance_three(self, exclude_river: bool = True) -> Tuple["Hex", ...]:
        return self.get_hexes_of_distance(3, exclude_river)


@dataclass
class BridgeSlot(Location):
    connected_hexes: Tuple[Hex, Hex]


@dataclass
class Map:
    locations: frozendict = frozendict()
    hexes: Tuple[Hex, ...] = ()
    bridge_slots: Tuple[BridgeSlot, ...] = ()

    def __init__(self, hexes: Tuple[Hex, ...], bridge_slots: Tuple[BridgeSlot, ...]):
        self.hexes = hexes
        self.bridge_slots = bridge_slots
        self.locations = {x.location_id: x for x in hexes + bridge_slots}


_adjacent_terrains = frozendict({
    Terrain.MOUNTAIN: (Terrain.WASTELAND, Terrain.DESERT),
    Terrain.DESERT: (Terrain.MOUNTAIN, Terrain.FIELD),
    Terrain.FIELD: (Terrain.DESERT, Terrain.SWAMP),
    Terrain.SWAMP: (Terrain.FIELD, Terrain.LAKE),
    Terrain.LAKE: (Terrain.SWAMP, Terrain.FOREST),
    Terrain.FOREST: (Terrain.LAKE, Terrain.WASTELAND),
    Terrain.WASTELAND: (Terrain.FOREST, Terrain.MOUNTAIN)})

