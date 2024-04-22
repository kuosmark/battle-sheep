import unittest
from constants import INITIAL_SHEEP, MAX_SHEEP_TO_MOVE, MIN_SHEEP_TO_MOVE
from game import Game
from pasture import Pasture


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def get_free_edge_pasture(self):
        return self.game.get_potential_initial_pastures()[0]

    def add_sheep_to_target_one_by_one(self, amount):
        self.game.add_sheep_to_target(amount)

    def subtract_sheep_from_target_one_by_one(self, amount):
        self.game.subtract_sheep_from_target(amount)

    def play_initial_turn_and_get_initial_pasture(self) -> Pasture:
        initial_pasture = self.get_free_edge_pasture()
        self.game.place_initial_sheep(initial_pasture)
        self.game.next_turn()
        return initial_pasture

    def play_initial_phase_and_choose_initial_pasture(self) -> Pasture:
        initial_pasture = self.play_initial_turn_and_get_initial_pasture()
        self.game.next_turn()
        self.game.click_on_pasture(initial_pasture)
        return initial_pasture

    def play_initial_phase_and_choose_pasture_and_target(self) -> Pasture:
        chosen_pasture = self.play_initial_phase_and_choose_initial_pasture()
        target = chosen_pasture.get_potential_targets(self.game.pastures)[
            0]
        self.game.click_on_pasture(target)
        return target

    def test_initial_sheep_can_be_placed_on_free_edge_pasture(self):
        choice = self.get_free_edge_pasture()
        self.game.place_initial_sheep(choice)
        self.assertTrue(choice.is_occupied())
        self.assertEqual(choice.get_amount_of_sheep(), INITIAL_SHEEP)

    def test_initial_sheep_can_not_be_placed_in_the_middle(self):
        choice = next(
            pasture for pasture in self.game.pastures if not pasture.is_on_edge(self.game.pastures))
        with self.assertRaises(ValueError):
            self.game.place_initial_sheep(choice)
        self.assertEqual(choice.get_amount_of_sheep(), 0)

    def test_initial_sheep_can_not_be_placed_on_occupied_pasture(self):
        choice = self.get_free_edge_pasture()
        self.game.place_initial_sheep(choice)
        with self.assertRaises(ValueError):
            self.game.place_initial_sheep(choice)

    def test_occupation_of_pasture_is_calculated_correctly(self):
        initial_pasture = self.play_initial_turn_and_get_initial_pasture()
        self.assertFalse(
            self.game.is_controlled_by_player_in_turn(initial_pasture))

        self.game.next_turn()
        self.assertTrue(
            self.game.is_controlled_by_player_in_turn(initial_pasture))

    def test_can_choose_pasture_with_own_sheep(self):
        chosen_pasture = self.play_initial_phase_and_choose_initial_pasture()
        self.assertEqual(self.game.chosen_pasture, chosen_pasture)

    def test_can_choose_target_pasture(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()
        self.assertEqual(self.game.target_pasture, target)

    def test_changing_turn_resets_chosen_pasture(self):
        self.play_initial_phase_and_choose_initial_pasture()
        self.game.next_turn()
        self.assertIsNone(self.game.chosen_pasture)

    def test_changing_turn_resets_target_pasture(self):
        self.play_initial_phase_and_choose_pasture_and_target()
        self.game.next_turn()

        self.assertIsNone(self.game.target_pasture)

    def test_changing_turn_resets_targeted_pastures(self):
        self.play_initial_phase_and_choose_initial_pasture()
        self.game.next_turn()

        targeted_pastures = self.game.get_targeted_pastures()
        self.assertEqual(len(targeted_pastures), 0)

    def test_single_sheep_is_added_to_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()

        self.add_sheep_to_target_one_by_one(1)
        self.assertEqual(target.planned_sheep, MIN_SHEEP_TO_MOVE + 1)

    def test_ten_sheep_is_added_to_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()

        self.add_sheep_to_target_one_by_one(10)
        self.assertEqual(target.planned_sheep, MIN_SHEEP_TO_MOVE + 10)

    def test_all_but_one_sheep_can_be_added_to_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()

        self.add_sheep_to_target_one_by_one(100)
        self.assertEqual(target.planned_sheep, INITIAL_SHEEP - 1)

    def test_adding_sheep_can_be_reversed(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()

        self.add_sheep_to_target_one_by_one(10)
        self.subtract_sheep_from_target_one_by_one(10)
        self.assertEqual(target.planned_sheep, MIN_SHEEP_TO_MOVE)

    def test_at_least_one_sheep_must_be_on_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()

        self.subtract_sheep_from_target_one_by_one(10)
        self.assertEqual(target.planned_sheep, MIN_SHEEP_TO_MOVE)

    def test_minimum_amount_of_sheep_is_moved_to_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()
        self.game.confirm_move()
        self.assertEqual(target.get_amount_of_sheep(), MIN_SHEEP_TO_MOVE)

    def test_max_amount_of_sheep_is_moved_to_target(self):
        target = self.play_initial_phase_and_choose_pasture_and_target()
        self.add_sheep_to_target_one_by_one(
            MAX_SHEEP_TO_MOVE - MIN_SHEEP_TO_MOVE)
        self.game.confirm_move()
        self.assertEqual(target.get_amount_of_sheep(), MAX_SHEEP_TO_MOVE)
