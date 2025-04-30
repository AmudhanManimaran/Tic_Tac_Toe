from flask import Flask, render_template, jsonify, request
import numpy as np
import random

app = Flask(__name__)

def is_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != '' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']

def minimax(board, depth, is_maximizing, alpha, beta, max_depth):
    if is_winner(board, 'O'):
        return 10 - depth
    if is_winner(board, 'X'):
        return depth - 10
    if is_draw(board) or depth >= max_depth:
        return 0

    if is_maximizing:
        best_score = -np.inf
        for i, j in get_empty_cells(board):
            board[i][j] = 'O'
            score = minimax(board, depth + 1, False, alpha, beta, max_depth)
            board[i][j] = ''
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = np.inf
        for i, j in get_empty_cells(board):
            board[i][j] = 'X'
            score = minimax(board, depth + 1, True, alpha, beta, max_depth)
            board[i][j] = ''
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def best_move(board):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    center = (1, 1)
    empty_cells = get_empty_cells(board)

    # Step 1: If user's first move is a corner, AI must take center
    user_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 'X']
    if len(user_moves) == 1 and user_moves[0] in corners:
        if board[center[0]][center[1]] == '':
            return center

    # Step 2: Try winning move for AI
    for i, j in empty_cells:
        board[i][j] = 'O'
        if is_winner(board, 'O'):
            board[i][j] = ''
            return (i, j)
        board[i][j] = ''

    # Step 3: Block opponent's winning move
    for i, j in empty_cells:
        board[i][j] = 'X'
        if is_winner(board, 'X'):
            board[i][j] = ''
            return (i, j)
        board[i][j] = ''

    # Step 4: Take center if available
    if board[center[0]][center[1]] == '':
        return center

    # Step 5: Take a corner if available
    available_corners = [pos for pos in corners if board[pos[0]][pos[1]] == '']
    if available_corners:
        return random.choice(available_corners)

    # Step 6: Minimax for best possible move
    best_score = -np.inf
    move = None
    max_depth = 5

    for i, j in empty_cells:
        board[i][j] = 'O'
        score = minimax(board, 0, False, -np.inf, np.inf, max_depth)
        board[i][j] = ''
        if score > best_score:
            best_score = score
            move = (i, j)

    return move if move else random.choice(empty_cells)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    next_move = best_move(board)
    if next_move:
        board[next_move[0]][next_move[1]] = 'O'
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)
