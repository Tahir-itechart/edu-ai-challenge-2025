# Sea Battle CLI Game (Refactored)

This is a simple command-line interface (CLI) implementation of the classic Sea Battle (Battleship) game, written in modern JavaScript (ES6+).

This project has been refactored from its original procedural script into a modular, class-based architecture to improve readability, maintainability, and structure.

## Gameplay

You play against a CPU opponent. Both players place their ships on a 10x10 grid. Players take turns guessing coordinates to hit the opponent's ships. The first player to sink all of the opponent's ships wins.

- `~` represents water (unknown).
- `S` represents your ships on your board.
- `X` represents a hit (on either board).
- `O` represents a miss (on either board).

## How to Run

1.  **Ensure you have Node.js v14+ installed.** You can download it from [https://nodejs.org/](https://nodejs.org/).
2.  **Navigate to the `task_7` directory** in your terminal.
3.  **Run the game** using the command:
    ```bash
    npm start
    ```
    Alternatively, you can run the main file directly:
    ```bash
    node refactored/main.js
    ```
4.  **Follow the prompts** to enter your guesses (e.g., `00` for the top-left corner, `99` for the bottom-right).

Enjoy the game! 