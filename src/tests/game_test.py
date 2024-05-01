from typing import Tuple
import unittest
from constants import (COMPUTER,
                       INITIAL_SHEEP,
                       PLAYER)
from game import Game
from pasture import Pasture


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    # Apumetodit

    def get_free_edge_pasture(self):
        return self.game.get_potential_initial_pastures()[0]

    def play_initial_turn(self) -> Pasture:
        initial_pasture = self.get_free_edge_pasture()
        self.game.make_initial_turn(initial_pasture)
        return initial_pasture

    def choose_target_pasture(self) -> Tuple[Pasture, Pasture]:
        chosen_pasture = self.play_initial_turn()
        # Tekoälyn vuoro
        self.play_initial_turn()

        self.game.click(chosen_pasture.centre)
        target = chosen_pasture.get_any_potential_target(self.game.pastures)
        if not target:
            raise SystemError('No potential targets found')
        self.game.click(target.centre)
        return chosen_pasture, target

    def add_sheep_to_target(self, amount: int):
        for _ in range(amount):
            self.game.scroll_up()

    def subtract_sheep_from_target(self, amount: int):
        for _ in range(amount):
            self.game.scroll_down()

    def occupy_neighbours(self, pasture: Pasture, occupier: int, sheep: int):
        neighbours = pasture.get_free_neighbours(self.game.pastures)

        for neighbour in neighbours:
            neighbour.occupy(occupier, sheep)

    def win_game_by_player(self):
        players_initial_pasture = self.play_initial_turn()
        computers_initial_pasture = self.play_initial_turn()
        players_initial_pasture.sheep = 1

        self.occupy_neighbours(computers_initial_pasture, PLAYER, 1)

    def win_game_by_computer(self):
        players_initial_pasture = self.play_initial_turn()
        computers_initial_pasture = self.play_initial_turn()
        computers_initial_pasture.sheep = 1

        self.occupy_neighbours(players_initial_pasture, COMPUTER, 1)

    # Testit

    def test_initial_sheep_can_be_placed_on_free_edge_pasture(self):
        choice = self.get_free_edge_pasture()
        self.game.make_initial_turn(choice)
        self.assertTrue(choice.is_occupied())
        self.assertEqual(choice.get_amount_of_sheep(), INITIAL_SHEEP)

    def test_initial_sheep_can_not_be_placed_in_the_middle(self):
        choice = next(
            pasture for pasture in self.game.pastures if not pasture.is_on_edge(self.game.pastures))
        with self.assertRaises(ValueError):
            self.game.make_initial_turn(choice)
        self.assertEqual(choice.get_amount_of_sheep(), 0)

    def test_initial_sheep_can_not_be_placed_on_occupied_pasture(self):
        choice = self.get_free_edge_pasture()
        self.game.make_initial_turn(choice)
        with self.assertRaises(ValueError):
            self.game.make_initial_turn(choice)

    def test_omputer_can_make_separate_initial_turn(self):
        players_initial_pasture = self.play_initial_turn()
        computers_initial_pasture = self.play_initial_turn()
        self.assertIsNot(players_initial_pasture, computers_initial_pasture)
        self.assertEqual(players_initial_pasture.get_amount_of_sheep(
        ), computers_initial_pasture.get_amount_of_sheep())

    def test_pasture_occupation_and_player_in_turn_are_calculated_correctly(self):
        players_initial_pasture = self.play_initial_turn()
        self.assertTrue(players_initial_pasture.is_occupied_by_player())
        self.assertFalse(
            self.game.is_occupied_by_player_in_turn(players_initial_pasture))

        computers_initial_pasture = self.play_initial_turn()
        self.assertTrue(computers_initial_pasture.is_occupied_by_computer())
        self.assertFalse(
            self.game.is_occupied_by_player_in_turn(computers_initial_pasture))

        self.assertTrue(players_initial_pasture.is_occupied_by_player())
        self.assertTrue(
            self.game.is_occupied_by_player_in_turn(players_initial_pasture))

    def test_initial_phase_is_calculated_correctly(self):
        self.assertTrue(self.game.is_in_initial_placement())
        self.play_initial_turn()
        self.assertTrue(self.game.is_in_initial_placement())
        self.game.next_turn()
        self.assertFalse(self.game.is_in_initial_placement())

    def test_game_is_not_over_before_initial_sheep_are_placed(self):
        self.assertFalse(self.game.is_over())
        self.assertFalse(self.game.is_over_for_player_in_turn())
        self.assertFalse(self.game.is_over_for_player())
        self.assertFalse(self.game.is_over_for_computer())

        self.play_initial_turn()
        self.assertFalse(self.game.is_over())
        self.assertFalse(self.game.is_over_for_player_in_turn())
        self.assertFalse(self.game.is_over_for_player())
        self.assertFalse(self.game.is_over_for_computer())

    def test_can_choose_own_pasture(self):
        pasture = self.play_initial_turn()
        self.game.next_turn()
        self.game.click(pasture.centre)
        self.assertEqual(self.game.chosen_pasture, pasture)

    def test_changing_turn_resets_targeted_pastures(self):
        pasture = self.play_initial_turn()
        self.game.next_turn()
        self.game.click(pasture.centre)

        self.game.next_turn()

        self.assertEqual(self.game.get_amount_of_targeted_pastures(), 0)

    def test_can_choose_target_pasture(self):
        _, target = self.choose_target_pasture()
        self.assertEqual(self.game.target_pasture, target)

    def test_changing_turn_resets_chosen_and_target_pastures(self):
        self.choose_target_pasture()
        self.game.next_turn()
        self.assertIsNone(self.game.chosen_pasture)
        self.assertIsNone(self.game.target_pasture)

    def test_at_default_one_sheep_is_added_to_target(self):
        source, target = self.choose_target_pasture()
        self.assertEqual(source.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 1)
        self.assertEqual(target.get_amount_of_planned_sheep(), 1)

    def test_an_additional_sheep_is_added_to_target_correctly(self):
        source, target = self.choose_target_pasture()
        self.game.scroll_up()
        self.assertEqual(source.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 2)
        self.assertEqual(target.get_amount_of_planned_sheep(), 2)

    def test_ten_additional_sheep_are_added_to_target_correctly(self):
        source, target = self.choose_target_pasture()
        self.add_sheep_to_target(10)
        self.assertEqual(source.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 11)
        self.assertEqual(target.get_amount_of_planned_sheep(), 11)

    def test_at_max_all_but_one_sheep_can_be_added_to_target(self):
        source, target = self.choose_target_pasture()
        self.add_sheep_to_target(100)
        self.assertEqual(source.get_amount_of_planned_sheep(), 1)
        self.assertEqual(target.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 1)

    def test_adding_sheep_can_be_reversed(self):
        source, target = self.choose_target_pasture()
        self.add_sheep_to_target(10)
        self.subtract_sheep_from_target(10)
        self.assertEqual(source.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 1)
        self.assertEqual(target.get_amount_of_planned_sheep(), 1)

    def test_at_least_one_sheep_must_be_on_target(self):
        source, target = self.choose_target_pasture()
        self.subtract_sheep_from_target(10)
        self.assertEqual(source.get_amount_of_planned_sheep(),
                         INITIAL_SHEEP - 1)
        self.assertEqual(target.get_amount_of_planned_sheep(), 1)

    def test_min_amount_of_sheep_is_moved_to_target_correctly(self):
        source, target = self.choose_target_pasture()
        self.game.press_enter()
        self.assertEqual(source.get_amount_of_sheep(), INITIAL_SHEEP - 1)
        self.assertEqual(target.get_amount_of_sheep(), 1)

    def test_max_amount_of_sheep_is_moved_to_target_correctly(self):
        source, target = self.choose_target_pasture()
        self.add_sheep_to_target(INITIAL_SHEEP - 2)
        self.game.press_enter()
        self.assertEqual(source.get_amount_of_sheep(), 1)
        self.assertEqual(target.get_amount_of_sheep(), INITIAL_SHEEP - 1)

    def test_initial_turn_can_be_undone(self):
        initial_pasture = self.play_initial_turn()
        self.assertTrue(initial_pasture.is_occupied())
        self.assertEqual(initial_pasture.get_amount_of_sheep(), INITIAL_SHEEP)
        # Pelaaja aloittaa, joten ensimmäisen vuoron jälkeen on tekoälyn vuoro.
        self.assertTrue(self.game.is_computers_turn())
        self.assertEqual(self.game.get_number_of_turn(), 2)

        self.game.undo_initial_turn(initial_pasture)

        self.assertTrue(initial_pasture.is_free())
        self.assertEqual(initial_pasture.get_amount_of_sheep(), 0)
        self.assertTrue(self.game.is_players_turn)
        self.assertEqual(self.game.get_number_of_turn(), 1)

    def test_normal_turn_can_be_undone(self):
        source, target = self.choose_target_pasture()
        self.game.press_enter()

        self.assertTrue(self.game.is_computers_turn())
        self.assertTrue(source.is_occupied())
        self.assertEqual(source.get_amount_of_sheep(), INITIAL_SHEEP - 1)
        self.assertTrue(target.is_occupied())
        self.assertEqual(target.get_amount_of_sheep(), 1)
        self.assertEqual(self.game.get_number_of_turn(), 4)

        self.game.undo_normal_turn(source, target, 1)

        self.assertTrue(self.game.is_players_turn)
        self.assertTrue(source.is_occupied())
        self.assertEqual(source.get_amount_of_sheep(), INITIAL_SHEEP)
        self.assertTrue(target.is_free())
        self.assertEqual(target.get_amount_of_sheep(), 0)
        self.assertEqual(self.game.get_number_of_turn(), 3)

    def test_game_is_over_if_no_more_sheep_left_to_move(self):
        players_initial_pasture = self.play_initial_turn()
        computers_initial_pasture = self.play_initial_turn()
        players_initial_pasture.sheep = 1

        self.assertTrue(self.game.is_over_for_player())
        self.assertTrue(self.game.is_over_for_player_in_turn())
        self.assertFalse(self.game.is_over_for_computer())
        self.assertFalse(self.game.is_over())

        computers_initial_pasture.sheep = 1
        self.assertTrue(self.game.is_over_for_computer())
        self.assertTrue(self.game.is_over())

    def test_game_is_over_if_all_sheep_are_surrounded(self):
        players_initial_pasture = self.play_initial_turn()
        self.play_initial_turn()

        self.occupy_neighbours(players_initial_pasture, COMPUTER, 2)

        self.assertTrue(self.game.is_over_for_player())
        self.assertTrue(self.game.is_over_for_player_in_turn())
        self.assertFalse(self.game.is_over_for_computer())
        self.assertFalse(self.game.is_over())

    def test_game_is_not_over_if_there_is_a_single_move_left(self):
        players_initial_pasture = self.play_initial_turn()
        self.play_initial_turn()

        self.occupy_neighbours(players_initial_pasture, COMPUTER, 2)

        # Tyhjennetään yksi naapureista
        players_initial_pasture.get_neighbours(self.game.pastures)[0].reset()

        self.assertFalse(self.game.is_over_for_player())
        self.assertFalse(self.game.is_over_for_player_in_turn())

    def test_turn_changes_correctly_if_player_can_not_move_anymore(self):
        players_pasture = self.play_initial_turn()
        self.play_initial_turn()
        self.game.next_turn()
        self.assertTrue(self.game.is_computers_turn())
        players_pasture.sheep = 1

        self.game.next_turn()
        self.assertTrue(self.game.is_computers_turn())
        self.assertTrue(self.game.is_over_for_player())
        self.assertFalse(self.game.is_over_for_computer())

    def test_turn_changes_correctly_if_computer_can_not_move_anymore(self):
        self.play_initial_turn()
        computers_pasture = self.play_initial_turn()
        self.assertTrue(self.game.is_players_turn)
        computers_pasture.sheep = 1

        self.game.next_turn()
        self.assertTrue(self.game.is_players_turn)
        self.assertFalse(self.game.is_over_for_player())
        self.assertTrue(self.game.is_over_for_computer())

    def test_winner_is_calculated_correctly_for_a_player_victory(self):
        self.win_game_by_player()
        self.assertTrue(self.game.is_over())
        self.assertTrue(self.game.is_player_the_winner())

    def test_winner_is_calculated_correctly_for_a_computer_victory(self):
        self.win_game_by_computer()
        self.assertTrue(self.game.is_over())
        self.assertFalse(self.game.is_player_the_winner())

    # def test_game_state_is_calculated_correctly_for_a_player_victory(self):
    #     self.win_game_by_player()
    #     self.assertEqual(self.game.evaluate_game_state(), float('Inf'))

    # def test_game_state_is_calculated_correctly_for_a_computer_victory(self):
    #     self.win_game_by_computer()
    #     self.assertEqual(self.game.evaluate_game_state(), float('-Inf'))

    def test_undoing_players_last_move_works_correctly(self):
        players_pasture = self.play_initial_turn()
        computers_pasture = self.play_initial_turn()

        # Tehdään vuorosta pelin viimeinen
        players_pasture.sheep = 2
        computers_pasture.sheep = 1
        self.assertFalse(self.game.is_over_for_player())
        self.assertTrue(self.game.is_over_for_computer())

        # Tehdään viimeinen siirto
        self.game.click(players_pasture.centre)
        target = players_pasture.get_any_potential_target(self.game.pastures)
        if not target:
            raise SystemError('No potential targets found')
        self.game.click(target.centre)
        self.game.press_enter()
        self.assertTrue(self.game.is_over())
        self.assertTrue(self.game.is_over_for_player())
        self.assertTrue(self.game.is_player_the_winner())

        # Perutaan siirto
        self.game.undo_normal_turn(
            players_pasture, target, 1)
        self.assertFalse(self.game.is_over())
        self.assertFalse(self.game.is_over_for_player())
        self.assertFalse(self.game.is_player_the_winner())

    def test_undoing_computers_last_move_works_correctly(self):
        players_pasture = self.play_initial_turn()
        computers_pasture = self.play_initial_turn()
        # Hypätään pelaajan vuoron yli
        self.game.next_turn()

        # Tehdään vuorosta pelin viimeinen
        players_pasture.sheep = 1
        computers_pasture.sheep = 2
        self.assertTrue(self.game.is_over_for_player())
        self.assertFalse(self.game.is_over_for_computer())

        # Tehdään viimeinen siirto
        target = computers_pasture.get_any_potential_target(
            self.game.pastures)
        if not target:
            raise SystemError('No potential targets found')
        self.game.make_normal_turn(computers_pasture, target, 1)
        self.assertTrue(self.game.is_over())
        self.assertTrue(self.game.is_over_for_computer())
        self.assertFalse(self.game.is_player_the_winner())

        # Perutaan siirto
        self.game.undo_normal_turn(
            computers_pasture, target, 1)
        self.assertFalse(self.game.is_over())
        self.assertFalse(self.game.is_over_for_computer())
        self.assertFalse(self.game.is_player_the_winner())
