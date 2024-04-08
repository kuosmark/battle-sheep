import unittest
from game import Game

INITIAL_SHEEP = 16


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def get_free_edge_pasture(self):
        return next(
            pasture for pasture in self.game.pastures if pasture.is_free() and pasture.is_on_edge(self.game.pastures))

    def test_initial_sheep_can_be_placed_on_free_edge_pasture(self):
        choice = self.get_free_edge_pasture()
        self.game.place_initial_sheep(choice)
        self.assertEqual(choice.is_taken(), True)
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
