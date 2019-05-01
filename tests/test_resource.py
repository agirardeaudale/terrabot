#!/usr/bin/env python

import pytest

from ..terrabot.sim.resource import PowerBowlState

def test_PowerBowlState_accessors():
    power_bowl_state = PowerBowlState(3, 5, 4)

    assert power_bowl_state.get_num_tokens() == 12
    assert power_bowl_state.get_available_power() == 8
    assert power_bowl_state.get_available_capacity() == 25 # 2*(12-3) + (12-5)

def test_PowerBowlState_gain_MoreThanCapacity():
    initial_state = PowerBowlState(3, 5, 4)

    resulting_state = initial_state.gain(700)
    assert resulting_state == PowerBowlState(0, 0, 12)

def test_PowerBowlState_gain_WithoutOverflow():
    initial_state = PowerBowlState(3, 5, 4)

    resulting_state = initial_state.gain(2)
    assert resulting_state == PowerBowlState(1, 7, 4)

def test_PowerBowlState_gain_WithOverflow():
    initial_state = PowerBowlState(3, 5, 4)

    resulting_state = initial_state.gain(7)
    assert resulting_state == PowerBowlState(0, 4, 8)

def test_PowerBowlState_spend_WithoutBurn():
    initial_state = PowerBowlState(3, 5, 4)

    resulting_state = initial_state.spend(3)
    assert resulting_state == PowerBowlState(6, 5, 1)

def test_PowerBowlState_spend_WithBurn():
    initial_state = PowerBowlState(3, 5, 4)

    resulting_state = initial_state.spend(6)
    assert resulting_state == PowerBowlState(7, 1, 0)

def test_PowerBowlState_spend_MoreThanCapacity():
    initial_state = PowerBowlState(3, 5, 4)

    with pytest.raises(ValueError):
        initial_state.spend(7)
