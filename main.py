import random
from typing import List, Union

STRIKE = -1
SPARE = -2


class Frame:
    def __init__(self):
        self.rolls: List[Union[int, str]] = []

    def is_strike(self) -> bool:
        if not self.rolls:
            return False
        return self.rolls[0] == STRIKE

    def is_spare(self) -> bool:
        if not self.rolls or len(self.rolls) <= 1:
            return False
        return self.rolls[1] == SPARE


class Player:
    def __init__(self, name: str):
        self.name = name
        self.frames: List[Frame] = []


class Game:
    def __init__(self, players: List[Player]):
        self.players = players

    def roll(self, player: Player) -> None:
        total_pins = 10
        remaining_pins = total_pins
        rolls_per_frame = 2
        frame = Frame()
        for i in range(rolls_per_frame):
            pins = random.randint(0, remaining_pins)
            if (pins == remaining_pins) and (i == 0):
                frame.rolls.append(STRIKE)
                player.frames.append(frame)
                return
            elif (pins == remaining_pins) and (i == 1):
                frame.rolls.append(SPARE)
                player.frames.append(frame)
                return
            else:
                remaining_pins -= pins
                frame.rolls.append(pins)
        player.frames.append(frame)

    def roll_last_frame(self, player: Player) -> None:
        total_pins = 10
        remaining_pins = total_pins
        frame = Frame()
        player.frames

        # First Roll
        first_roll = random.randint(0, total_pins)
        if first_roll == total_pins:
            frame.rolls.append(STRIKE)
        else:
            frame.rolls.append(first_roll)
            remaining_pins -= first_roll

        # Second Roll
        second_roll = random.randint(0, remaining_pins)
        if frame.rolls[0] == STRIKE:
            if second_roll == remaining_pins:
                frame.rolls.append(STRIKE)
            else:
                frame.rolls.append(second_roll)
                remaining_pins -= second_roll
        elif second_roll == remaining_pins:
            frame.rolls.append(SPARE)
            remaining_pins = total_pins
        else:
            frame.rolls.append(second_roll)
            player.frames.append(frame)
            return

        # Bonus Roll
        last_roll = random.randint(0, remaining_pins)
        if (last_roll == total_pins) and (frame.rolls[-1] < 0):
            frame.rolls.append(STRIKE)
        elif last_roll == remaining_pins:
            frame.rolls.append(SPARE)
        else:
            frame.rolls.append(last_roll)
        player.frames.append(frame)

    def play_frame(self, is_last_frame: bool) -> None:
        for player in self.players:
            if is_last_frame:
                self.roll_last_frame(player)
            else:
                self.roll(player)

    def start(self):
        num_frames = 10
        for frame in range(1, num_frames + 1):
            is_last_frame = frame == num_frames
            self.play_frame(is_last_frame)

    def print_scoreboard(self):
        print("\n---------------------")
        print("FINAL SCOREBOARD")
        print("---------------------\n")
        winner = ""
        max_score = -float("inf")
        for player in self.players:
            print("***********************")
            print(player.name, "\n")
            for frame in player.frames:
                print("|", end=" ")
                for roll in frame.rolls:
                    if roll == STRIKE:
                        strike_char = "X"
                        print(strike_char, end=" ")
                    elif roll == SPARE:
                        spare_char = "/"
                        print(spare_char, end=" ")
                    else:
                        print(roll, end=" ")
            print("|", end=" ")
            total_score = self.get_player_score(player)
            if total_score > max_score:
                max_score = total_score
                winner = player.name
            print("\n\nTotal:", total_score)
            print("***********************\n")
        print("********************\n")
        print("WINNER, WINNER, SOMETHING DINNER!\n")
        print(f"{winner} won!!!")
        print("\n********************")

    def get_player_score(self, player: Player) -> int:
        total_score = 0
        for frame_num, frame in enumerate(player.frames):
            if frame_num == 9:
                points = self.calculate_last_frame(frame)
                total_score += points
            elif frame.is_strike():
                points = self.calculate_strike_points(frame_num, player.frames)
                total_score += points
            elif frame.is_spare():
                points = self.calculate_spare_points(frame_num, player.frames)
                total_score += points
            else:
                points = sum(frame.rolls)
                total_score += points
        return total_score

    def calculate_strike_points(self, frame_num: int, frames: List[Frame]) -> int:
        """Strike is 10 + the next two rolls"""
        extra_rolls: int = 2
        points: int = 10
        roll_count: int = 0
        next_frame_index = frame_num + 1
        while roll_count < extra_rolls:
            next_frame = frames[next_frame_index]
            if next_frame_index == 9:
                remaining_rolls = next_frame.rolls[: extra_rolls - roll_count]
                if roll_count == 0 and remaining_rolls[1] == SPARE:
                    points += 10
                    roll_count += 2
                    break
                for roll in remaining_rolls:
                    if roll == STRIKE:
                        points += 10
                    else:
                        points += roll
                    roll_count += 1
                break
            elif next_frame.is_strike():
                points += 10
                roll_count += 1
            elif roll_count == 0 and next_frame.is_spare():
                points += 10
                roll_count += 2
            else:
                rolls_remaining = extra_rolls - roll_count
                roll_count += rolls_remaining
                points += sum(next_frame.rolls[:rolls_remaining])
            next_frame_index += 1
        return points

    def calculate_spare_points(self, frame_num: int, frames: List[Frame]) -> int:
        """Spare is 10 + the next roll."""
        points: int = 10
        next_frame = frames[frame_num + 1]
        if next_frame.is_strike():
            points += 10
        else:
            next_roll = next_frame.rolls[0]
            points += next_roll
        return points

    def calculate_last_frame(self, frame: Frame) -> int:
        """"""
        points: int = 0
        if len(frame.rolls) == 2:
            points += sum(frame.rolls)
            return points
        max_rolls = 3
        for i in range(max_rolls):
            curr_roll = frame.rolls[i]
            if curr_roll == STRIKE:
                points += 10
            elif curr_roll == SPARE:
                points += 10
            elif i == 1 and frame.rolls[i + 1] != SPARE:
                points += curr_roll
            elif i == 2:
                points += curr_roll
        return points


def parse_num_players() -> int:
    """
    """
    min_players = 2
    max_players = 4
    invalid_input_response = -1
    num_input: str = input(f"How many players? Up to {max_players}...\n")
    is_digit: bool = num_input.isdigit()
    if not is_digit:
        return invalid_input_response
    num = int(num_input)
    is_valid_range: bool = (min_players <= num <= max_players)
    if not is_valid_range:
        return invalid_input_response
    return num


def parse_player_info(num_players: int) -> List[Player]:
    player_info: List[Player] = []
    for i in range(1, num_players + 1):
        name = input(f"Enter Player {i}'s name...\n")
        player = Player(name)
        player_info.append(player)
    return player_info


def calculate_last_frame():
    pass


if __name__ == "__main__":
    num_players = parse_num_players()
    if num_players == -1:
        print("Invalid number of players.")
        exit(0)
    players = parse_player_info(num_players)
    game = Game(players)
    game.start()
    game.print_scoreboard()
