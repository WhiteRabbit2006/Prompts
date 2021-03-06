from os import system, name
import random


def get_bool(question):  # given a question, returns yes or no answer as True for yes and False for no
    answer = input(question)
    while True:
        if not answer.capitalize() == "Yes" and not answer.capitalize() == "No":
            answer = input('Please answer "yes" or "no": ')
            continue
        break
    if answer.capitalize() == "Yes":
        return True
    return False


def clear():  # clears previous output from run screen
    if name == "nt":  # for windows name is 'nt'
        system('cls')
    else:  # for macos or linux name is 'posix'
        system('clear')


class Player:
    lengths = [5, 4, 3, 3, 2]  # lengths of ships
    keys = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]  # names of rows

    def __init__(self, player):  # if human is playing player should be true, otherwise false and computer plays
        self.player = player
        self.give_hint = False
        self.num_guessed = 0  # counts guesses
        self.already_guessed = []  # stores previous guesses as coordinates
        self.board = {  # board with all ships placed
            "A": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "B": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "C": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "D": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "E": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "F": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "G": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "H": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "I": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "J": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        }
        self.guesses = {  # logs result of guesses
            "A": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "B": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "C": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "D": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "E": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "F": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "G": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "H": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "I": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "J": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        }
        self.ship_squares = [  # will contain all squares occupied by each ship; ex. a1, a2, a3
            [],
            [],
            [],
            [],
            []
        ]
        self.ship_healths = [5, 4, 3, 3, 2]  # goes down every time corresponding ship sustains a hit
        if self.player:
            self.hint = get_bool("Does this player want suggestions from the computer? (yes or no): ")
            self.random_ships = get_bool("Does this player want randomly placed ships? (yes or no): ")
        if self.player and not self.random_ships:
            self.place_ships()
        else:
            self.random_ship_placer()
        self.health = 17  # total length of all ships; goes down one for every hit on a ship (lose at 0)

    def turn(self, opponent):  # method that runs for every turn
        # TODO: print when ships are destroyed
        # TODO: implement computer suggestions
        if self.player:
            print("\nYour board: \n" + self.get_board())
            print("Your guesses:\n" + self.get_guesses())
        if self.player:
            guess = self.guess()
            print(self.guess_it(guess, opponent))
        else:
            guess = self.random_guesser()
            self.guess_it(guess, opponent)

    def get_turn_num(self):
        return self.num_guessed

    def place_ships(self):  # takes user input to place ships as coordinates and directions
        for ship in self.lengths:
            run = True
            direction = False
            while run:
                run = False  # true is horizontal, false is vertical
                coordinates = input("Input the starting square of the boat " + "(len: " + str(ship) + "): ")
                # noinspection PyBroadException
                try:
                    col = int(coordinates[1:])
                    row = coordinates[0].capitalize()
                except BaseException:
                    run = True
                    print("Those are not coordinates. Input a letter A-J and an integer 1-10. ex. H7")
                    continue
                if not (row.capitalize() in self.keys) or not (-1 < col < 11) or not 1 < len(coordinates) < 4:
                    run = True
                    print("Those are not coordinates. Input a letter A-J and an integer 1-10. ex. H7")
                    continue
                direction_let = input("What is the direction (h for horizontal or v for vertical)?")
                if not direction_let == "h" and not direction_let == "v":
                    run = True
                    print("Must be a lower-case h or a lower-case v.")
                if direction_let == "h":
                    direction = True

                if not self.place_ship(coordinates, direction, ship):
                    print("No space for a ship there. Make sure there is not another ship in the way.")
                    run = True

    def place_ship(self, start, direction, ship):  # populates board with ship based on parameters
        if self.open_spot(start, direction, ship):
            col = int(start[1:])
            row = start[0].capitalize()
            if direction:
                for tile in range(ship):
                    self.board[row][col + tile - 1] = "-"
            else:
                initial = sorted(self.board).index(row)
                for num in range(initial, initial + ship):
                    if self.board[sorted(self.board)[num]][col - 1] == " ":
                        self.board[sorted(self.board)[num]][col - 1] = "-"
            return True
        return False

    # to be called by place_ship
    def open_spot(self, start, direction, ship):  # determines whether a ship can be placed in a certain location
        col = int(start[1:])
        row = start[0].capitalize()
        if direction:
            if col - 1 + ship > 10:
                return False
            else:
                for tile in range(ship):
                    if self.board[row][col - 1 + tile] == " ":
                        continue
                    else:
                        return False
                return True
        else:
            start = self.keys.index(row)
            if start + ship > len(self.keys):
                return False
            else:
                for num in range(start, start + ship):
                    if self.board[self.keys[num]][col - 1] == " ":
                        continue
                    else:
                        return False
                return True

    def random_ship_placer(self):  # randomly places ships on grid
        for ship in self.lengths:
            run = True
            while run:
                run = False
                start_square = list(self.board)[random.randint(0, len(list(self.board)) - ship)] + str(
                    random.randint(0, 10 - ship))
                direction = bool(random.getrandbits(1))
                if self.place_ship(start_square, direction, ship):
                    continue
                run = True

    # def smart_ship_placer(self):
    # TODO: implement smart_ship_placer method

    def guess(self):  # gets a guess from the player
        while True:
            guess = input("Guess a square that you haven't already guessed: ")
            # noinspection PyBroadException
            try:
                col = int(guess[1:])
                row = guess[0].capitalize()
            except BaseException:
                print("Those are not coordinates. Input a letter A-J and an integer 1-10. ex. H7")
                continue
            if not (row.capitalize() in self.board) or not (-1 < col < 11) or not 1 < len(guess) < 4:
                print("Those are not coordinates. Input a letter A-J and an integer 1-10. ex. H7")
                continue
            if (str(row) + str(col)).capitalize() in self.already_guessed:
                print("You already guessed these coordinates.")
                continue
            self.num_guessed += 1
            return guess

    # def smart_guess(self):
    # TODO: implement smart_guess method

    def random_guesser(self):  # guesses a random square
        guess = list(self.board)[random.randint(0, len(list(self.board)) - 1)] + str(random.randint(0, 10))
        while guess in self.already_guessed:
            guess = list(self.board)[random.randint(0, len(list(self.board)) - 1)] + str(random.randint(0, 10))
        return guess

    def guess_it(self, guess, board):  # given a guess and another board, calls guess_result on other board and records outcome in self.guesses
        self.already_guessed.append(guess.capitalize())
        col = int(guess[1:]) - 1
        row = guess[0].capitalize()
        if (row.capitalize() in self.board) and (-1 < col < 10):
            guess_result = board.guess_result(guess)
            if guess_result:
                self.guesses[row][col] = "X"
                return "hit!"  # hit
            self.guesses[row][col] = "O"
            return "miss."  # miss

    # to be called by guess_it
    def guess_result(self, guess):  # given a guess, returns false if it is a miss, takes hit and returns true if guess is a hit
        col = int(guess[1:]) - 1
        row = guess[0].capitalize()
        if self.board[row][col] == "-":
            self.board[row][col] = "X"
            self.health -= 1
            return True
        self.board[row][col] = "O"
        return False

    def get_guesses(self):  # returns board of guesses (recorded hits and misses)
        # TODO: improve formatting
        formatted_guesses = ""
        for key in self.guesses:
            formatted_guesses += (str(self.guesses[key]) + "\n")
        return formatted_guesses

    def get_health(self):
        return self.health

    def get_board(self):  # returns players board
        # TODO: improve formatting
        formatted_board = ""
        for key in self.board:
            formatted_board += (str(self.board[key]) + "\n")
        return formatted_board


