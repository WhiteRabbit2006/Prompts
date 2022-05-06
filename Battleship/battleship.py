def check_if_coordinates(coordinates):

class Battleship:

    opponent = ""
    give_hint = False
    lengths = [5, 4, 3, 3, 2]
    board = {
        "A": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "B": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "C": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "D": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "E": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "F": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "G": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "H": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "I": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "J": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
    }

    def __init__(self, opponent, give_hint):
        self.opponent = opponent
        self.give_hint = give_hint

    def place_ships(self):
        run = True
        for ship in self.lengths:
            col = 0
            row = ""
            dir = False
            while run:
                run = False  # true is horizontal, false is vertical
                coordinates: str = input("Input the starting square of the boat", "(len:", ship + "): ")
                col = int(coordinates[-1])
                row = coordinates[0].capitalize()
                if not (row.capitalize() in self.board) or not (-1 < col < 10):
                    run = True
                    print("Those are not coordinates. Input a letter A-J and an integer 1-10. ex. H7")
                dir_let = input("What is the direction (h for horizontal or v for vertical)?")
                if not dir_let == "h" or not dir_let == "v":
                    run = True
                    print("Must be a lower-case h or a lower-case v.")
                if dir_let == "h":
                    dir = True
            if dir:
                if col + ship > 10:
                    print("This ship is too long to fit here. Pick another spot.")
            else:
                if
               # for self.board[row][col - 1, col - 1 + ship]




'''
//place each ship by specifying the starting square and direction
//option: play against computer or have two human players
//display board with "-" for unchecked spaces, "o" for misses, "x" for hits 10x10
//display status of each ship
//option: computer suggests best move based on information

functions:
1. constructor: you can call the class with "computer" or "player"
'''