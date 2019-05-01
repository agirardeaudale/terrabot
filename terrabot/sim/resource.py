from dataclasses import dataclass
from enum import Enum, auto
from fractions import Fraction
from typing import Tuple

@dataclass
class ResourceDelta:
    coins: int = 0
    workers: int = 0
    priests: int = 0
    power: int = 0
    victory_points: int = 0

    # TODO: arithmetic operators, especially __neg__


@dataclass
class ResourceType:
    COINS = auto()
    WORKERS = auto()
    PRIESTS = auto()
    POWER = auto()
    POINTS = auto()


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
    #   VP <--> C
    from_: ResourceType
    to: ResourceType
    quantity: int
    rate: Fraction


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

    def gain(self, resources: ResourceDelta) -> PowerBowlState:
        coins = self.coins + resources.coins
        workers = self.workers + resources.workers
        priests = self.priests + resources.priests
        power = self.power.gain(resources.power)
        return replace(self,
                coins = coins,
                workers = workers,
                priests = priests,
                power = power)

    def spend(self, resources: ResourceDelta) -> PowerBowlState:
        coins = self.coins - resources.coins
        workers = self.workers - resources.workers
        priests = self.priests - resources.priests
        power = self.power.spend(resources.power)
        return replace(self,
                coins = coins,
                workers = workers,
                priests = priests,
                power = power)

    def could_afford(self, cost: ResourceDelta) -> Tuple[bool, Tuple[Conversion, ...]]:
        # TODO
        # Actually this method might be a bad idea, since there are often there are many possible
        # ways one could convert resources to meet a cost (i.e., PW->C, P->C, W->C, VP->C)
        return (True, None)


