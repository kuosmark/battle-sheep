import unittest
from constants import (
    PLAYER
)
from pasture import Pasture


class TestPasture(unittest.TestCase):
    def setUp(self) -> None:
        self.pasture = Pasture((100, 100))

    def test_free_pasture_is_not_occupied_by_anyone(self):
        self.assertTrue(self.pasture.is_free())
        self.assertFalse(self.pasture.is_occupied())
        self.assertFalse(self.pasture.is_occupied_by_player())
        self.assertFalse(self.pasture.is_occupied_by_computer())

    def test_player_can_occupy_pasture(self):
        self.pasture.occupy(PLAYER, 10)
        self.assertEqual(self.pasture.get_amount_of_sheep(), 10)

        self.assertFalse(self.pasture.is_free())
        self.assertTrue(self.pasture.is_occupied())
        self.assertTrue(self.pasture.is_occupied_by_player())
        self.assertFalse(self.pasture.is_occupied_by_computer())

    def test_planned_sheep_are_added_and_subtracted_correctly(self):
        self.pasture.add_a_planned_sheep()
        self.assertEqual(self.pasture.get_amount_of_planned_sheep(), 1)
        self.pasture.subtract_a_planned_sheep()
        self.assertEqual(self.pasture.get_amount_of_planned_sheep(), 0)

    def test_resetting_pasture_functions_correctly(self):
        self.pasture.occupy(PLAYER, 10)
        self.pasture.add_a_planned_sheep()
        self.pasture.reset()

        self.assertTrue(self.pasture.is_free())
        self.assertEqual(self.pasture.get_amount_of_sheep(), 0)
        self.assertEqual(self.pasture.get_amount_of_planned_sheep(), 0)

    def test_value_of_pasture_without_neighbours_is_zero(self):
        self.assertEqual(self.pasture.get_value([self.pasture]), 0)