class Game:  # facilitates game between two players

    def __init__(self, player1, player2):  # takes two booleans which determine whether the players are human
        self.player1 = player1
        self.player2 = player2
        if player1:
            print("\nPlayer 1:\n")
            self.p1 = Player(True)
        else:
            self.p1 = Player(False)
        if player2:
            print("\nPlayer 2:\n")
            self.p2 = Player(True)
        else:
            self.p2 = Player(False)

    def play(self):  # loops through turns until a player wins
        if self.player1 or self.player2:
            input("\nBegin?")
        while self.p1.get_health() > 0 and self.p2.get_health() > 0:
            # input("\nStart turn Player 1? ")
            if self.p1:
                clear()
                print("Player 1 turn", str(self.p1.get_turn_num() + 1) + ":\n")
            self.p1.turn(self.p2)
            if self.p1:
                input("\nEnd turn Player 1?")
            if self.player1 and self.player2:
                # input("\nStart turn Player 2? ")
                clear()
                print("Player 2 turn", str(self.p1.get_turn_num() + 1) + ":\n")
            self.p2.turn(self.p1)
            if self.player1 and self.player2:
                input("\nEnd turn player 2?")
        if self.p1.get_health() == 0:
            print("Player 2 wins!")
        else:
            print("Player 1 wins!")


if __name__ == '__main__':
    g = Game(True, get_bool("Are there two players? "))
    g.play()

# TODO: make fancy display
