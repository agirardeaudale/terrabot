from terrabot.sim.map import Terrain
from terrabot.sim.player import Faction
from terrabot.sim.resources import ResourceType, _DEFAULT_CONVERSION_RATES

FACTIONS = tuple(
        Faction(
                name = "Alchemists",
                home_terrain = Terrain.SWAMP,
                resource_conversion_rates = frozendict_with_item(
                        _DEFAULT_CONVERSION_RATES, (ResourceType.POINTS, ResourceType.COINS), 1)
                )
        )
