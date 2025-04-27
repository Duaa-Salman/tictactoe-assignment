import math
import time

PLAYER = 'X'
AI = 'O'
EMPTY = ' '

class TicTacToe:
    def __init__(self):
        self.board = [EMPTY] * 9

    def display_board(self):
        print("\nCurrent Board:")
        for i in range(0, 9, 3):
            row = ' | '.join(self.board[i:i+3])
            print(f" {row} ")
            if i < 6:
                print("---+---+---")

    def is_winner(self, player):
        b = self.board
        win_states = [
            [b[0], b[1], b[2]],
            [b[3], b[4], b[5]],
            [b[6], b[7], b[8]],
            [b[0], b[3], b[6]],
            [b[1], b[4], b[7]],
            [b[2], b[5], b[8]],
            [b[0], b[4], b[8]],
            [b[2], b[4], b[6]],
        ]
        return [player] * 3 in win_states

    def is_draw(self):
        return EMPTY not in self.board and not self.is_winner(PLAYER) and not self.is_winner(AI)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == EMPTY]

    def make_move(self, index, player):
        if self.board[index] == EMPTY:
            self.board[index] = player
            return True
        return False

    def undo_move(self, index):
        self.board[index] = EMPTY

    def evaluate(self):
        if self.is_winner(AI):
            return 1
        elif self.is_winner(PLAYER):
            return -1
        return 0

# -------- Minimax Algorithm --------

class MinimaxAI:
    def __init__(self):
        self.node_count = 0

    def minimax(self, game, depth, is_maximizing):
        self.node_count += 1
        score = game.evaluate()

        if score in [1, -1] or game.is_draw():
            return score

        if is_maximizing:
            best_score = -math.inf
            for move in game.available_moves():
                game.make_move(move, AI)
                score = self.minimax(game, depth + 1, False)
                game.undo_move(move)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in game.available_moves():
                game.make_move(move, PLAYER)
                score = self.minimax(game, depth + 1, True)
                game.undo_move(move)
                best_score = min(score, best_score)
            return best_score

    def find_best_move(self, game):
        best_score = -math.inf
        best_move = -1
        for move in game.available_moves():
            game.make_move(move, AI)
            score = self.minimax(game, 0, False)
            game.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

# -------- Alpha-Beta Pruning --------

class AlphaBetaAI:
    def __init__(self):
        self.node_count = 0

    def minimax_ab(self, game, depth, alpha, beta, is_maximizing):
        self.node_count += 1
        score = game.evaluate()

        if score in [1, -1] or game.is_draw():
            return score

        if is_maximizing:
            max_eval = -math.inf
            for move in game.available_moves():
                game.make_move(move, AI)
                eval = self.minimax_ab(game, depth + 1, alpha, beta, False)
                game.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game.available_moves():
                game.make_move(move, PLAYER)
                eval = self.minimax_ab(game, depth + 1, alpha, beta, True)
                game.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, game):
        best_score = -math.inf
        best_move = -1
        for move in game.available_moves():
            game.make_move(move, AI)
            score = self.minimax_ab(game, 0, -math.inf, math.inf, False)
            game.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

# -------- Performance Comparison --------

def compare_algorithms():
    initial_board = [EMPTY] * 9
    game = TicTacToe()
    game.board = initial_board.copy()

    minimax_ai = MinimaxAI()
    alpha_beta_ai = AlphaBetaAI()

    print("\nRunning Minimax...")
    start = time.time()
    move_mm = minimax_ai.find_best_move(game)
    end = time.time()
    print(f"Best Move: {move_mm}, Nodes Evaluated: {minimax_ai.node_count}, Time: {end - start:.4f}s")

    print("\nRunning Alpha-Beta Pruning...")
    start = time.time()
    move_ab = alpha_beta_ai.find_best_move(game)
    end = time.time()
    print(f"Best Move: {move_ab}, Nodes Evaluated: {alpha_beta_ai.node_count}, Time: {end - start:.4f}s")

if __name__ == "__main__":
    compare_algorithms()

