# test_cycle_process.py
"""
Cycle-process-test: Tester en simpel cyklisk proces (f.eks. simulering af tidsskiftende tilstand)
"""

import pytest
from dataclasses import dataclass
from typing import List

# Eksempel på en cyklisk proces-klasse (den du tester)
@dataclass
class CycleSimulator:
    """Simulerer en proces der kører i cyklusser (f.eks. dag/nat, temperatur-ændring, spil-tick)"""
    initial_value: float = 0.0
    cycle_count: int = 0
    max_cycles: int = 1000

    def reset(self):
        self.initial_value = 0.0
        self.cycle_count = 0

    def run_one_cycle(self, delta: float) -> float:
        """Kører én cyklus og opdaterer værdien"""
        self.initial_value += delta
        self.cycle_count += 1
        return self.initial_value

    def run_cycles(self, delta: float, num_cycles: int) -> List[float]:
        """Kører flere cyklusser og returnerer historik"""
        history = []
        for _ in range(num_cycles):
            history.append(self.run_one_cycle(delta))
        return history


# ──────────────────────────────────────────────
# FIXTURES
# ──────────────────────────────────────────────

@pytest.fixture
def simulator():
    sim = CycleSimulator()
    yield sim
    # cleanup / reset efter hver test (god vane)
    sim.reset()


# ──────────────────────────────────────────────
# TESTS – Cycle Process
# ──────────────────────────────────────────────

def test_single_cycle_increases_value(simulator):
    result = simulator.run_one_cycle(5.0)
    assert result == 5.0
    assert simulator.cycle_count == 1


def test_multiple_cycles_accumulate_correctly(simulator):
    history = simulator.run_cycles(2.5, 4)
    assert history == [2.5, 5.0, 7.5, 10.0]
    assert simulator.cycle_count == 4


def test_cycle_count_increases_properly(simulator):
    simulator.run_cycles(1.0, 10)
    assert simulator.cycle_count == 10


@pytest.mark.parametrize("cycles, expected_final", [
    (0,   0.0),
    (1,   3.0),
    (5,  15.0),
    (100, 300.0),
])
def test_parametrized_cycle_count(simulator, cycles, expected_final):
    simulator.run_cycles(3.0, cycles)
    assert simulator.initial_value == pytest.approx(expected_final)


def test_max_cycles_not_exceeded(simulator):
    """Simulerer at processen stopper ved max_cycles"""
    simulator.max_cycles = 5
    simulator.run_cycles(1.0, 10)  # forsøger 10, men stopper ved 5
    assert simulator.cycle_count == 5
    assert simulator.initial_value == 5.0


def test_reset_clears_state(simulator):
    simulator.run_cycles(10.0, 3)
    assert simulator.initial_value == 30.0
    assert simulator.cycle_count == 3

    simulator.reset()
    assert simulator.initial_value == 0.0
    assert simulator.cycle_count == 0


def test_negative_delta_works(simulator):
    """Cyklusser med negativ ændring (f.eks. cooldown)"""
    history = simulator.run_cycles(-1.5, 6)
    assert history == [-1.5, -3.0, -4.5, -6.0, -7.5, -9.0]


def test_floating_point_precision_over_many_cycles(simulator):
    """Tjek for akkumuleringsfejl over mange iterationer"""
    simulator.run_cycles(0.1, 1000)
    assert simulator.initial_value == pytest.approx(100.0, abs=1e-10)