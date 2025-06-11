import { Board } from './board.js';
import { HumanPlayer, CPUPlayer } from './player.js';
import * as ui from './ui.js';
import { NUM_SHIPS } from './constants.js';

export class Game {
    constructor() {
        this.player = new HumanPlayer();
        this.cpu = new CPUPlayer();
        this.playerBoard = new Board(true); // isPlayerBoard = true
        this.cpuBoard = new Board();
    }

    async start() {
        ui.printMessage(`\\nLet's play Sea Battle!`);
        ui.printMessage(`Try to sink the ${NUM_SHIPS} enemy ships.`);
        this.playerBoard.placeShipsRandomly();
        this.cpuBoard.placeShipsRandomly();
        await this.gameLoop();
    }

    async gameLoop() {
        let gameOver = false;
        while (!gameOver) {
            ui.printBoard(this.playerBoard, this.cpuBoard);
            
            // Player's turn
            const playerGuess = await ui.getPlayerGuess(this.player.guesses);
            this.player.guesses.add(playerGuess);
            const playerResult = this.cpuBoard.receiveGuess(playerGuess);
            this.handleGuessResult('Player', playerResult, playerGuess);

            if (this.cpuBoard.allShipsSunk()) {
                ui.printMessage('\\n*** CONGRATULATIONS! You sunk all enemy battleships! ***');
                gameOver = true;
                continue;
            }

            // CPU's turn
            ui.printMessage("\\n--- CPU's Turn ---");
            const cpuGuess = this.cpu.generateGuess();
            const cpuResult = this.playerBoard.receiveGuess(cpuGuess);
            this.handleGuessResult('CPU', cpuResult, cpuGuess);
            
            if (cpuResult === 'hit' || cpuResult === 'sunk') {
                this.cpu.updateAfterHit(cpuGuess, cpuResult === 'sunk');
            }

            if (this.playerBoard.allShipsSunk()) {
                ui.printMessage('\\n*** GAME OVER! The CPU sunk all your battleships! ***');
                gameOver = true;
            }
        }
        ui.printBoard(this.playerBoard, this.cpuBoard);
        ui.closeInterface();
    }
    
    handleGuessResult(playerName, result, guess) {
        switch (result) {
            case 'hit':
                ui.printMessage(`${playerName} HIT at ${guess}!`);
                break;
            case 'miss':
                ui.printMessage(`${playerName} MISS at ${guess}.`);
                break;
            case 'sunk':
                 ui.printMessage(`${playerName} HIT at ${guess}!`);
                 const message = (playerName === 'Player') 
                    ? 'You sunk an enemy battleship!' 
                    : 'CPU sunk your battleship!';
                 ui.printMessage(message);
                break;
        }
    }
} 