from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

class ResourceType(Enum):
    COINS = auto()
    WORKERS = auto()
    PRIESTS = auto()
    POWER = auto()
    POINTS = auto()


@dataclass
class ResourceDelta:
    coins: int = 0
    workers: int = 0
    priests: int = 0
    power: int = 0
    victory_points: int = 0

    def add_by_type(self, amount: int, resource_type: ResourceType):
        if resource_type == ResourceType.COINS:
            return ResourceDelta(coins = self.coins + amount)
        elif resource_type == ResourceType.WORKERS:
            return ResourceDelta(workers = self.workers + amount)
        elif resource_type == ResourceType.PRIESTS:
            return ResourceDelta(priests = self.priests + amount)
        elif resource_type == ResourceType.POWER:
            return ResourceDelta(power = self.power + amount)
        elif resource_type == ResourceType.POINTS:
            return ResourceDelta(victory_points = self.victory_points + amount)
        else:
            raise AssertionError(f"Unrecognized ResourceType {resource_type}.")

    def __repr__(self):
        changes = []
        if self.coins:
            changes.append(f"{self.coins}C")
        if self.workers:
            changes.append(f"{self.workers}W")
        if self.priests:
            changes.append(f"{self.priests}P")
        if self.power:
            changes.append(f"{self.power}PW")
        if self.victory_points:
            changes.append(f"{self.victory_points}VP")
        return return f"({changes.join(", ")})"

    def __add__(self, other: "ResourceDelta") -> "ResourceDelta":
        coins = self.coins + other.coins
        workers = self.workers + other.workers
        priests = self.priests + other.priests
        power = self.power + other.power
        victory_points = self.victory_points + other.victory_points
        return ResourceDelta(coins, workers, priests, power, victory_points)

    def __sub__(self, other: "ResourceDelta") -> "ResourceDelta":
        coins = self.coins - other.coins
        workers = self.workers - other.workers
        priests = self.priests - other.priests
        power = self.power - other.power
        victory_points = self.victory_points - other.victory_points
        return ResourceDelta(coins, workers, priests, power, victory_points)

    def __neg__(self) -> "ResourceDelta":
        coins = -self.coins
        workers = -self.workers
        priests = -self.priests
        power = -self.power
        victory_points = -self.victory_points
        return ResourceDelta(coins, workers, priests, power, victory_points)


_DEFAULT_CONVERSION_RATES = frozendict({
    (ResourceType.POWER, ResourceType.PRIESTS): 5,
    (ResourceType.POWER, ResourceType.WORKERS): 3,
    (ResourceType.POWER, ResourceType.COINS): 1,
    (ResourceType.PRIESTS, ResourceType.WORKERS): 1,
    (ResourceType.PRIESTS, ResourceType.COINS): 1,
    (ResourceType.WORKERS, ResourceType.COINS): 1,


@dataclass
class Conversion:
    #   PW ->
    #       P
    #       W
    #       C
    #   P ->
    #       W
    #       C
    #   W ->
    #       C
    # Alchemists:
    #   VP ->
    #       C
    from_: ResourceType
    to: ResourceType
    quantity_produced: int

    def get_resource_delta(self, faction: "Faction"):
        rate = Conversion.get_rate(self.from_, self.to, faction)
        quantity_spent = quantity_produced * rate
        return ResourceDelta() \
                .add_by_type(-from_ * quantity_spent) \
                .add_by_type(to * quantity_produced)

    @staticmethod
    def get_rate(from_: ResourceType, to: ResourceType, faction: "Faction" = None) -> int:
        if faction:
            rate_map = faction.resource_conversion_rates
        else:
            rate_map = _DEFAULT_CONVERSION_RATES

        try:
            return rate_map[(from_, to)]
        except KeyError:
            raise ValueError(f"No available conversion from {from_} to {to}")


@dataclass
class PowerBowlState:
    bowl_one: int = 12
    bowl_two: int = 0
    bowl_three: int = 0

    def gain(self, power: int) -> "PowerBowlState":
        if power <= self.available_capacity():
            bowl_one = 0
            bowl_two = 0
            bowl_three = self.bowl_one + self.bowl_two + self.bowl_three
        elif power <= self.bowl_one:
            bowl_one = self.bowl_one - power
            bowl_two =  self.bowl_two + power
            bowl_three = self.bowl_three
        else:
            excess = power - self.bowl_one
            bowl_one = 0
            bowl_two = self.bowl_one + self.bowl_two - excess
            bowl_three = self.bowl_three + excess

        return replace(self,
                bowl_one = bowl_one,
                bowl_two = bowl_two,
                bowl_three = bowl_three)

    def spend(self, power: int) -> "PowerBowlState":
        if power < self.available_power():
            raise ValueError(
                    f"Tried to spend {power} power, only {self.available_power()} available.")
        elif power < self.bowl_three:
            bowl_one = self.bowl_one + power
            bowl_two = self.bowl_two
            bowl_three = self.bowl_three - power
        else:
            burn = power - self.bowl_three
            bowl_one = self.bowl_one + power
            bowl_two = self.bowl_two - (2 * burn)
            bowl_three = 0

        return replace(self,
                bowl_one = bowl_one,
                bowl_two = bowl_two,
                bowl_three = bowl_three)

    def get_num_tokens(self):
        return self.bowl_one + self.bowl_two + self.bowl_three

    def get_available_power(self):
        """how much power could be spent (with max burn)"""
        return self.bowl_three + (self.bowl_two // 2)

    def get_available_capacity(self):
        """how much more power could be gained"""
        num_tokesn = self.get_num_tokens()
        return 2 * (num_tokens - self.bowl_one) + (num_tokens - self.bowl_two)


@dataclass
class PlayerResourceState:
    coins: int = 0
    workers: int = 0
    priests: int = 0
    priest_pool_size: int = 7
    power: PowerBowlState = PowerBowlState()

    def add(self, resources: ResourceDelta) -> "PlayerResourceState":
        coins = self.coins + resources.coins
        workers = self.workers + resources.workers
        priests = self.priests + resources.priests
        power = self.power.gain(resources.power)
        return replace(self,
                coins = coins,
                workers = workers,
                priests = priests,
                power = power)

    def subtract(self, resources: ResourceDelta) -> "PlayerResourceState":
        coins = self.coins - resources.coins
        workers = self.workers - resources.workers
        priests = self.priests - resources.priests
        power = self.power.spend(resources.power)
        return replace(self,
                coins = coins,
                workers = workers,
                priests = priests,
                power = power)

    def are_quantities_nonnegative(self) -> bool:
        # TODO
        pass

    def could_afford(self, cost: ResourceDelta) -> Tuple[bool, Tuple[Conversion, ...]]:
        # TODO
        # Actually this method might be a bad idea, since often there are many possible
        # ways one could convert resources to meet a cost (i.e., PW->C, P->C, W->C, VP->C)
        return (True, None)


@dataclass
class LeechOpportunity:
    amount: int
    from_player_id: str

    def get_resource_delta(self, available_capacity: int):




