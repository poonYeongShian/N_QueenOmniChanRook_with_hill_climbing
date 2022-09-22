"""
File for Question 3 of FIT3080 S2/2022
"""
__author__ = "Poon Yeong Shian(30696003)"


from random import randrange
import copy


# Question 3
def generate_board(N):
    """This method initialised a N x N board and its state"""
    board = [[(0, " ")] * N for _ in range(N)]
    state = [(0, " ")] * N
    return board, state


def random_assign(board, state):
    """This method takes in empty board and put a random chess in each row"""

    # This list is used as a probability
    # "o" is omni, "q" is queen, "c" is chancellor, "r" is rook
    # e.g.  There is 30% chance for "o" to appear,
    #                40% chance for "q" to appear,
    #                10% chance for "r" to appear,
    #                10% chance for "c" to appear,
    #                10% chance for no chess appear,

    chess = ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"]
    for i in range(len(board)):
        state[i] = randrange(7)

        # randomly choose chess based on probability
        chess_type = chess[randrange(10)]
        board[i][state[i]] = (1, chess_type)

    return board


def current_num_atk(brd, state):
    """This method calculate the number of chess attacking each other"""

    attacking = 0
    N = len(brd)
    # For each row
    for row in range(N):
        col = state[row]

        # current chess is omni
        if brd[row][col][1] == "o":
            attacking += rook_pattern_atk(N, brd, col, row)
            attacking += diag_pattern_atk(N, brd, col, row)
            attacking += knight_pattern_atk(N, brd, col, row)

        # current chess is queen
        if brd[row][col][1] == "q":
            attacking += rook_pattern_atk(N, brd, col, row)
            attacking += diag_pattern_atk(N, brd, col, row)

        # current chess is chancellor
        elif brd[row][col][1] == "c":
            attacking += rook_pattern_atk(N, brd, col, row)
            attacking += knight_pattern_atk(N, brd, col, row)

        # current chess is rook
        elif brd[row][col][1] == "r":
            attacking += rook_pattern_atk(N, brd, col, row)

    return attacking / 2


def diag_pattern_atk(N, brd, col, row):
    """This method calculate the number of chess that the current chess is attacking
    diagonally in its current position"""

    attacking = 0

    # bottom-right
    temp_row = row + 1
    temp_col = col + 1
    while temp_col < N and temp_row < N:
        if brd[temp_row][temp_col][0] == 1:
            attacking += 1
            break
        temp_row += 1
        temp_col += 1

    # upper-left
    temp_row = row - 1
    temp_col = col - 1
    while temp_col >= 0 and temp_row >= 0:
        if brd[temp_row][temp_col][0] == 1:
            attacking += 1
            break
        temp_row -= 1
        temp_col -= 1

    # upper-right
    temp_row = row - 1
    temp_col = col + 1
    while temp_col < N and temp_row >= 0:
        if brd[temp_row][temp_col][0] == 1:
            attacking += 1
            break

        temp_row -= 1
        temp_col += 1

    # bottom-left
    temp_row = row + 1
    temp_col = col - 1
    while temp_col >= 0 and temp_row < N:
        if brd[temp_row][temp_col][0] == 1:
            attacking += 1
            break
        temp_row += 1
        temp_col -= 1

    return attacking


def rook_pattern_atk(N, brd, col, row):
    """This method calculate the number of chess that the current chess is attacking
    vertically in its current position"""

    attacking = 0

    # down
    for down in range(row + 1, N):
        if brd[down][col][0] == 1:
            attacking += 1
            break
    # up
    for up in range(row - 1, -1, -1):
        if brd[up][col][0] == 1:
            attacking += 1
            break

    return attacking


