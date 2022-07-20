import pygame
import math
from client import Network
import json

pygame.init()

BOARD_WIDTH = 5
BOARD_HEIGHT = 4

CELL_SIZE = 50
MARGIN = 5

WIDTH, HEIGHT = CELL_SIZE * BOARD_WIDTH + 2 * BOARD_WIDTH * MARGIN, CELL_SIZE * BOARD_HEIGHT + 2 * BOARD_HEIGHT * MARGIN
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chomp game!")

PLAYER_MOVE = pygame.USEREVENT + 1

# Colors
LIME = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (255, 102, 178)
SALMON = (255, 192, 203)
WHITE = (255, 255, 255)
LIGHT_PINK = (255, 181, 197)
SKY_BLUE = (176, 226, 255)
YELLOW = (255, 255, 0)

board = []
for row in range(BOARD_HEIGHT):
    board.append([])
    for column in range(BOARD_WIDTH):
        board[row].append(1)
board[0][0] = -1

class Game:
    def __init__(self):
        self.net = Network()
        self.job = ' '

    def print_board(self):
        global board
        for row in range(BOARD_HEIGHT):
            for column in range(BOARD_WIDTH):
                color = RED
                if board[row][column] == 1:
                    color = LIGHT_PINK
                if row == 0 and column == 0:
                    color = BLACK
                pygame.draw.rect(WIN, color, [(MARGIN + CELL_SIZE) * column + MARGIN,
                                              (MARGIN + CELL_SIZE) * row + MARGIN, CELL_SIZE, CELL_SIZE])

        pygame.display.update()

    def board_collapse(self, r, c):
        global board
        for row in range(BOARD_HEIGHT):
            for column in range(BOARD_WIDTH):
                if row >= r and column >= c:
                    board[row][column] = 0

    def player_move(self, mx, my):
        global board
        position = [-1, -1]
        position[0] = math.floor(mx / (CELL_SIZE + 2 * MARGIN))  # ---------
        position[1] = math.floor(my / (CELL_SIZE + 2 * MARGIN))

        board[position[1]][position[0]] = 0
        self.board_collapse(position[1], position[0])

    def send_data(self):
        global board
        data = str(self.net.id) + ":" + str(self.job) + ";"
        string = json.dumps(board)
        data += string
        reply = self.net.send(data)
        print(reply)
        return reply

    @staticmethod
    def parse_data(data):
        print(data)
        d = data.split(":")[1].split(";")
        l = json.loads(d[1])
        return d[0], l

    def play(self):
        global board
        clock = pygame.time.Clock()
        net = Network()
        # Main loop
        run = True
        while run:
            clock.tick(10)
            job = 'a'
            mx, my = pygame.mouse.get_pos()
            # click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click = True
                        self.player_move(mx, my)
                        self.job, board = self.parse_data(self.send_data())

            # Check if sb won
            winner = True
            for r in range(BOARD_HEIGHT):
                if 1 in board[r]:
                    winner = False
            if winner:
                print("Game over")
                break

            self.print_board()


if __name__ == '__main__':
    game = Game()
    game.play()
