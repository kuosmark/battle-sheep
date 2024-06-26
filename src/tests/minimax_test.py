from typing import Tuple
import unittest
from constants import (
    ALPHA,
    BETA,
    COMPUTER,
    PLAYER
)
from minimax import (get_possible_moves, minimax)
from game import Game


BOARD_HEIGHT = 4
BOARD_WIDTH = 4
AMOUNT_OF_PASTURES = BOARD_HEIGHT * BOARD_WIDTH


class TestMinimax(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(BOARD_HEIGHT, BOARD_WIDTH, is_simulation=False)

    # Apumetodit

    def is_over_for_opponent(self) -> bool:
        if self.game.is_players_turn:
            return self.game.is_over_for_computer()
        return self.game.is_over_for_player()

    def get_amount_of_players_sheep(self) -> int:
        return sum(p.get_amount_of_sheep() for p in self.game.get_pastures_occupied_by_player())

    def get_amount_of_computers_sheep(self) -> int:
        return sum(p.get_amount_of_sheep() for p in self.game.get_pastures_occupied_by_computer())

    # Get_possible_moves

    def get_amount_of_possible_moves_for(self, player: int) -> int:
        was_players_turn = self.game.is_players_turn

        self.game.is_players_turn = player == PLAYER
        possible_moves = len(get_possible_moves(
            self.game, self.game.is_players_turn))

        self.game.is_players_turn = was_players_turn
        return possible_moves

    def get_move_with_highest_value(self, game: Game) -> Tuple[float, Game | None]:
        possible_moves = get_possible_moves(game, game.is_players_turn)
        highest_value = float('-inf')
        best_move: Game | None = None

        for move in possible_moves:
            move_value = move.evaluate_game_state()
            if move_value > highest_value:
                highest_value = move_value
                best_move = move
        return highest_value, best_move

    def get_move_with_lowest_value(self, game: Game) -> Tuple[float, Game | None]:
        possible_moves = get_possible_moves(game, game.is_players_turn)
        lowest_value = float('inf')
        best_move: Game | None = None

        for move in possible_moves:
            move_value = move.evaluate_game_state()
            if move_value < lowest_value:
                lowest_value = move_value
                best_move = move
        return lowest_value, best_move

    def make_best_next_move(self) -> None:
        possible_next_moves = get_possible_moves(
            self.game, self.game.is_players_turn)
        if len(possible_next_moves) > 0:
            self.game = possible_next_moves[0]

    def make_worst_next_move(self) -> None:
        possible_next_moves = get_possible_moves(
            self.game, self.game.is_players_turn)
        if len(possible_next_moves) > 0:
            self.game = possible_next_moves[-1]

    def play_game_for_turns(self, turns: int) -> None:
        for _ in range(turns):
            self.make_best_next_move()

    def play_full_game_against_the_worst(self, is_player: bool) -> None:
        for _ in range(AMOUNT_OF_PASTURES):
            if is_player == self.game.is_players_turn:
                self.make_best_next_move()
            else:
                self.make_worst_next_move()

    # Minimax

    def get_best_move_using_minimax(self, depth: int, max_player: bool) -> Game | None:
        _, move = minimax(self.game, depth, ALPHA, BETA, max_player)
        return move

    def make_best_move_using_minimax(self, depth: int, max_player: bool) -> None:
        next_move = self.get_best_move_using_minimax(depth, max_player)
        if next_move is not None:
            self.game = next_move

    def play_full_game_using_minimax(self, player_depth: int, computer_depth: int) -> None:
        for _ in range(AMOUNT_OF_PASTURES):
            players_turn = self.game.is_players_turn
            depth = player_depth if players_turn else computer_depth
            self.make_best_move_using_minimax(depth, players_turn)

    def play_full_game_using_minimax_against_the_worst(self, depth: int, is_player: bool) -> None:
        for _ in range(AMOUNT_OF_PASTURES):
            if is_player == self.game.is_players_turn:
                self.make_best_move_using_minimax(depth, is_player)
            else:
                self.make_worst_next_move()

    def play_game_using_minimax_until_winning_move_is_found(
            self, depth: int, is_player: bool) -> bool:
        winning_value = float('inf') if is_player else float('-inf')

        for _ in range(AMOUNT_OF_PASTURES):
            if is_player == self.game.is_players_turn:
                move_value, move = minimax(
                    self.game, depth, ALPHA, BETA, is_player)
                if move_value == winning_value:
                    print('arvo on' + str(move_value))
                    return True
                if move is not None:
                    self.game = move
            else:
                self.make_best_next_move()

        return False

    # Testit

    def test_correct_amounts_of_possible_initial_moves_are_found(self):
        amount_of_edge_pastures = self.game.get_amount_of_edge_pastures()
        possible_first_turns = get_possible_moves(
            self.game, self.game.is_players_turn)
        self.assertEqual(len(possible_first_turns), amount_of_edge_pastures)

        first_turn = possible_first_turns[0]
        possible_second_turns = get_possible_moves(
            first_turn, first_turn.is_players_turn)
        self.assertEqual(len(possible_second_turns),
                         amount_of_edge_pastures - 1)

    def test_possible_moves_are_sorted_best_first(self):
        best_value, best_first_move = self.get_move_with_highest_value(
            (self.game))
        self.assertEqual(best_value, get_possible_moves(self.game, self.game.is_players_turn
                                                        )[0].evaluate_game_state())

        best_value, _ = self.get_move_with_lowest_value(best_first_move)
        self.assertEqual(best_value, get_possible_moves(best_first_move, best_first_move.is_players_turn
                                                        )[0].evaluate_game_state())

    def test_game_value_is_evaluated_correclty(self):
        self.assertEqual(self.game.evaluate_game_state(), 0)
        self.play_game_for_turns(2)
        game_value = self.get_amount_of_possible_moves_for(
            PLAYER) - self.get_amount_of_possible_moves_for(COMPUTER)
        self.assertEqual(self.game.evaluate_game_state(), game_value)

        self.play_game_for_turns(2)
        game_value = self.get_amount_of_possible_moves_for(
            PLAYER) - self.get_amount_of_possible_moves_for(COMPUTER)
        self.assertEqual(self.game.evaluate_game_state(), game_value)

        self.play_game_for_turns(1)
        game_value = self.get_amount_of_possible_moves_for(
            PLAYER) - self.get_amount_of_possible_moves_for(COMPUTER)
        self.assertEqual(self.game.evaluate_game_state(), game_value)

    def test_total_amount_of_sheep_does_not_change(self):
        self.play_game_for_turns(2)
        self.assertEqual(self.get_amount_of_players_sheep(),
                         self.game.initial_sheep)
        self.assertEqual(self.get_amount_of_computers_sheep(),
                         self.game.initial_sheep)

        self.play_game_for_turns(2)
        self.assertEqual(self.get_amount_of_players_sheep(),
                         self.game.initial_sheep)
        self.assertEqual(self.get_amount_of_computers_sheep(),
                         self.game.initial_sheep)

        self.play_game_for_turns(2)
        self.assertEqual(self.get_amount_of_players_sheep(),
                         self.game.initial_sheep)
        self.assertEqual(self.get_amount_of_computers_sheep(),
                         self.game.initial_sheep)

    def test_turns_are_calculated_correctly(self):
        self.play_game_for_turns(1)
        self.assertTrue(self.game.is_in_initial_placement())
        self.assertFalse(self.game.is_players_turn)

        self.play_game_for_turns(1)
        self.assertFalse(self.game.is_in_initial_placement())
        self.assertTrue(self.game.is_players_turn)

        self.play_game_for_turns(1)
        self.assertFalse(self.game.is_players_turn)

        self.play_game_for_turns(1)
        self.assertTrue(self.game.is_players_turn)

    def test_turn_changes_to_opponent_if_is_not_over_for_player(self):
        self.play_game_for_turns(3)
        is_players_turn = self.game.is_players_turn

        self.play_game_for_turns(1)
        self.assertTrue(self.game.is_players_turn != is_players_turn
                        or self.is_over_for_opponent())

        self.play_game_for_turns(2)
        is_players_turn = self.game.is_players_turn

        self.play_game_for_turns(1)
        self.assertTrue(self.game.is_players_turn != is_players_turn
                        or self.is_over_for_opponent())

        self.play_game_for_turns(1)
        is_players_turn = self.game.is_players_turn

        self.play_game_for_turns(1)
        self.assertTrue(self.game.is_players_turn != is_players_turn
                        or self.is_over_for_opponent())

    def test_correct_amount_of_pastures_are_occupied(self):
        self.assertEqual(len(self.game.get_occupied_pastures()), 0)
        self.play_game_for_turns(3)
        self.assertEqual(len(self.game.get_occupied_pastures()), 3)
        self.play_game_for_turns(3)
        self.assertEqual(len(self.game.get_occupied_pastures()), 6)

    def test_game_mut_be_over_after_maximum_amount_of_turns(self):
        self.play_game_for_turns(AMOUNT_OF_PASTURES)
        self.assertTrue(self.game.is_over_for_player())
        self.assertTrue(self.game.is_over_for_computer())
        self.assertTrue(self.game.is_over())

    def test_minimax_returns_the_best_initial_move_for_player_when_using_depth_1(self):
        move = self.get_best_move_using_minimax(1, self.game.is_players_turn)

        best_value, _ = self.get_move_with_highest_value((self.game))
        self.assertEqual(move.evaluate_game_state(), best_value)

    def test_minimax_returns_the_best_initial_move_for_computer_when_using_depth_1(self):
        self.play_game_for_turns(1)
        move = self.get_best_move_using_minimax(1, self.game.is_players_turn)

        best_value, _ = self.get_move_with_lowest_value((self.game))
        self.assertEqual(move.evaluate_game_state(), best_value)

    def test_minimax_returns_the_best_move_on_turn_5(self):
        self.play_game_for_turns(4)
        move = self.get_best_move_using_minimax(1, self.game.is_players_turn)

        best_value, _ = self.get_move_with_highest_value((self.game))
        self.assertEqual(move.evaluate_game_state(), best_value)

    def test_player_making_the_best_move_beats_opponent_making_the_worst_move(self):
        self.play_full_game_against_the_worst(is_player=True)
        self.assertTrue(self.game.is_over())
        self.assertEqual(self.game.calculate_winner(), PLAYER)
        self.assertEqual(self.game.evaluate_game_state(), float('inf'))

    def test_computer_making_the_best_move_beats_opponent_making_the_worst_move(self):
        self.play_full_game_against_the_worst(is_player=False)
        self.assertTrue(self.game.is_over())
        self.assertEqual(self.game.calculate_winner(), COMPUTER)
        self.assertEqual(self.game.evaluate_game_state(), float('-inf'))

    def test_player_using_minimax_beats_opponent_making_the_worst_move(self):
        self.play_full_game_using_minimax_against_the_worst(
            depth=3, is_player=True)
        self.assertTrue(self.game.is_over())
        self.assertEqual(self.game.calculate_winner(), PLAYER)
        self.assertEqual(self.game.evaluate_game_state(), float('inf'))

    def test_computer_using_minimax_beats_opponent_making_the_worst_move(self):
        self.play_full_game_using_minimax_against_the_worst(
            depth=3, is_player=False)
        self.assertTrue(self.game.is_over())
        self.assertEqual(self.game.calculate_winner(), COMPUTER)
        self.assertEqual(self.game.evaluate_game_state(), float('-inf'))

    # Algoritmi osaa voittaa pelin

    def player_wins_game_if_minimax_finds_winning_move(self, depth: int):
        winning_move_found = self.play_game_using_minimax_until_winning_move_is_found(
            depth, is_player=True)

        if winning_move_found:
            # Pelataan syvyyden verran vuoroja eteenpäin, minkä jälkeen pelin pitäisi olla voitettu
            for _ in range(depth):
                self.make_best_move_using_minimax(
                    depth, self.game.is_players_turn)

            self.assertTrue(self.game.is_over_for_computer())
            self.assertEqual(self.game.evaluate_game_state(), float('inf'))
            self.assertEqual(self.game.calculate_winner(), PLAYER)
        else:
            self.assertTrue(self.game.is_over())

    def computer_wins_game_if_minimax_finds_winning_move(self, depth: int):
        winning_move_found = self.play_game_using_minimax_until_winning_move_is_found(
            depth, is_player=False)

        if winning_move_found:
            # Pelataan syvyyden verran vuoroja eteenpäin, minkä jälkeen pelin pitäisi olla voitettu
            for _ in range(depth):
                self.make_best_move_using_minimax(
                    depth, self.game.is_players_turn)

            self.assertTrue(self.game.is_over_for_player())
            self.assertEqual(self.game.evaluate_game_state(), float('-inf'))
            self.assertEqual(self.game.calculate_winner(), COMPUTER)
        else:
            self.assertTrue(self.game.is_over())

    # Syvyys 1

    def test_player_wins_if_depth_1_minimax_finds_winning_move_against_best_opponent(self):
        self.player_wins_game_if_minimax_finds_winning_move(depth=1)

    def test_computer_wins_if_depth_1_minimax_finds_winning_move_against_best_opponent(self):
        self.computer_wins_game_if_minimax_finds_winning_move(depth=1)

    # Syvyys 2

    def test_player_wins_if_depth_2_minimax_finds_winning_move_against_best_opponent(self):
        self.player_wins_game_if_minimax_finds_winning_move(depth=2)

    def test_computer_wins_if_depth_2_minimax_finds_winning_move_against_best_opponent(self):
        self.computer_wins_game_if_minimax_finds_winning_move(depth=2)

    # Syvyys 3

    def test_player_wins_if_depth_3_minimax_finds_winning_move_against_best_opponent(self):
        self.player_wins_game_if_minimax_finds_winning_move(depth=3)

    def test_computer_wins_if_depth_3_minimax_finds_winning_move_against_best_opponent(self):
        self.computer_wins_game_if_minimax_finds_winning_move(depth=3)

    # Syvyys 4

    def test_player_wins_if_depth_4_minimax_finds_winning_move_against_best_opponent(self):
        self.player_wins_game_if_minimax_finds_winning_move(depth=4)

    def test_computer_wins_if_depth_4_minimax_finds_winning_move_against_best_opponent(self):
        self.computer_wins_game_if_minimax_finds_winning_move(depth=4)

    # Syvyys 5

    def test_player_wins_if_depth_5_minimax_finds_winning_move_against_best_opponent(self):
        self.player_wins_game_if_minimax_finds_winning_move(depth=5)

    def test_computer_wins_if_depth_5_minimax_finds_winning_move_against_best_opponent(self):
        self.computer_wins_game_if_minimax_finds_winning_move(depth=5)
