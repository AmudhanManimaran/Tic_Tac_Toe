from flask import Flask, render_template, jsonify, request
import numpy as np
import random

app = Flask(__name__)

# Tic Tac Toe board
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

def minimax(board, depth, is_maximizing, max_depth):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if is_draw(board) or depth >= max_depth:
        return 0

    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False, max_depth)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True, max_depth)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -np.inf
    move = None
    max_depth = random.choice([2, 3, 4])  # AI sometimes looks deeper, making it unpredictable

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False, max_depth)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

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
