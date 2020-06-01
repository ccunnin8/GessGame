import unittest
from GessGame import Board, Piece, GessGame


class TestGame(unittest.TestCase):

    def test_it_can_determine_a_valid_move(self):
        game = GessGame()
        self.assertFalse(game.is_valid_move("f5", "l7"))
        self.assertFalse(game.is_valid_move("a0", "a3"))
        self.assertFalse(game.is_valid_move("p1", "h9"))
        self.assertFalse(game.is_valid_move("g9", "q4"))
        self.assertFalse(game.is_valid_move("k16", "k14"))
        self.assertFalse(game.is_valid_move("a3", "b3"))
        self.assertFalse(game.is_valid_move("b18", "a18"))
        self.assertFalse(game.is_valid_move("r3", "t3"))
        self.assertFalse(game.is_valid_move("r18", "r20"))
        self.assertFalse(game.is_valid_move("c18", "c20"))
        self.assertFalse(game.make_move("ADSGASDGASD", "ADSFASDFASDFASDF"))

    def test_determine_direction(self):
        game = GessGame()
        self.assertEqual("E", game.determine_direction(0, 0, 0, 3))
        self.assertEqual("W", game.determine_direction(5, 10, 5, 3))
        self.assertEqual("N", game.determine_direction(12, 4, 9, 4))
        self.assertEqual("NE", game.determine_direction(5, 5, 4, 6))
        self.assertEqual("NW", game.determine_direction(7, 10, 5, 4))
        self.assertEqual("S", game.determine_direction(6, 3, 10, 3))
        self.assertEqual("SW", game.determine_direction(6, 6, 8, 4))
        self.assertEqual("SE", game.determine_direction(6, 6, 10, 15))

    def test_analyze_piece(self):
        game = GessGame()
        piece = [
            [None, "X", None],
            [None, None, None],
            [None, None, None]
        ]
        self.assertListEqual(game.analyze_piece(piece), ["N"])
        piece2 = [
            ["X","X","X"],
            ["X","X","X"],
            ["X","X","X"]
        ]
        self.assertSetEqual(set(game.analyze_piece(piece2)), set(["N", "E", "W", "S", "SE", "SW", "NE", "NW", "C"]))

    def test_is_valid_move(self):
        board = Board()
        board.print()
        game = GessGame()
        self.assertFalse(game.is_valid_move("b3", "b4"))
        self.assertFalse(game.is_valid_move("b3", "b4"))
        self.assertFalse(game.is_valid_move("b2", "b16"))
        self.assertFalse(game.is_valid_move("f7", "f8"))
        self.assertFalse(game.is_valid_move("f7", "f6"))
        self.assertFalse(game.is_valid_move("f14", "e13"))
        self.assertFalse(game.is_valid_move("f14", "g13"))
        self.assertFalse(game.is_valid_move("f14", "e15"))
        self.assertFalse(game.is_valid_move("f14", "g15"))
        self.assertFalse(game.is_valid_move("k18", "k17"))
        self.assertFalse(game.is_valid_move("h10", "i10"))
        self.assertTrue(game.is_valid_move("c3", "d3"))
        self.assertFalse(game.is_valid_move("x2", "B4"))


    def test_analyze_rings(self):
        board = Board()
        board.print()
        game = GessGame()
        game._rings = {}
        game.analyze_rings()
        print(game._rings)
        self.assertEqual(len(game._rings["player1"]), 1)
        self.assertEqual(len(game._rings["player2"]), 1)

    def test_player_can_resign(self):
        game = GessGame()
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        game.resign_game()
        self.assertEqual(game.get_game_state(), "WHITE_WON")
        game = GessGame()
        game.toggle_turn()
        game.resign_game()
        self.assertEqual(game.get_game_state(), "BLACK_WON")
