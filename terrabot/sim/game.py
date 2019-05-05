from dataclasses import dataclass, field
from enum import Enum, auto
from random import sample
from sets import Set
from typing import Iterator, Tuple
from weakref import proxy, ProxyType

from terrabot.sim.data.actions import STANDARD_ACTIONS, POWER_ACTIONS, \
        get_off_turn_action_by_phase
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
    active_player_id: str
    lines: Iterable[str, ...]
    # previous_state: "GameState" = None # Actually ProxyMappingType[GameState]
    # resulting_state: "GameState" = None # Actually ProxyMappingType[GameState]


@dataclass
class GameState:
    players: Set[Player, ...]
    num_players: int
    setup: Setup
    pool: TileSet
    active_player_position: int = 0
    round: int = 0
    map: Map = DEFAULT_MAP
    phase: Phase = Phase.SELECT_FACTION

    # History
    previous_state: "GameState" = None
    most_recent_log_entry: LogEntry = None

    # Action slots
    expended_action_slots: Tuple[str, ...] = ()

    # Convenience fields
    players_by_id: frozendict = field(init=False, repr=False)
    players_by_turn: frozendict = field(init=False, repr=False)
    active_player: Player = field(init=False, repr=False)
    active_player_id: str = field(init=False, repr=False)

    @staticmethod
    def create(
            player_metadata: Iterator[PlayerMetadata],
            randomize_turn_order: bool = True,
            setup: Setup = None):

        shuffled_player_metadata = tuple(
                shuffled(player_metadata) if randomize_turn_order else player_metadata)
        players = frozenset(Player.create(x, pos) for x, pos in enumerate(shuffled_player_metadata)
        num_players = len(player_metadata)

        setup = setup if setup is not None else Setup.create_random_setup(num_players)
        pool = TileSet(
                bonus_tiles = setup.bonus_tiles,
                favor_tiles = FAVOR_TILES,
                town_tiles = TOWN_TILES)

        return GameState(
                players = frozenset(players),
                num_players = num_players,
                setup = setup,
                pool = pool)

    def get_available_actions(self) -> Tuple[Action, ...]:
        if self.phase != Phase.TURN:
            return tuple([self.get_applicable_off_turn_action()])
        else:
            power_actions = self.get_available_power_actions()
            special_actions = self.get_available_special_actions()
            return STANDARD_ACTIONS + power_actions + special_actions

    def get_available_power_actions(self) -> Tuple[Action, ...]:
        return (x for x in POWER_ACTIONS if x.action_id not in self.expended_action_slots)

    def get_available_special_actions(self) -> Tuple[Action, ...]:
        special_actions = self.active_player.faction.get_special_actions(
                self.active_player.player_state)
        return (x for x in special_actions if x.action_id not in self.expended_action_slots)

    def get_applicable_off_turn_action(self) -> Action:
        return get_off_turn_action_by_phase(self.phase)

    def submit(self,
            action_execution: ActionExecution,
            leech_decisions: Iterator[bool] = (),
            conversions_before_action: Iterable[Conversion] = frozenset(),
            conversions_after_action: Iterable[Conversion] = frozenset()) -> "GameState":

        if not self.phase == Phase.TURN and \
                (leech_decisions or pre_action_conversions or post_action_conversions):
            raise ValueError("A player may only convert resources or accept leech on their turn")

        return self._reflect_leech_decisions(leech_decisions) \
                ._reflect_conversions(conversions_before_action) \
                ._reflect_step(action_execution.compute(self)) \
                ._reflect_conversions(conversions_after_action) \
                ._reflect_phase_transition()

    def _reflect_leech_decisions(self, leech_decisions: Iterable[bool]) -> "GameState":

        if not len(leech_decisions) == len(player_state.leech_opportunities):
            raise ValueError("Wrong number of leech decisions provided. Expected {}, found {}."
                    .format(len(leech_decisions), len(player_state.leech_decisions)))

        player_state = self.active_player.player_state

        leech_decisions_accepted = [
                amount
                for amount, taken in zip(player_state.leech_opportunities, leech_decisions)
                if taken]

        total_capacity = player_state.resources.power.get_available_capacity()
        total_leech_delta = ResourceDelta()
        for amount in leech_decisions_accepted:
            capacity = total_capacity - leech_decisions_accepted.power
            actual_amount = min(capacity, amount)
            leech_delta = ResourceDelta(
                    power = actual_amount,
                    victory_points = -(actual_amount - 1))
            total_leech_delta = total_leech_delta + leech_delta

        if player_state.resources.victory_points > abs(total_leech_delta.victory_points):
            raise ValueError("Not enough victory points to leech")

        new_resource_state = player_state.resources.add(total_leech_delta)
        new_player_state = player_state.replace(
                resources = new_resource_state,
                leech_opportunities = ())

        return self.update_player_state(new_player_state, self.active_player_id)

    def _reflect_conversions(self, conversions: Iterable[Conversion]) -> ResourceDelta:
        resource_delta = sum(x.get_resource_delta(self.active_player.faction) for x in conversions)
        new_resource_state = self.active_player.player_state.resources.add(resource_delta)
        return self._update_resource_state(new_resource_state, self.active_player_id)

    def _reflect_phase_transition(self) -> "GameState":
        # TODO
        pass

    def _reflect_step(self, step: Step) -> "GameState":
        # TODO
        pass

    def _update_resource_state(self, new_resource_state: ResourceState, player_id: str) \
            -> "GameState":
        """Convenience version of the replace() method provided by python dataclasses providing
        nested replacement.
        """
        player = self.players_by_id[player_id]
        new_player_state = player.player_state.replace(resources = new_resource_state)
        return self._update_player_state(new_player_state, player_id)

    def _update_player_state(self, new_player_state: PlayerState, player_id: str) -> "GameState":
        player = self.players_by_id[player_id]
        new_player = player.replace(player_state = new_player_state)
        return self._update_player(player)

    def _update_player(self, new_player: Player) -> "GameState":
        other_players = Set(x for x in self.players if x.player_id != player.player_id)
        players = frozenset(other_playsers.add(player))
        return self.replace(players = players)

    def __post_init__(self):
        self.players_by_id = frozendict({x.player_id: x for x in self.players})
        self.players_by_turn = frozendict({x.initial_turn_position: x for x in self.players})
        self.active_player = self.players_by_turn[self.active_player_position]
        self.active_player_id = self.active_player.player_id

#    def _get_next_player(self):
#        return active_player + 1 if active_player < self.num_players else 1


