from dataclasses import dataclass

from frozendict import frozendict

from terrabot.sim.action import *


TRANSFORM_AND_BUILD_ACTION = TransformAndBuildAction("Action-Transform/Build")
ADVANCE_DIG_ACTION = AdvanceDigAction("Action-AdvanceDig")
ADVANCE_SHIP_ACTION = AdvanceShipAction("Action-AdvanceShip")
UPGRADE_STRUCTURE_ACTION = UpgradeStructureAction("Action-UpgradeStructure")
SEND_PRIEST_ACTION = SendPriestAction("Action-SendPriest")
PASS_ACTION = PassAction("Action-Pass")

STANDARD_ACTIONS = (
        TRANSFORM_AND_BUILD_ACTION,
        ADVANCE_DIG_ACTION,
        ADVANCE_SHIP_ACTION,
        UPGRADE_STRUCTURE_ACTION,
        SEND_PRIEST_ACTION,
        PASS_ACTION)

POWER_ACTION_1 = BridgePowerAction(
        action_id = "Action-PWR-Bridge-(ACT1)",
        power_cost = 3)
POWER_ACTION_2 = ResourcePowerAction(
        action_id = "Action-PWR-Priest-(ACT2)",
        power_cost = 3,
        resources_provided = ResourceDelta(priests=1))
POWER_ACTION_3 = ResourcePowerAction(
        action_id = "Action-PWR-2Worker-(ACT3)",
        power_cost = 4,
        resources_provided = ResourceDelta(workers=2))
POWER_ACTION_4 = ResourcePowerAction(
        action_id = "Action-PWR-7Coin-(ACT4)",
        power_cost = 4,
        resources_provided = ResourceDelta(coins=7))
POWER_ACTION_5 = SpadePowerAction(
        action_id = "Action-PWR-1Spade-(ACT5)",
        power_cost = 4,
        spades_provided = 1)
POWER_ACTION_6 = SpadePowerAction(
        action_id = "Action-PWR-2Spade-(ACT6)",
        power_cost = 6,
        spades_provided = 2)

POWER_ACTIONS = (
        POWER_ACTION_1,
        POWER_ACTION_2,
        POWER_ACTION_3,
        POWER_ACTION_4,
        POWER_ACTION_5,
        POWER_ACTION_6)
POWER_ACTION_IDS = (x.action_id for x in POWER_ACTIONS)

BONUS_TILE_SPADE_ACTION = TileSlotAction(action_id = "Action-BonusTile-Spade-(BON1)")
BONUS_TILE_CULT_ACTION = TileSlotAction(action_id = "Action-BonusTile-Cult-(BON2)")
FAVOR_TILE_CULT_ACTION = TileSlotAction(action_id = "Action-FavorTile-Cult-(FAV6)")

TILE_SLOT_ACTIONS = (
        BONUS_TILE_SPADE_ACTION,
        BONUS_TILE_CULT_ACTION,
        FAVOR_TILE_CULT_ACTION)

FACTION_SPECIAL_ACTIONS = ( )

SPECIAL_ACTIONS = TILE_SLOT_ACTIONS + FACTION_SPECIAL_ACTIONS

OFF_TURN_ACTIONS = ( )

ALL_ACTIONS = STANDARD_ACTIONS + POWER_ACTIONS + SPECIAL_ACTIONS + OFF_TURN_ACTIONS


_ACTION_LOOKUP_BY_ID = frozendict({x.action_id: x for x in ALL_ACTIONS})
def get_action_by_id(action_id: str) -> Action:
    return _ACTION_LOOKUP_BY_ID[action_id]

_OFF_TURN_ACTION_LOOKUP_BY_PHASE = frozendict({x.phase: x for x in OFF_TURN_ACTIONS})
def get_off_turn_action_by_phase(phase: Phase) -> Action:
    return _OFF_TURN_ACTION_LOOKUP_BY_PHASE[phase]



# Actions/Options:
#   Transform:
#       Location
#       New Terrain
#       Dwelling y/n
#   Advance Dig
#   Advance Ship
#   Build:
#       StructureType
#       Location
#       Town Tile Selection
#       Favor Tile(s) Selection
#   Send
#       Cult Track
#       Max or 1step
#   Power Action
#       ACT1:
#           Location
#       ACT2
#       ACT3
#       ACT4
#       ACT5:
#           Location
#           Build y/n
#       ACT6:
#           Location 1
#           Location 2
#           Build L1/L2/no
#   Special Action
#       Faction Action
#           Engineers
#           Dwarves
#           Fakir
#           ???
#       Stronghold ActionSlot
#           Witches
#           Auren
#           Swarmlings
#           Chaos Magicians
#           Nomads
#           Giants
#       Tile Actions
#           FAV6 (2Water)
#           BON? spd, cult
#
#   Pass
#       Bonus Tile
#
