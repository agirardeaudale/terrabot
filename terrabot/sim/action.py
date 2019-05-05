"""Not a huge fan of "event" and "EventTrigger" as module/class names. maybe rename."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

from frozendict import frozendict

from terrabot.sim.cult import CultDelta
from terrabot.sim.map import Terrain
from terrabot.sim.player import Faction
from terrabot.sim.resource import ResourceDelta, Conversion, LeechOpportunity
from terrabot.sim.structure import Structure
from terrabot.sim.tile import Tile

class Phase(Enum):
    SELECT_FACTION = auto()
    PLACE_INITIAL_DWELLING = auto()
    SELECT_INITIAL_BONUS_TILE = auto()
    TURN = auto()
    SELECT_TOWN_TILE = auto()
    SELECT_FAVOR_TILE = auto()
    LEECH_DECISION = auto()
    BONUS_SPADE_DECISION = auto()
    CULTIST_DECISION = auto()
    OVER = auto()

    # If a player can only has keys to enter step 10 of one cult track but gained enough cult steps
    # to move into multiple (e.g. due to a town tile)
    CULT_TRACK_DECISION = auto()


@dataclass
class Step:
    """A Step represents one set of changes that receives a LogEntry and an iteration of the
    gamestate.
    """
    description: str
    passed: bool = False
    resource_delta: ResourceDelta = ResourceDelta()
    new_structures: Tuple[Structure, ...] = ()
    new_tiles: Tuple[Tile, ...] = ()
    returned_tile: Tile = None
    cult_delta: CultDelta = CultDelta()

    new_leech_opportunities: frozendict = frozendict() # map by player_id
    new_cultist_steps: frozendict = frozendict() # map by player_id
    new_town_tile_decisions: int = 0
    new_favor_tile_decisions: int = 0

    action_slot_expended: str = None # by action_id

    # Chaos Magicians' Stronghold Action
    extra_turns: int = 0

    # Off Turn Actions
    faction_selected: Faction = None


@dataclass
class ActionExecution(ABC):
    """One full execution of an action, with all options specified, resulting in a single Step.

    Consider no longer having separate Action/ActionExecution classes.
    """
    cost: ResourceDelta

    #@abstractmethod
    def compute(self, game_state: 'GameState') -> Step:
        raise NotImplementedError


@dataclass
class Action(ABC):
    """One action that may or may not be available to a player, which would result in a single step.
    The action may have multiple options or versions. For example, the "BON1 (spd)" Action allows
    digging on any adjacent Hex. "BON1 (spd) H8, build D" would be an ActionExecution based on that
    Action.
    """
    action_id: str

    #@abstractmethod
    def get_available_executions(self, game_state: 'GameState') -> Tuple["Action", ...]:
        raise NotImplementedError


#------------------------------------
# Always available actions
@dataclass
class TransformAndBuildActionExecution(ActionExecution):
    location: str # by location_id
    new_terrain: Terrain = None
    build_dwelling: bool = False

@dataclass
class TransformAndBuildAction(Action):
    pass

@dataclass
class AdvanceDigAction(Action):
    pass

@dataclass
class AdvanceShipAction(Action):
    pass

@dataclass
class UpgradeStructureAction(Action):
    pass

@dataclass
class SendPriestAction(Action):
    pass

@dataclass
class PassAction(Action):
    pass

#------------------------------------
# Power Actions
@dataclass
class PowerAction(Action):
    power_cost: int

@dataclass
class SpadePowerAction(PowerAction):
    spades_provided: int

@dataclass
class BridgePowerAction(PowerAction):
    pass

@dataclass
class ResourcePowerAction(PowerAction):
    resources_provided: ResourceDelta

#------------------------------------
# Special Actions
@dataclass
class FactionSpecialAction(Action):
    pass

@dataclass
class TileSlotAction(Action):
    pass

#------------------------------------
# Off-Turn Actions
@dataclass
class OffTurnAction(Action):
    phase: Phase

@dataclass
class SelectFactionAction(OffTurnAction):
    action_id = "Action-SelectFaction"
    phase = Phase.SELECT_FACTION

@dataclass
class PlaceInitialDwellingAction(OffTurnAction):
    action_id = "Action-PlaceInitialDwelling"
    phase = Phase.PLACE_INITIAL_DWELLING

@dataclass
class SelectInitialBonusTileAction(OffTurnAction):
    action_id = "Action-SelectInitialBonusTile"
    phase = Phase.SELECT_INITIAL_BONUS_TILE

@dataclass
class SelectTownTileAction(OffTurnAction):
    action_id = "Action-SelectTownTile"
    phase = Phase.SELECT_TOWN_TILE

@dataclass
class SelectFavorTileAction(OffTurnAction):
    action_id = "Action-SelectFavorTile"
    phase = Phase.SELECT_FAVOR_TILE

@dataclass
class MakeLeechDecisionAction(OffTurnAction):
    action_id = "Action-MakeLeechDecision"
    phase = Phase.LEECH_DECISION

@dataclass
class MakeBonusSpadeDecisionAction(OffTurnAction):
    action_id = "Action-MakeBonusSpadeDecision"
    phase = Phase.BONUS_SPADE_DECISION

@dataclass
class MakeCultistDecisionAction(OffTurnAction):
    action_id = "Action-MakeCultistDecision"
    phase = Phase.CULTIST_DECISION
