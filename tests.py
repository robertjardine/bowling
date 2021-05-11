"""
"""

import unittest
from typing import List
from unittest import mock
from unittest.mock import patch

import main


class MainTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_parse_num_players_happy_path(self):
        user_inputs = ("2", "3", "4")
        expected_output = (2, 3, 4)
        for user_input, expected in zip(user_inputs, expected_output):
            with patch("builtins.input", side_effect=user_input):
                num_players = main.parse_num_players()
                self.assertEqual(num_players, expected)

    def test_parse_num_players_invalid(self):
        user_inputs = ("-1", "0", "1", "5")
        expected_result = -1
        for user_input in user_inputs:
            with patch("builtins.input", side_effect=user_input):
                num_players = main.parse_num_players()
                self.assertEqual(num_players, expected_result)

    @mock.patch("builtins.input")
    def test_parse_num_players_noninterger_input(self, input_mock):
        user_inputs = ("abc", "$#k", "12a", "1n")
        expected_result = -1
        for user_input in user_inputs:
            input_mock.return_value = user_input
            num_players = main.parse_num_players()
            self.assertEqual(num_players, expected_result)

    def test_parse_player_info_happy_path(self) -> None:
        names = ["Bob", "Alice"]
        num_players = len(names)
        expected_response = [
            main.Player("Bob"),
            main.Player("Alice"),
        ]
        with patch("builtins.input", side_effect=names):
            player_info = main.parse_player_info(num_players)
            for player, expected in zip(player_info, expected_response):
                self.assertEqual(player.name, expected.name)
                self.assertListEqual(player.frames, [])

    def test_last_frame(self) -> None:
        """
        Tenth frame combinations:
            xxx
            xx1
            x2/
            x22
            2/x
            2/2
        """
        frame = main.Frame()
        all_rolls = [
            ([1, 2], 3),
            ([main.STRIKE, main.STRIKE, main.STRIKE], 30),
            ([main.STRIKE, main.STRIKE, 7], 27),
            ([main.STRIKE, 2, 3], 15),
            ([main.STRIKE, 8, main.SPARE], 20),
            ([1, main.SPARE, main.STRIKE], 20),
            ([4, main.SPARE, 8], 18),
        ]
        game = main.Game([])
        for rolls, expected in all_rolls:
            frame.rolls = rolls
            points = game.calculate_last_frame(frame)
            self.assertEqual(points, expected)

    def test_calculate_stike_points(self) -> None:
        frame_num = 0
        curr_frame = main.Frame()
        curr_frame.rolls = [main.STRIKE]
        next_frame = main.Frame()
        all_roles = [([1, 2], 13), ([1, main.SPARE], 20)]
        game = main.Game([])
        for rolls, expected in all_roles:
            next_frame.rolls = rolls
            frames: List[main.Frame] = [curr_frame, next_frame]
            points = game.calculate_strike_points(frame_num, frames)
            self.assertEqual(points, expected)

    def test_calculate_strike_points_multiple_strike(self) -> None:
        frame_num = 0
        curr_frame = main.Frame()
        curr_frame.rolls = [main.STRIKE]
        all_roles = [
            ([main.STRIKE, main.STRIKE], 30),
            ([main.STRIKE, 4], 24),
        ]
        game = main.Game([])
        for rolls, expected in all_roles:
            frames: List[main.Frame] = [curr_frame]
            for roll in rolls:
                next_frame = main.Frame()
                next_frame.rolls = [roll]
                frames.append(next_frame)
            points = game.calculate_strike_points(frame_num, frames)
            self.assertEqual(points, expected)

    def test_calculate_spare_points(self) -> None:
        frame_num = 0
        curr_frame = main.Frame()
        curr_frame.rolls = [5, main.SPARE]
        next_frame = main.Frame()
        all_rolls = [
            ([main.STRIKE], 20),
            ([7, 2], 17),
            ([0, 9], 10),
        ]
        game = main.Game([])
        for rolls, expected in all_rolls:
            next_frame.rolls = rolls
            frames: List[main.Frame] = [curr_frame, next_frame]
            points = game.calculate_spare_points(frame_num, frames)
            self.assertEqual(points, expected)

    def test_get_player_score(self) -> None:
        player = main.Player("Bob")
        game_results = [
            ("X-X-X-X-X-X-X-X-X-X,X,X", 300),  # All Strikes
            ("X-X-X-X-X-X-5,2-X-X-X,X,X", 259),  # Mostly Strikes with one normal frame
            ("0,0-0,0-0,0-0,0-0,0-0,0-0,0-0,0-0,0-0,0", 0),  # All gutter balls
            ("2,/-2,/-2,/-2,/-2,/-2,/-2,/-2,/-2,/-2,/,2", 120),  # All Spares
            ("4,5-5,4-3,6-2,7-0,9-6,3-8,1-1,8-9,0-7,2", 90),  # All open frames
            (
                "0,/-1,/-2,/-3,/-4,/-5,/-6,/-7,/-8,/-9,/,X",
                155,
            ),  # All spares with a final strike
        ]
        game = main.Game([])
        for result, expected in game_results:
            frames = self._parse_frames(result)
            player.frames = frames
            score = game.get_player_score(player)
            self.assertEqual(score, expected)

    def _parse_frames(self, result: str) -> List[main.Frame]:
        frames_split = result.split("-")
        rolls_split = [frame.split(",") for frame in frames_split]
        frames: List[main.Frame] = []
        for rolls in rolls_split:
            curr_rolls = []
            for roll in rolls:
                if roll == "X":
                    curr_rolls.append(main.STRIKE)
                elif roll == "/":
                    curr_rolls.append(main.SPARE)
                else:
                    curr_rolls.append(int(roll))
            new_frame = main.Frame()
            new_frame.rolls = curr_rolls
            frames.append(new_frame)
        return frames
