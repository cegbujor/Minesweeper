import sys
import random
import string

# Minseweeper game
# Chidera , 09/05/2020

class GError:
    # Class for error handling
    def __init__(self, error):
        # Constructor
        if error == "Known Input Error": self.show_input_error(known = True)
        elif error == "Unknown Input Error": self.show_input_error(known = False)
        elif error == "Unexpected": self.show_unexpected_error()
    
    def show_input_error(self, known):
        # Function for displaying user input errors
        if known: print("Invalid selection, try again.")
        else: print("Error occured, selection may be invalid. Try again.\n Error: {0},{1}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def show_unexpected_error(self):
        # Function for displaying unexpected errors
        print("Unexpected Error encoutered, exiting.\n Error: {0}, {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

class Board:
    # Class for manipulating game board
    def __init__(self):
        # Constructor class
        self.board = self.create_board()
        self.create_mines()
        self.set_member_contents()

    def create_board(self):
        # Function for creating game board
        board_array = [[Spot(i,j) for j in range(8)] for i in range(8)]
        return board_array

    def create_mines(self):
        # Function for assigning content to game board
        bomb_points = random.sample(range(1,64), 8)
        for bomb_point in bomb_points:
            row = int(bomb_point / 8)
            column = int(bomb_point % 8)
            #self.board[row][column].update_content("m")
            self.board[row][column].set_as_mine()

    def set_member_contents(self):
        # Need to assign contents to determine distance from bomb
        for row_of_spots in self.board:
            for current_spot in row_of_spots:
                # check for mines in adjacent blocks, and update no of adjacent mines
                for x_next in ((current_spot.x - 1), current_spot.x, (current_spot.x + 1)):
                    if x_next >= 0 and x_next < 8:
                        for y_next in ((current_spot.y - 1), current_spot.y, (current_spot.y + 1)):
                            if y_next >= 0 and y_next < 8:
                                if (self.board[x_next][y_next].is_mine and not current_spot.is_mine): 
                                    current_spot.add_adjacent_mine(1)

                if not (current_spot.is_mine): current_spot.update_content(current_spot.no_of_adjacent_mines)
 
    def display_board(self, mode="PLAYER"):
        # Function for displaying game board
    
        # Display first line        
        print(" ", end=" ")
        for letter in string.ascii_uppercase[0:8]: print(letter, end=" ")
        print() 

        row_number = 1 # Row number to display
        for spot_list in self.board:
            print(row_number, end=" ")            
            row_number += 1
            for spot in spot_list:
                # Two modes for player and admin
                if (mode == "PLAYER"):
                    if spot.opened: print(spot.content, end=" ")
                    else: print("*", end=" ")
                elif (mode == "ADMIN"): print(spot.content, end=" ")

            print()

    def request_input(self):
        # Function to get player input
        valid_response = False

        while(not valid_response):
            response = input("Select a location using (yx) e.g (yx) = (A1) \n")
        
            # Perform validation on input    
            try:
                if ( len(response)>2 or int(response[1])<0 or int(response[1])>8 or (response[0] not in string.ascii_uppercase[0:8])):
                    input_error = GError("Known Input Error")
                else:
                    print ("You have selected: {0}".format(response))
                    valid_response = True
                    return response
            except:
                input_error = GError("Unknown Input Error")
                
    def process_response(self, response):
        # Function to process player response

        # Convert response to game_board position
        x_value = int(response[1])-1
        y_value = int(string.ascii_uppercase[0:8].index(response[0]))

        self.board[x_value][y_value].open()
        if self.board[x_value][y_value].check_if_mine():
            return self.display_board_state("END")
        else:
            return self.display_board_state("CONTINUE")
    
    def display_board_state(self, state):
        # Function for displaying board status
        if (state == "CONTINUE"):
            print("You did not hit a mine, continue")
            return True
        elif (state == "END"):
            print("Sorry, you hit a mine")
            return False
    
class Game:
    # Class for controlling game and game loop

    def welcome(self):
        print("Welcome to a demo Minesweeper game.")

    def start(self):
        self.welcome()
        self.game_board = Board()

        game_live = True

        # Main game loop
        while(game_live):
            self.game_board.display_board()
            player_response = self.game_board.request_input()
            game_live = self.game_board.process_response(player_response)

        self.stop()

    def stop(self):
        print("Game over. Thanks for playing")
        self.game_board.display_board("ADMIN")

class Spot:
    # Class for handling spots on the board
    def __init__(self, x, y, content="0"):
        # Constructor
        self.x = x
        self.y = y
        self.opened = False
        self.content = content
        self.is_mine = False
        self.no_of_adjacent_mines = 0
        
    def open(self):
        # Fucntion to open spot
        self.opened = True

    def update_content(self, content):
        # Fucntion to modify spot content
        self.content = content
    
    def set_as_mine(self):
        # Fucntion to set spot as mine
        self.is_mine = True
        self.content = "m"

    def add_adjacent_mine(self, number):
        # Function to increase number of adjacent mines
        self.no_of_adjacent_mines += number

    def check_if_mine(self):
        # Function to check if spot is a mine
        return self.is_mine

def main():
    # Main function

    try:
        # Create game object
        new_game = Game()
        new_game.start()
    except:
        game_error = GError("Unexpected")
        print("Unexpected Error encoutered, exiting.\n Error: {0}, {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

if __name__ == "__main__":
    main()