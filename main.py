#!/usr/bin/env python
from random import randrange, seed

seed(42)
NUM_QUESTIONS = 50
COINS_TO_WIN = 6
DICE_MIN = 1
DICE_MAX = 6
FAILURE_CONDITION = 7


class GameException(Exception):
    pass


class Game:
    def __init__(self, num_questions: int):
        self.players: list[str] = []
        self.purses: list[int] = []
        self.in_penalty_box: list[bool] = []
        self.current_player: int = 0
        self.is_getting_out_of_penalty_box: bool = False
        self.places: list[int] = []

        self._initialize_questions(num_questions)

    def _initialize_questions(self, num_questions: int):

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        for i in range(num_questions):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append("Rock Question %s" % i)

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name: str):
        self.players.append(player_name)
        self.purses.append(0)
        self.in_penalty_box.append(False)
        self.places.append(0)

        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll: int):
        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player] and roll % 2 == 0:
            print("%s is not getting out of the penalty box" % self.players[self.current_player])
            self.is_getting_out_of_penalty_box = False
            return

        if self.in_penalty_box[self.current_player]:
            self.is_getting_out_of_penalty_box = True

            print("%s is getting out of the penalty box" % self.players[self.current_player])

        self.places[self.current_player] = self.places[self.current_player] + roll
        if self.places[self.current_player] > 11:
            self.places[self.current_player] = self.places[self.current_player] - 12

        print(self.players[self.current_player] + "'s new location is " + str(self.places[self.current_player]))
        print("The category is %s" % self._current_category)
        self._ask_question()

    def _ask_question(self):
        if self._current_category == "Pop":
            print(self.pop_questions.pop(0))
        if self._current_category == "Science":
            print(self.science_questions.pop(0))
        if self._current_category == "Sports":
            print(self.sports_questions.pop(0))
        if self._current_category == "Rock":
            print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] in [0, 4, 8]:
            return "Pop"
        if self.places[self.current_player] in [1, 5, 9]:
            return "Science"
        if self.places[self.current_player] in [2, 6, 10]:
            return "Sports"
        if self.places[self.current_player] in [3, 7, 11]:
            return "Rock"  # 3, 7, 11
        err_string = f"Player: {self.current_player} ({self.players[self.current_player]}) in invalid place: {self.places[self.current_player]}"
        raise GameException(err_string)

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player] and not self.is_getting_out_of_penalty_box:
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0
            return True

        print("Answer was correct!!!!")
        self.purses[self.current_player] += 1
        print(self.players[self.current_player] + " now has " + str(self.purses[self.current_player]) + " Gold Coins.")

        winner = self._did_player_win()
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

        return winner

    def wrong_answer(self):
        print("Question was incorrectly answered")
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        self.current_player = self.current_player % self.how_many_players
        return True

    def _did_player_win(self):
        return self.purses[self.current_player] != COINS_TO_WIN


if __name__ == "__main__":
    not_a_winner = False

    game = Game(NUM_QUESTIONS)

    game.add("Chet")
    game.add("Pat")
    game.add("Sue")

    if not game.is_playable():
        print("Too few players!!!")
        exit(1)

    while True:
        game.roll(randrange(DICE_MIN, DICE_MAX))

        possible_outcome = randrange(9)
        if possible_outcome == FAILURE_CONDITION:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner:
            break
