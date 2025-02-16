document.addEventListener("DOMContentLoaded", function() {
    const cells = document.querySelectorAll(".cell");
    const status = document.getElementById("status");
    const resetButton = document.getElementById("reset");

    let board = [["", "", ""], ["", "", ""], ["", "", ""]];
    let currentPlayer = "X";
    let gameActive = true;

    function updateBoard() {
        cells.forEach((cell, index) => {
            let row = Math.floor(index / 3);
            let col = index % 3;
            cell.textContent = board[row][col];
            cell.classList.toggle("taken", board[row][col] !== "");
        });
    }

    function checkWinner() {
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6] // Diagonals
        ];

        let flatBoard = board.flat();
        for (let pattern of winPatterns) {
            let [a, b, c] = pattern;
            if (flatBoard[a] && flatBoard[a] === flatBoard[b] && flatBoard[a] === flatBoard[c]) {
                status.innerText = `Player ${flatBoard[a]} Wins!`;
                gameActive = false;
                return;
            }
        }

        if (!flatBoard.includes("")) {
            status.innerText = "It's a Draw!";
            gameActive = false;
        }
    }

    function aiMove() {
        fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: board })
        })
        .then(response => response.json())
        .then(data => {
            board = data.board;
            updateBoard();
            checkWinner();
            if (gameActive) {
                currentPlayer = "X";
                status.innerText = "Player X's turn";
            }
        })
        .catch(error => console.error("Error:", error));
    }

    cells.forEach((cell, index) => {
        cell.addEventListener("click", function() {
            if (!gameActive) return;

            let row = Math.floor(index / 3);
            let col = index % 3;

            if (board[row][col] === "") {
                board[row][col] = currentPlayer;
                updateBoard();
                checkWinner();

                if (gameActive) {
                    currentPlayer = "O";
                    status.innerText = "AI is thinking...";
                    setTimeout(aiMove, 500);
                }
            }
        });
    });

    resetButton.addEventListener("click", function() {
        board = [["", "", ""], ["", "", ""], ["", "", ""]];
        gameActive = true;
        currentPlayer = "X";
        status.innerText = "Player X's turn";
        updateBoard();
    });
});
