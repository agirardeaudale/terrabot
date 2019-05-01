from dataclasses import dataclass
from enum import Enum, auto
from random import sample
from typing import Iterator, Tuple
from weakref import proxy, ProxyType

from terrabot.sim.data.actions import STANDARD_ACTIONS, POWER_ACTIONS
from terrabot.sim.data.maps import DEFAULT_MAP
from terrabot.sim.data.tiles import FAVOR_TILES, TOWN_TILES, BONUS_TILES, ROUND_TILES
from terrabot.sim.action import Action, ActionExecution, Phase, Step
from terrabot.sim.cult import CultDelta
from terrabot.sim.map import Map
from terrabot.sim.player import Player, PlayerMetadata
from terrabot.sim.tile import Tile, TileSet
from terrabot.sim.resource import ResourceDelta, Conversion
from terrabot.util import shuffled

@dataclass
class Setup:
    round_tiles: Tuple[Tile, Tile, Tile, Tile, Tile, Tile]
    bonus_tiles: Tuple[Tile, ...]

    @staticmethod
    def create_random_setup(num_players: int) -> "Setup":
        round_tiles = tuple(sample(ROUND_TILES, 6))
        bonus_tiles = tuple(sample(BONUS_TILES, num_players + 3))

        return Setup(round_tiles, bonus_tiles)


@dataclass
class LogEntry:
    description: str
    active_player: Player = None
    previous_state: "GameState" = None # Actually ProxyMappingType[GameState]
    resulting_state: "GameState" = None # Actually ProxyMappingType[GameState]


@dataclass
class GameState:
    players: Tuple[Player, ...]
    num_players: int
    setup: Setup
    pool: TileSet
    round: int = 0
    active_player: Player = None
    map: Map = DEFAULT_MAP
    phase: Phase = Phase.SELECT_FACTION

    # History
    previous_state: "GameState" = None
    log: Tuple[LogEntry, ...] = None

    # Action slots
    expended_action_slots: Tuple[str, ...] = ()

    @staticmethod
    def create(
            player_metadata: Iterator[PlayerMetadata],
            randomize_turn_order: bool = True,
            setup: Setup = None):

        shuffled_player_metadata = tuple(
                shuffled(player_metadata) if randomize_turn_order else player_metadata)
        players = [Player.create(x, pos) for x, pos in enumerate(shuffled_player_metadata)]
        num_players = len(player_metadata)

        setup = setup if setup is not None else Setup.create_random_setup(num_players)
        pool = TileSet(
                bonus_tiles = setup.bonus_tiles,
                favor_tiles = FAVOR_TILES,
                town_tiles = TOWN_TILES)

        return GameState(
                players = players,
                active_player = players[0],
                num_players = num_players,
                setup = setup,
                pool = pool)

    def get_available_actions(self) -> Tuple[Action, ...]:
        if self.phase != Phase.TURN:
            return self.get_applicable_off_turn_action()
        else:
            power_actions = self.get_available_power_actions()
            special_actions = self.get_available_special_actions()
            return STANDARD_ACTIONS + power_actions + special_actions

    def get_available_power_actions(self) -> Tuple[Action, ...]:
        return (x for x in POWER_ACTIONS if x.action_id not in self.expended_action_slots)

    def get_available_special_actions(self) -> Tuple[Action, ...]:
        # TODO
        pass

    def get_applicable_off_turn_action(self) -> Tuple[Action, ...]:
        # TODO
        pass

    def submit(self,
            action_execution: ActionExecution,
            conversions: Iterator[Conversion] = frozenset(),
            leech_decisions: Iterator[bool] = ()) -> "GameState":
        # TODO
        pass

    def _reflect_step(self, step: Step) -> "GameState":
        # TODO
        pass

    def _get_active_player(self):
        return self.players[self.active_player]

#    def _get_next_player(self):
#        return active_player + 1 if active_player < self.num_players else 1


