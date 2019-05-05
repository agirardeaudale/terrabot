from dataclasses import dataclass
from typing import Tuple

from terrabot.sim.cult import CultDelta, PlayerCultState
from terrabot.sim.event import EventTrigger
from terrabot.sim.map import Terrain
from terrabot.sim.resource import ResourceDelta, PlayerResourceState, _DEFAULT_CONVERSION_RATES,
        LeechOpportunity
from terrabot.sim.structure import PlayerStructureState
from terrabot.sim.tile import Tile, TileSet

@dataclass
class PlayerState:
    dig_level: int = 0
    ship_level: int = 0
    tiles: TileSet = TileSet()
    structures: PlayerStructureState = PlayerStructureState()
    resources: PlayerResourceState = PlayerResourceState()
    cult_state: PlayerCultState = PlayerCultState()
    has_passed: bool = False

    leech_opportunities: Tuple[LeechOpportunity, ...] = ()

    # Cultists. Number of free cult steps the player has to spend.
    cultist_steps: int = 0


@dataclass
class Faction:
    name: str
    home_terrain: Terrain

    starting_ship_level = 0

    max_ship_level: int = 3
    max_dig_level: int = 3

    dwelling_cost: ResourceDelta = ResourceDelta(coins=2, workers=1)
    trading_post_cost_with_neighbors: ResourceDelta = ResourceDelta(coins=3, workers=2)
    trading_post_cost_without_neighbors: ResourceDelta = ResourceDelta(coins=3, workers=2)
    temple_cost: ResourceDelta = ResourceDelta(coins=5, workers=2)
    stronghold_cost: ResourceDelta = ResourceDelta(coins=6, workers=4)
    sanctuary_cost: ResourceDelta = ResourceDelta(coins=6, workers=4)

    shipping_advance_cost: ResourceDelta = ResourceDelta(coins=4, priests=1)
    dig_advance_cost: ResourceDelta = ResourceDelta(coins=5, workers=2, priests=1)

    starting_resources: ResourceDelta = ResourceDelta(coins=15, workers=3, power=7)
    starting_cult_steps: CultDelta = CultDelta()

    zero_dwelling_income: ResourceDelta = ResourceDelta(workers=1)
    dwelling_income: Tuple[ResourceDelta, ...] = tuple([ResourceDelta(workers=1)]) * 8
    trading_post_income: Tuple[ResourceDelta, ...] = (
            ResourceDelta(coins=2, power=1),
            ResourceDelta(coins=2, power=1),
            ResourceDelta(coins=2, power=2),
            ResourceDelta(coins=2, power=2))
    temple_income: Tuple[ResourceDelta, ...] = tuple([ResourceDelta(priests=1)]) * 3
    stronghold_income: ResourceDelta = ResourceDelta(power=2)
    sanctuary_income: ResourceDelta = ResourceDelta(priests=1)

    # Alchemists
    resource_conversion_rates: frozendict = _DEFAULT_CONVERSION_RATES

    # Chaos Magicians
    place_last: bool = False

    def get_shipping(self, player_state: PlayerState) -> int:
        return ship_level + 1

    def get_dig_cost(self, player_state: PlayerState) -> ResourceDelta:
        default_cost_workers = 3 - player_state.dig_level
        return ResourceDelta(workers=default_cost_workers)

    def get_special_actions(self, player_state: PlayerState) -> Tuple[str, ...]:
        """Returns special actions available to the player even if they have been used this round,
        but not if they haven't been unlocked by e.g. building a stronghold.
        """
        return ()

    def get_event_triggers(self, player_state: PlayerState) -> Tuple[EventTrigger, ...]:
        return ()


@dataclass
class PlayerMetadata:
    name: str


@dataclass
class Player:
    player_metadata: PlayerMetadata
    initial_turn_position: int # zero-indexed
    player_id: str # e.g. "player1"
    faction: Faction # None indicates that factions have not yet been chosen
    player_state: PlayerState # None indicates that starting resources, factions, etc are unset

    @staticmethod
    def create(
            player_metadata: PlayerMetadata,
            initial_turn_position: int,
            faction: Faction = None):
        player_id = Player.create_player_id(initial_turn_position)
        return Player(player_metadata, initial_turn_position, player_id, None, None)

    @staticmethod
    def create_player_id(initial_turn_position: int) -> str:
        return f"player{initial_turn_position}"

    def update_structures(self, new_structures: PlayerStructureState) -> "Player":
        return self.replace(player_state = self.player_state.replace(structures = new_structures)

    def update_resources(self, new_resources: PlayerResourceState) -> "Player":
        return self.replace(player_state = self.player_state.replace(resources = new_resources)

    def update_cult(self, new_cult: PlayerCultState) -> "Player":
        return self.replace(player_state = self.player_state.replace(cult_state = new_cult)