def knight_pattern_atk(N, brd, col, row):
    """This method calculate the number of chess that the current chess is attacking
    with (knight attacking pattern) in its current position"""

    attacking = 0

    if (row - 2 >= 0 and col - 1 >= 0) and brd[row - 2][col - 1][0] == 1:
        attacking += 1
    if (row - 1 >= 0 and col - 2 >= 0) and brd[row - 1][col - 2][0] == 1:
        attacking += 1
    if (row + 1 < N and col - 2 >= 0) and brd[row + 1][col - 2][0] == 1:
        attacking += 1
    if (row + 2 < N and col - 1 >= 0) and brd[row + 2][col - 1][0] == 1:
        attacking += 1
    if (row - 2 >= 0 and col + 1 < N) and brd[row - 2][col + 1][0] == 1:
        attacking += 1
    if (row - 1 >= 0 and col + 2 < N) and brd[row - 1][col + 2][0] == 1:
        attacking += 1
    if (row + 1 < N and col + 2 < N) and brd[row + 1][col + 2][0] == 1:
        attacking += 1
    if (row + 2 < N and col + 2 < N) and brd[row + 2][col + 1][0] == 1:
        attacking += 1

    return attacking


def get_neighbour(nBoard, state):
    """This function generating all neighbours of
    the current state and return the neighbour with less chess attacking each other"""

    # initialised neighbour board and neighbour state, and their best result
    N = len(nBoard)
    neighbourBoard = copy.deepcopy(nBoard)
    neighbourState = copy.deepcopy(state)

    bestNeighbourState = copy.deepcopy(neighbourState)
    bestNeighbourBoard = copy.deepcopy(neighbourBoard)

    # initialised best_num_atk with the current board
    best_num_atk = current_num_atk(nBoard, state)

    # For each row
    for i in range(N):
        # For each col
        for j in range(N):
            # remember the current state
            j_temp_tuple = neighbourBoard[i][neighbourState[i]]
            # skip current state
            if j != state[i]:
                neighbourState[i] = j

                # move the current chess to that col
                neighbourBoard[i][neighbourState[i]] = j_temp_tuple
                neighbourBoard[i][state[i]] = (0, " ")

                # recalculate the number of chess attacking each other
                current_n_atk = current_num_atk(neighbourBoard, neighbourState)

                # Check is it a best move?
                if current_n_atk <= best_num_atk:
                    best_num_atk = current_n_atk
                    bestNeighbourState = copy.deepcopy(neighbourState)
                    bestNeighbourBoard = copy.deepcopy(neighbourBoard)

                # Move the chess back to its original position
                neighbourBoard[i][neighbourState[i]] = (0, " ")
                neighbourState[i] = state[i]
                neighbourBoard[i][state[i]] = j_temp_tuple

    return bestNeighbourBoard, bestNeighbourState


def hill_climbling(board, state1):
    """This function perform hill climbling to find
    the best neighbour with no chess attacking each other"""

    # initialised the best neighbour board and its number of chess attacking each other
    neigh_board, sta = get_neighbour(board, state1)
    current_best = current_num_atk(neigh_board, sta)

    # initialised counter
    counter = 0
    # previous number of chess attacking each other
    previous = 0

    # continue to find the best neighbour until no chess is attacking each other
    while current_best != 0:
        neigh_board, sta = get_neighbour(neigh_board, sta)
        current_best = current_num_atk(neigh_board, sta)

        # If the number chess attacking each other does not reduced
        if previous == current_best:

            # regenerate a new board
            board, state1 = generate_board(8)
            board = random_assign(board, state1)
            neigh_board, sta = get_neighbour(board, state1)
            current_best = current_num_atk(neigh_board, sta)

        # Remember the current number chess attacking each other
        previous = current_best
        counter += 1

        # Exit if we cannot found a improve solution after 50 iteration
        if counter == 50:
            return 0, neigh_board

    # return point based on the type of chess on the board
    return calc_point(board, neigh_board, sta), neigh_board


def calc_point(board, neigh_board, sta):
    """This method calculate total points based on type of chess on the board"""
    point = 0
    for i in range(len(board)):
        temp = neigh_board[i][sta[i]]
        if temp[1] == 'o':
            # Omni
            point += 5
        elif temp[1] == 'q':
            # Queen
            point += 4
        elif temp[1] == 'c':
            # Chancellor
            point += 3
        elif temp[1] == 'r':
            # Rook
            point += 2
    return point


def main():
    # Generate new board
    board, state1 = generate_board(8)
    board = random_assign(board, state1)
    # Initialise max point
    max_point = 0
    max_board = []

    # Try different pieces of chess on board
    for i in range(200):
        temp, brd = hill_climbling(board, state1)
        if temp > max_point:
            max_point = temp
            max_board = brd

    print(max_board)
    print("max point: ", max_point)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
